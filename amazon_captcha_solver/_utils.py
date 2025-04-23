from __future__ import annotations

import zlib
from io import BytesIO, RawIOBase, BufferedIOBase
from pathlib import Path
from typing import TYPE_CHECKING, overload

from PIL import Image as ImageModule, ImageChops

from ._resources import TRAINING_DATA

if TYPE_CHECKING:
    from typing import Iterable

    from ._typings import StrPath, BinaryIO, ImageSource

    type Image = ImageModule.Image


@overload
def read_image(s: StrPath, /, *, formats: list[str] | None = None) -> Image: ...
@overload
def read_image(s: BinaryIO, /, *, formats: list[str] | None = None) -> Image: ...
@overload
def read_image(s: bytes, /, *, formats: list[str] | None = None) -> Image: ...
def read_image(s: ImageSource, /, *, formats: list[str] | None = None) -> Image:
    """Read image from file, bytes or binary-io."""
    # TODO: support image-base64 in future.

    # file-path
    if isinstance(s, (str, Path)):
        if isinstance(s, str):
            s = Path(s)
        if not s.exists():
            raise FileNotFoundError(f'"{s}" not exist.')
        if not s.is_file():
            raise IOError(f'"{s}" is not a file.')
        return ImageModule.open(s, formats=formats)

    # binary-io
    if isinstance(s, (RawIOBase, BufferedIOBase)):
        return ImageModule.open(s)  # type: ignore

    # bytes
    return ImageModule.open(BytesIO(s), formats=formats)


def monochrome(img: Image, weight: int, /) -> Image:
    """Convert image to monochrome using thresholding."""
    return ImageModule.eval(
        img.convert('L'),
        lambda p: 0 if p <= weight else 255,
    )


def merge_horizontally(img1: Image, img2: Image, /) -> Image:
    """Merge two images side by side horizontally."""
    r = ImageModule.new('L', (img1.width + img2.width, img1.height))
    r.paste(img1, (0, 0))
    r.paste(img2, (img1.width, 0))
    return r


def split_letters(img: Image, /, max_width: int, min_width: int) -> Iterable[Image]:
    """Split captcha image into individual letter images."""
    columns = [[(img.getpixel((x, y))) for y in range(img.height)] for x in range(img.width)]
    column_flags = [0 not in _ for _ in columns]
    x_points = [i for i, f in enumerate(column_flags) if not f]
    x_borders = [_ for _ in x_points if _ - 1 not in x_points or _ + 1 not in x_points]
    if len(x_borders) % 2 != 0:
        x_borders.insert(1, x_borders[0])

    border_pairs: list[tuple[int, int]] = list()
    for a, b in zip(x_borders[0::2], x_borders[1::2]):
        start = a
        end = min(b + 1, img.width - 1)

        if end - start <= max_width:
            border_pairs.append((start, end))
        else:
            two_letter = {k: v.count(0) for k, v in enumerate(columns[start + 5 : end - 5])}
            divider = min(two_letter, key=two_letter.get) + 5  # type: ignore
            border_pairs.extend(
                [
                    (start, start + divider),
                    (start + divider + 1, end),
                ]
            )

    letter_imgs = [img.crop((_[0], 0, _[1], img.height)) for _ in border_pairs]

    if (
        len(letter_imgs) != 6
        and len(letter_imgs) != 7
        or (len(letter_imgs) == 6 and letter_imgs[0].width < min_width)
    ):
        return (ImageModule.new('L', (200, 70)) for _ in range(6))

    if len(letter_imgs) == 7:
        letter_imgs[-1] = merge_horizontally(letter_imgs[-1], letter_imgs[0])
        del letter_imgs[0]

    return (_ for _ in letter_imgs)


def crop_border(img: Image, /) -> Image:
    """Remove white borders from letter image."""
    bg = ImageModule.new(img.mode, img.size, 255)
    diff = ImageChops.difference(img, bg)
    return img.crop(diff.getbbox())


def extract_feature(img: Image, /) -> str:
    """Extract compressed feature string from letter image."""
    img_data = ''.join(map(lambda pix: '1' if pix == 0 else '0', img.getdata()))
    return str(zlib.compress(img_data.encode('utf-8')))


def predict_one(feature: str) -> str | None:
    """Predict letter from extracted feature using training data."""
    for letter, features in TRAINING_DATA.items():
        if feature in features:
            return letter

    # no matched feature in training_data
    return None
