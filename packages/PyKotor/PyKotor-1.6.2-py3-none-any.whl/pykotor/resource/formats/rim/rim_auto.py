from typing import Union

from pykotor.common.stream import BinaryReader
from pykotor.resource.formats.rim import RIM, RIMBinaryReader, RIMBinaryWriter
from pykotor.resource.type import ResourceType


def read_rim(
        source: Union[str, bytes, bytearray, BinaryReader],
        offset: int = 0,
        size: int = None
) -> RIM:
    """
    Returns an RIM instance from the source. The file format (RIM only) is automatically determined before parsing
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
        An RIM instance.
    """
    return RIMBinaryReader(source, offset, size).load()


def write_rim(
        rim: RIM,
        target: Union[str, bytearray, BinaryReader],
        file_format: ResourceType = ResourceType.RIM
) -> None:
    """
    Writes the RIM data to the target location with the specified format (RIM only).

    Args:
        rim: The RIM file being written.
        target: The location to write the data to.
        file_format: The file format.

    Raises:
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be written to the specified destination.
        ValueError: If the specified format was unsupported.
    """
    if file_format == ResourceType.RIM:
        RIMBinaryWriter(rim, target).write()
    else:
        raise ValueError("Unsupported format specified; use RIM.")


def bytes_rim(
        rim: RIM,
        file_format: ResourceType = ResourceType.RIM
) -> bytes:
    """
    Returns the RIM data in the specified format (RIM only) as a bytes object.

    This is a convience method that wraps the write_rim() method.

    Args:
        rim: The target RIM object.
        file_format: The file format.

    Raises:
        ValueError: If the specified format was unsupported.

    Returns:
        The RIM data.
    """
    data = bytearray()
    write_rim(rim, data, file_format)
    return data
