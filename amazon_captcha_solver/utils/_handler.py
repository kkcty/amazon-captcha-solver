from __future__ import annotations

import zlib
from typing import TYPE_CHECKING

from PIL import Image as ImageModule, ImageChops

if TYPE_CHECKING:
    from typing import Iterable

    from ..type_hints import Image


def split_letters(
    img: Image,
    /,
    max_width: int = 33,
    min_width: int = 14,
) -> Iterable[Image]:
    # 从图片中切分出每个字母
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


def merge_horizontally(i1: Image, i2: Image, /) -> Image:
    # 水平合并两张图片
    r = ImageModule.new('L', (i1.width + i2.width, i1.height))
    r.paste(i1, (0, 0))
    r.paste(i2, (i1.width, 0))
    return r


def monochrome(i: Image, weight: int = 1, /) -> Image:
    # 二值化
    return ImageModule.eval(
        i.convert('L'),
        lambda p: 0 if p <= weight else 255,
    )


def crop_border(img: Image, /) -> Image:
    # 边框裁剪
    bg = ImageModule.new(img.mode, img.size, 255)
    diff = ImageChops.difference(img, bg)
    return img.crop(diff.getbbox())


def extract_data(img: Image, /) -> str:
    # 提取图片信息
    img_data = ''.join(map(lambda pix: '1' if pix == 0 else '0', img.getdata()))
    return str(zlib.compress(img_data.encode('utf-8')))
