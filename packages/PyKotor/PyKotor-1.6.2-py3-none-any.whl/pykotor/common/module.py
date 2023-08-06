from __future__ import annotations

import os.path
from contextlib import suppress
from copy import copy
from typing import List, TypeVar, Generic, Optional, Any

from pykotor.resource.formats.bwm.bwm_auto import bytes_bwm
from pykotor.resource.formats.erf import write_erf, read_erf, ERFType
from pykotor.resource.formats.rim import read_rim, write_rim

from pykotor.resource.formats.vis.vis_auto import bytes_vis

from pykotor.resource.formats.tpc.tpc_auto import bytes_tpc

from pykotor.common.misc import CaseInsensitiveDict

from pykotor.common.stream import BinaryReader, BinaryWriter
from pykotor.extract.capsule import Capsule
from pykotor.extract.file import ResourceIdentifier
from pykotor.extract.installation import Installation, SearchLocation
from pykotor.resource.formats.bwm import read_bwm
from pykotor.resource.formats.gff import read_gff
from pykotor.resource.formats.lyt import LYT
from pykotor.resource.formats.lyt.lyt_auto import read_lyt, bytes_lyt
from pykotor.resource.formats.mdl import MDL
from pykotor.resource.formats.tpc import read_tpc, TPC
from pykotor.resource.formats.vis import read_vis, VIS
from pykotor.resource.generics.are import ARE, read_are, bytes_are
from pykotor.resource.generics.dlg import read_dlg, bytes_dlg
from pykotor.resource.generics.git import GIT, read_git, bytes_git
from pykotor.resource.generics.ifo import IFO, read_ifo, bytes_ifo
from pykotor.resource.generics.pth import read_pth, bytes_pth, PTH
from pykotor.resource.generics.utc import UTC, read_utc, bytes_utc
from pykotor.resource.generics.utd import UTD, read_utd, bytes_utd
from pykotor.resource.generics.ute import UTE, read_ute, bytes_ute
from pykotor.resource.generics.uti import UTI, read_uti, bytes_uti
from pykotor.resource.generics.utm import UTM, read_utm, bytes_utm
from pykotor.resource.generics.utp import UTP, read_utp, bytes_utp
from pykotor.resource.generics.uts import read_uts, bytes_uts, UTS
from pykotor.resource.generics.utt import UTT, read_utt, bytes_utt
from pykotor.resource.generics.utw import UTW, read_utw, bytes_utw
from pykotor.resource.type import ResourceType
from pykotor.tools.model import list_textures, list_lightmaps

T = TypeVar('T')
SEARCH_ORDER = [SearchLocation.OVERRIDE, SearchLocation.CUSTOM_MODULES, SearchLocation.CHITIN]


class Module:
    def __init__(
            self,
            root: str,
            installation: Installation,
            custom_capsule: Optional[Capsule] = None
    ):
        self._installation = installation
        self._root = root = root.lower()

        self._capsules = [custom_capsule] if custom_capsule is not None else []
        self._capsules.extend([Capsule(installation.module_path() + module) for module in installation.module_names() if root in module.lower()])

        for capsule in self._capsules:
            if capsule.exists("module", ResourceType.IFO):
                ifo = read_gff(capsule.resource("module", ResourceType.IFO))
                self._id = ifo.root.get_resref("Mod_Entry_Area").get().lower()
                break
        else:
            raise ValueError("Unable to locate module IFO file for '{}'.".format(root))

        self.resources: CaseInsensitiveDict[ModuleResource] = CaseInsensitiveDict()
        self.reload_resources()

    @staticmethod
    def get_root(
            filepath: str
    ) -> str:
        """
        Returns the root name for a module from the given filepath (or filename). For example "danm13_s.rim" would
        become "danm13".

        Args:
            filepath: The filename or filepath of one of the module encapsulated file.

        Returns:
            The string for the root name of a module.
        """
        root = os.path.basename(filepath).replace(".rim", "").replace(".erf", "").replace(".mod", "").lower()
        roota = root[:5]
        rootb = root[5:]
        if "_" in rootb:
            rootb = rootb[:rootb.index("_")]
        return roota + rootb

    def capsules(
            self
    ) -> List[Capsule]:
        """
        Returns a copy of the capsules used by the module.

        Returns:
            A list of linked capsules.
        """
        return copy(self._capsules)

    def reload_resources(
            self
    ):
        # Look in module files
        for capsule in self._capsules:
            for resource in capsule:
                resname = resource.resname()
                restype = resource.restype()
                self.add_locations(resname, restype, [capsule.path()])

        # Look for LYT/VIS
        for resource in self._installation.chitin_resources():
            if resource.resname() == self._id:
                self.add_locations(resource.resname(), resource.restype(), [resource.filepath()])
        for directory in self._installation.override_list():
            for resource in self._installation.override_resources(directory):
                if resource.resname() == self._id:
                    self.add_locations(resource.resname(), resource.restype(), [resource.filepath()])

        # Any resource linked in the GIT not present in the module files
        original = self.git().active()
        look_for = []
        for location in self.git().locations():
            self.git().activate(location)
            git = self.git().resource()
            [look_for.append(ResourceIdentifier(creature.resref.get(), ResourceType.UTC)) for creature in git.creatures]
            [look_for.append(ResourceIdentifier(placeable.resref.get(), ResourceType.UTP)) for placeable in
             git.placeables]
            [look_for.append(ResourceIdentifier(door.resref.get(), ResourceType.UTD)) for door in git.doors]
            [look_for.append(ResourceIdentifier(sound.resref.get(), ResourceType.UTS)) for sound in git.sounds]
            [look_for.append(ResourceIdentifier(waypoint.resref.get(), ResourceType.UTW)) for waypoint in git.waypoints]
            [look_for.append(ResourceIdentifier(encounter.resref.get(), ResourceType.UTE)) for encounter in
             git.encounters]
            [look_for.append(ResourceIdentifier(trigger.resref.get(), ResourceType.UTT)) for trigger in git.triggers]
            [look_for.append(ResourceIdentifier(store.resref.get(), ResourceType.UTM)) for store in git.stores]
        self.git().activate(original)

        # Models referenced in LYTs
        original = self.layout().active()
        for location in self.layout().locations():
            self.layout().activate(location)
            layout = self.layout().resource()
            for room in layout.rooms:
                look_for.append(ResourceIdentifier(room.model, ResourceType.MDL))
                look_for.append(ResourceIdentifier(room.model, ResourceType.MDX))
                look_for.append(ResourceIdentifier(room.model, ResourceType.WOK))
        self.layout().activate(original)

        search = self._installation.locations(look_for, [SearchLocation.OVERRIDE, SearchLocation.CHITIN])
        for identifier, locations in search.items():
            self.add_locations(identifier.resname, identifier.restype, [location.filepath for location in locations])

        # Also try get paths for textures in models
        look_for = []
        textures = set()
        for model in self.models():
            with suppress(Exception):
                data = model.data()
                for texture in list_textures(data):
                    textures.add(texture)
                for lightmap in list_lightmaps(data):
                    textures.add(lightmap)
        for texture in textures:
            look_for.append(ResourceIdentifier(texture, ResourceType.TPC))
            look_for.append(ResourceIdentifier(texture, ResourceType.TGA))
        search = self._installation.locations(look_for, [SearchLocation.OVERRIDE, SearchLocation.CHITIN,
                                                         SearchLocation.TEXTURES_TPA,
                                                         SearchLocation.TEXTURES_TPB, SearchLocation.TEXTURES_TPC])
        for identifier, locations in search.items():
            if len(locations) == 0:
                continue
            self.add_locations(identifier.resname, identifier.restype, [location.filepath for location in locations])

        for resource in self.resources.values():
            resource.activate()

    def add_locations(
            self,
            resname: str,
            restype: ResourceType,
            locations: List[str]
    ):
        # In order to store TGA resources in the same ModuleResource as their TPC counterpart, we use the .TPC extension
        # instead of the .TGA for the dictionary key.
        filename_ext = str(ResourceType.TPC if restype == ResourceType.TGA else restype)
        filename = "{}.{}".format(resname, filename_ext)
        if filename in self.resources:
            self.resources[filename].add_locations(locations)
        else:
            self.resources[filename] = ModuleResource(resname, restype, self._installation)
            self.resources[filename].add_locations(locations)

    def installation(
            self
    ) -> Installation:
        return self._installation

    def resource(
            self,
            resname: str,
            restype: ResourceType
    ) -> Optional[ModuleResource]:
        filename = resname + "." + restype.extension
        return self.resources[filename] if filename in self.resources else None

    def layout(
            self
    ) -> ModuleResource[LYT]:
        for filename, resource in self.resources.items():
            if resource.resname().lower() == self._id and resource.restype() == ResourceType.LYT:
                return resource

    def vis(
            self
    ) -> ModuleResource[VIS]:
        for filename, resource in self.resources.items():
            if resource.resname().lower() == self._id and resource.restype() == ResourceType.VIS:
                return resource

    def are(
            self
    ) -> ModuleResource[ARE]:
        for filename, resource in self.resources.items():
            if resource.resname().lower() == self._id and resource.restype() == ResourceType.ARE:
                return resource

    def git(
            self
    ) -> ModuleResource[GIT]:
        for filename, resource in self.resources.items():
            if resource.resname().lower() == self._id and resource.restype() == ResourceType.GIT:
                return resource

    def pth(
            self
    ) -> ModuleResource[PTH]:
        for filename, resource in self.resources.items():
            if resource.resname().lower() == self._id and resource.restype() == ResourceType.PTH:
                return resource

    def info(
            self
    ) -> ModuleResource[IFO]:
        for filename, resource in self.resources.items():
            if resource.resname().lower() == "module" and resource.restype() == ResourceType.IFO:
                return resource

    def creature(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTC]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTC:
                return resource
        return None

    def creatures(
            self
    ) -> List[ModuleResource[UTC]]:
        creatures = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTC:
                creatures.append(resource)
        return creatures

    def placeable(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTP]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTP:
                return resource
        return None

    def placeables(
            self
    ) -> List[ModuleResource[UTP]]:
        placeables = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTP:
                placeables.append(resource)
        return placeables

    def door(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTD]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTD:
                return resource
        return None

    def doors(
            self
    ) -> List[ModuleResource[UTD]]:
        doors = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTD:
                doors.append(resource)
        return doors

    def item(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTI]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTI:
                return resource
        return None

    def items(
            self
    ) -> List[ModuleResource[UTI]]:
        doors = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTD:
                doors.append(resource)
        return doors

    def encounter(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTE]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTE:
                return resource
        return None

    def encounters(
            self
    ) -> List[ModuleResource[UTE]]:
        encounters = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTE:
                encounters.append(resource)
        return encounters

    def store(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTM]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTM:
                return resource
        return None

    def stores(
            self
    ) -> List[ModuleResource[UTM]]:
        stores = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTM:
                stores.append(resource)
        return stores

    def trigger(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTT]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTT:
                return resource
        return None

    def triggers(
            self
    ) -> List[ModuleResource[UTT]]:
        triggers = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTT:
                triggers.append(resource)
        return triggers

    def waypoint(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTW]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTW:
                return resource
        return None

    def waypoints(
            self
    ) -> List[ModuleResource[UTW]]:
        waypoints = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTW:
                waypoints.append(resource)
        return waypoints

    def model(
            self,
            resname: str
    ) -> Optional[ModuleResource[MDL]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.MDL:
                return resource
        return None

    def model_ext(
            self,
            resname: str
    ) -> Optional[ModuleResource]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.MDX:
                return resource
        return None

    def models(
            self
    ) -> List[ModuleResource[MDL]]:
        models = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.MDL:
                models.append(resource)
        return models

    def texture(
            self,
            resname: str
    ) -> Optional[ModuleResource[TPC]]:
        for resource in self.resources.values():
            if resname.lower() == resource.resname().lower() and resource.restype() in [ResourceType.TPC, ResourceType.TGA]:
                return resource
        return None

    def textures(
            self
    ) -> List[ModuleResource[MDL]]:
        textures = []
        for resource in self.resources.values():
            if resource.restype() in [ResourceType.TPC, ResourceType.TGA]:
                textures.append(resource)
        return textures

    def sound(
            self,
            resname: str
    ) -> Optional[ModuleResource[UTS]]:
        for resource in self.resources.values():
            if resname == resource.resname() and resource.restype() == ResourceType.UTS:
                return resource
        return None

    def sounds(
            self
    ) -> List[ModuleResource[UTS]]:
        sounds = []
        for resource in self.resources.values():
            if resource.restype() == ResourceType.UTS:
                sounds.append(resource)
        return sounds


class ModuleResource(Generic[T]):
    def __init__(
            self,
            resname: str,
            restype: ResourceType,
            installation: Installation
    ):
        self._resname: str = resname
        self._installation = installation
        self._restype: ResourceType = restype
        self._active: Optional[str] = None
        self._resource: Any = None
        self._locations: List[str] = []

    def resname(
            self
    ) -> str:
        """
        Returns the resource name.

        Returns:
            The resource name.
        """
        return self._resname

    def restype(
            self
    ) -> ResourceType:
        """
        Returns the type of resource stored.

        Returns:
            The resource type.
        """
        return self._restype

    def localized_name(
            self
    ) -> Optional[str]:
        res = self.resource()
        if res is None:
            return None
        elif isinstance(res, UTC):
            return self._installation.string(res.first_name) + " " + self._installation.string(res.last_name)
        elif isinstance(res, UTP):
            return self._installation.string(res.name)
        elif isinstance(res, UTD):
            return self._installation.string(res.name)
        elif isinstance(res, UTW):
            return self._installation.string(res.name)
        elif isinstance(res, UTT):
            return self._installation.string(res.name)
        elif isinstance(res, UTE):
            return self._installation.string(res.name)
        elif isinstance(res, UTM):
            return self._installation.string(res.name)
        elif isinstance(res, UTS):
            return self._installation.string(res.name)
        else:
            return None

    def data(
            self
    ) -> bytes:
        """
        Opens the file at the active location and returns the data.

        Raises:
            ValueError: If no file is active.

        Returns:
            The bytes data of the active file.
        """

        if self._active is None:
            raise ValueError("No file is currently active for resource '{}.{}'.".format(self.resname, self._restype.extension))
        elif self._active.endswith(".erf") or self._active.endswith(".mod") or self._active.endswith(".rim"):
            capsule = Capsule(self._active)
            return capsule.resource(self._resname, self._restype)
        elif self._active.endswith("bif"):
            return self._installation.resource(self._resname, self._restype, [SearchLocation.CHITIN]).data
        else:
            return BinaryReader.load_file(self._active)

    def resource(
            self
    ) -> Optional[T]:
        """
        Returns the cached resource object. If no object has been cached, then it will load the object.

        Returns:
            The resource object.
        """

        if self._resource is None:
            conversions = {
                ResourceType.UTC: (lambda data: read_utc(data)),
                ResourceType.UTP: (lambda data: read_utp(data)),
                ResourceType.UTD: (lambda data: read_utd(data)),
                ResourceType.UTI: (lambda data: read_uti(data)),
                ResourceType.UTM: (lambda data: read_utm(data)),
                ResourceType.UTE: (lambda data: read_ute(data)),
                ResourceType.UTT: (lambda data: read_utt(data)),
                ResourceType.UTW: (lambda data: read_utw(data)),
                ResourceType.UTS: (lambda data: read_uts(data)),
                ResourceType.DLG: (lambda data: read_dlg(data)),
                ResourceType.PTH: (lambda data: read_pth(data)),
                ResourceType.NCS: (lambda data: data),
                ResourceType.TPC: (lambda data: read_tpc(data)),
                ResourceType.TGA: (lambda data: read_tpc(data)),
                ResourceType.LYT: (lambda data: read_lyt(data)),
                ResourceType.VIS: (lambda data: read_vis(data)),
                ResourceType.IFO: (lambda data: read_ifo(data)),
                ResourceType.ARE: (lambda data: read_are(data)),
                ResourceType.GIT: (lambda data: read_git(data)),
                ResourceType.WOK: (lambda data: read_bwm(data))
            }

            if self._active is None:
                self._resource = None
            elif self._active.endswith(".erf") or self._active.endswith(".mod") or self._active.endswith(".rim"):
                data = Capsule(self._active).resource(self._resname, self._restype)
                self._resource = conversions[self._restype](data)
            elif self._active.endswith("bif"):
                data = self._installation.resource(self._resname, self._restype, [SearchLocation.CHITIN]).data
                self._resource = conversions[self._restype](data)
            else:
                data = BinaryReader.load_file(self._active)
                self._resource = conversions[self._restype](data)

        return self._resource

    def add_locations(
            self,
            filepaths: List[str]
    ) -> None:
        """
        Adds a list of filepaths to the list of locations stored for the resource. If a filepath already exists, it is
        ignored.

        Args:
            filepaths: A list of filepaths pointing to a location for the resource.
        """
        self._locations.extend([filepath for filepath in filepaths if filepath not in self._locations])
        if self._active is None and self._locations:
            self.activate(self._locations[0])

    def locations(
            self,
    ) -> List[str]:
        return self._locations

    def activate(
            self,
            filepath: str = None
    ) -> None:
        """
        Sets the active file to the specified path. Calling this method will reset the loaded resource.

        Raises:
            ValueError: If the filepath is not stored in the resource list of locations.

        Args:
            filepath: The new active file.
        """
        self._resource = None
        if filepath is None:
            self._active = self._locations[0] if len(self._locations) > 0 else None
        elif filepath in self._locations:
            self._active = filepath
        else:
            raise ValueError("The filepath '{}' is not being tracked as a location for the resource.".format(self._active))

    def unload(
            self
    ) -> None:
        """
        Clears the cached resource object from memory.
        """
        self._resource = None

    def reload(
            self
    ) -> None:
        """
        Reloads the resource object from the active location.
        """
        self._resource = None
        self.resource()

    def active(
            self
    ) -> Optional[str]:
        """
        Returns the filepath of the currently active file for the resource.

        Returns:
            Filepath to the active resource.
        """
        return self._active

    def save(
            self
    ) -> None:
        conversions = {
            ResourceType.UTC: (lambda res: bytes_utc(res)),
            ResourceType.UTP: (lambda res: bytes_utp(res)),
            ResourceType.UTD: (lambda res: bytes_utd(res)),
            ResourceType.UTI: (lambda res: bytes_uti(res)),
            ResourceType.UTM: (lambda res: bytes_utm(res)),
            ResourceType.UTE: (lambda res: bytes_ute(res)),
            ResourceType.UTT: (lambda res: bytes_utt(res)),
            ResourceType.UTW: (lambda res: bytes_utw(res)),
            ResourceType.UTS: (lambda res: bytes_uts(res)),
            ResourceType.DLG: (lambda res: bytes_dlg(res)),
            ResourceType.PTH: (lambda res: bytes_pth(res)),
            ResourceType.NCS: (lambda res: res),
            ResourceType.TPC: (lambda res: bytes_tpc(res)),
            ResourceType.TGA: (lambda res: bytes_tpc(res)),
            ResourceType.LYT: (lambda res: bytes_lyt(res)),
            ResourceType.VIS: (lambda res: bytes_vis(res)),
            ResourceType.IFO: (lambda res: bytes_ifo(res)),
            ResourceType.ARE: (lambda res: bytes_are(res)),
            ResourceType.GIT: (lambda res: bytes_git(res)),
            ResourceType.WOK: (lambda res: bytes_bwm(res))
        }

        if self._active is None:
            raise ValueError("No active file selected for resource '{}.{}'".format(self._resname, self._restype.extension))
        elif self._active.endswith(".erf") or self._active.endswith(".mod"):
            erf = read_erf(self._active)
            erf.erf_type = ERFType.ERF if self._active.endswith(".erf") else ERFType.MOD
            erf.set(self._resname, self._restype, conversions[self._restype](self.resource()))
            write_erf(erf, self._active)
        elif self._active.endswith(".rim"):
            rim = read_rim(self._active)
            rim.set(self._resname, self._restype, conversions[self._restype](self.resource()))
            write_rim(rim, self._active)
        elif self._active.endswith("bif"):
            raise ValueError("Cannot save file to BIF.")
        else:
            BinaryWriter.dump(self._active, conversions[self._restype](self.resource()))
