from __future__ import annotations

from typing import TYPE_CHECKING

from PIL.Image import Image

from ._utils import read_image, split_letters, crop_border, monochrome, extract_feature, predict_one

if TYPE_CHECKING:
    from ._typings import ImageSource


MAX_LETTER_WIDTH = 33
MIN_LETTER_WIDTH = 14
MONOCHROME_WEIGHT = 1


def solve(source: Image | ImageSource) -> str | None:
    source = source if isinstance(source, Image) else read_image(source)

    croped_letter_images = map(
        crop_border,
        split_letters(
            monochrome(source, MONOCHROME_WEIGHT),
            max_width=MAX_LETTER_WIDTH,
            min_width=MIN_LETTER_WIDTH,
        ),
    )

    letter_datas = map(extract_feature, croped_letter_images)

    result: list[str] = list()
    for _ in letter_datas:
        predict = predict_one(_)
        if predict is None:
            return None
        result.append(predict)

    return ''.join(result)
