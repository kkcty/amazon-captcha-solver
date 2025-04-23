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
    """Solve Amazon captcha and return the recognized text.

    :param source: Image source to process. Can be either:
        - PIL.Image.Image object
        - File path (str/Path)
        - Bytes data (bytes)
        - File-like object
    :type source: Image | ImageSource

    :return: Recognized text in uppercase if successful, None if any character cannot be recognized
    :rtype: str | None

    Processing steps:
    1. Convert input to PIL Image if not already
    2. Binarize image using monochrome conversion
    3. Split image into individual letter regions
    4. Crop borders from each letter image
    5. Extract features from processed letters
    6. Predict each letter using extracted features
    7. Return concatenated result if all letters recognized
    """
    source = source if isinstance(source, Image) else read_image(source)

    # 图片二值化 -> 切分出各个字母 -> 裁剪掉各个字母的边框
    croped_letter_images = map(
        crop_border,
        split_letters(
            monochrome(source, MONOCHROME_WEIGHT),
            max_width=MAX_LETTER_WIDTH,
            min_width=MIN_LETTER_WIDTH,
        ),
    )

    # 提取每个字母的特征
    letter_features = map(extract_feature, croped_letter_images)

    # 依次匹配所有字母的特征
    result: list[str] = list()
    for _ in letter_features:
        predict = predict_one(_)

        # 但凡出现一个无法匹配的字母就返回 None
        if predict is None:
            return None

        result.append(predict)

    return ''.join(result)
