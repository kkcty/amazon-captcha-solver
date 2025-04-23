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

    :return: Recognized text if successful, None if any character cannot be recognized
    :rtype: str | None
    """
    source = source if isinstance(source, Image) else read_image(source)

    # Convert to monochrome -> split into letters -> crop letter borders
    croped_letter_images = map(
        crop_border,
        split_letters(
            monochrome(source, MONOCHROME_WEIGHT),
            max_width=MAX_LETTER_WIDTH,
            min_width=MIN_LETTER_WIDTH,
        ),
    )

    # Extract features from each letter image
    letter_features = map(extract_feature, croped_letter_images)

    # Match features against known patterns for all letters
    result: list[str] = list()
    for _ in letter_features:
        predict = predict_one(_)

        # Return None if any letter fails to match
        if predict is None:
            return None

        result.append(predict)

    return ''.join(result)
