from __future__ import annotations

from io import BytesIO, RawIOBase, BufferedIOBase
from pathlib import Path
from typing import TYPE_CHECKING, overload, cast

from PIL import Image as ImageModule

if TYPE_CHECKING:
    from ..type_hints import BinaryIO, Image, ImageSource, StrPath


def check_file_before_read(f: StrPath, /) -> Path:
    if isinstance(f, str):
        f = Path(f)

    if not f.exists():
        raise FileNotFoundError(f'"{f}" not exist')

    if not f.is_file():
        raise IsADirectoryError(f'"{f}" is a directory')

    return f


@overload
def read_image(s: StrPath, /, *, formats: list[str] | None = None) -> Image: ...
@overload
def read_image(s: BinaryIO, /, *, formats: list[str] | None = None) -> Image: ...
@overload
def read_image(s: bytes, /, *, formats: list[str] | None = None) -> Image: ...
def read_image(s: ImageSource, /, *, formats: list[str] | None = None) -> Image:
    """
    read image from file, bytes or binary-io

    :param s: file-path, bytes or binary-io
    :type s: Path | str | bytes | RawIOBase | BufferedIOBase
    :param formats: possible image formats
    :type formats: list[str] | None

    :return: Pillow Image
    :rtype: Image
    """
    # TODO: support image-base64 in future.

    # if d is file-path
    if isinstance(s, (str, Path)):
        s = check_file_before_read(s)
        return ImageModule.open(s, formats=formats)

    # if d is binary-io
    if isinstance(s, (RawIOBase, BufferedIOBase)):
        return ImageModule.open(s)  # type: ignore

    # if d is bytes
    s = cast(bytes, s)
    return ImageModule.open(BytesIO(s), formats=formats)
