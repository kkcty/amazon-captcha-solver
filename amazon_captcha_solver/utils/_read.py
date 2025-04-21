from __future__ import annotations

from io import BytesIO, RawIOBase, BufferedIOBase
from pathlib import Path
from typing import TYPE_CHECKING, overload, cast

from aiofiles import open as async_open
from PIL import Image as ImageModule

if TYPE_CHECKING:
    from typing import Awaitable, Literal

    from ..type_hints import BinaryIO, Image, ImageSource, StrPath


sync_open = open


def check_file_before_read(f: StrPath, /) -> Path:
    if isinstance(f, str):
        f = Path(f)

    if not f.exists():
        raise FileNotFoundError(f'"{f}" not exist')

    if not f.is_file():
        raise IsADirectoryError(f'"{f}" is a directory')

    return f


@overload
async def read_image(
    d: StrPath, async_mode: Literal[True], /, *, formats: list[str] | None = None
) -> Image: ...
@overload
def read_image(d: StrPath, async_mode: Literal[False], /, *, formats: list[str] | None = None) -> Image: ...
@overload
def read_image(d: BinaryIO, async_mode: None = None, /, *, formats: list[str] | None = None) -> Image: ...
@overload
def read_image(d: bytes, async_mode: None = None, /, *, formats: list[str] | None = None) -> Image: ...
def read_image(
    d: ImageSource, async_mode: bool | None = None, /, *, formats: list[str] | None = None
) -> Image | Awaitable[Image]:
    """
    read image from file, bytes or binary-io

    :param d: file-path, bytes or binary-io
    :type d: Path | str | bytes | RawIOBase | BufferedIOBase
    :param async_mode: enable async (file-path only)
    :type async_mode: bool | None
    :param formats: possible image formats
    :type formats: list[str] | None

    :return: Pillow Image
    :rtype: Image | Awaitable[Image]
    """
    # TODO: support image-base64 in future

    # if d is file-path
    if isinstance(d, (str, Path)):
        d = check_file_before_read(d)
        if async_mode is True:
            return read_image_async(d, formats=formats)
        else:
            return ImageModule.open(d, formats=formats)

    # if d is binary-io
    if isinstance(d, (RawIOBase, BufferedIOBase)):
        return ImageModule.open(d)  # type: ignore

    # if d is bytes
    d = cast(bytes, d)
    return ImageModule.open(BytesIO(d), formats=formats)


async def read_image_async(f: StrPath, /, *, formats: list[str] | None = None) -> Image:
    """read image from file (async)"""
    f = check_file_before_read(f)

    async with async_open(f, 'rb') as fp:
        bio = BytesIO(await fp.read())

    return ImageModule.open(bio, formats=formats)
