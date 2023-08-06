from typing import Union

from pykotor.common.stream import BinaryReader
from pykotor.resource.formats.vis import VIS, VISAsciiWriter, VISAsciiReader
from pykotor.resource.type import ResourceType


def read_vis(
        source: Union[str, bytes, bytearray, BinaryReader],
        offset: int = 0,
        size: int = None
) -> VIS:
    """
    Returns an VIS instance from the source. The file format (VIS only) is automatically determined before parsing
    the data.

    Args:
        source: The source of the data.
        offset: The byte offset of the file inside the data.
        size: Number of bytes to allowed to read from the stream. If not specified, uses the whole stream.

    Raises:
        FileNotFoundError: If the file could not be found.
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be accessed.
        ValueError: If the file was corrupted or the format could not be determined.

    Returns:
        An VIS instance.
    """
    return VISAsciiReader(source, offset, size).load()


def write_vis(
        vis: VIS,
        target: Union[str, bytearray, BinaryReader],
        file_format: ResourceType = ResourceType.VIS
) -> None:
    """
    Writes the VIS data to the target location with the specified format (VIS only).

    Args:
        vis: The VIS file being written.
        target: The location to write the data to.
        file_format: The file format.

    Raises:
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be written to the specified destination.
        ValueError: If the specified format was unsupported.
    """
    if file_format == ResourceType.VIS:
        VISAsciiWriter(vis, target).write()
    else:
        raise ValueError("Unsupported format specified; use VIS.")


def bytes_vis(
        vis: VIS,
        file_format: ResourceType = ResourceType.VIS
) -> bytes:
    """
    Returns the VIS data in the specified format (VIS only) as a bytes object.

    This is a convience method that wraps the write_vis() method.

    Args:
        vis: The target VIS object.
        file_format: The file format.

    Raises:
        ValueError: If the specified format was unsupported.

    Returns:
        The VIS data.
    """
    data = bytearray()
    write_vis(vis, data, file_format)
    return data
