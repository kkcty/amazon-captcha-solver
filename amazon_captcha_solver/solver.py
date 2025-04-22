from __future__ import annotations

from typing import TYPE_CHECKING, cast

from PIL.Image import Image

from ._resources import TRAINING_DATA
from .utils import (
    read_image,
    split_letters,
    crop_border,
    monochrome,
    extract_data,
)

if TYPE_CHECKING:
    from .type_hints import ImageSource


class AmazonCaptchaSolver:
    def __init__(
        self,
        source: Image | ImageSource,
        /,
        *,
        max_letter_width: int = 33,
        min_letter_width: int = 14,
        monochrome_weight: int = 1,
    ) -> None:
        if isinstance(source, Image):
            self.__origin_image = source
        else:
            self.__origin_image = read_image(source)

        # NOTICE: Not support other args yet.
        # self.__max_width = max_letter_width
        # self.__min_width = min_letter_width
        # self.__mono_weight = monochrome_weight

        self.__max_width = 33
        self.__min_width = 14
        self.__mono_weight = 1

    def solve(self) -> str | None:
        croped_letter_images = map(
            crop_border,
            split_letters(
                monochrome(self.__origin_image, self.__mono_weight),
                max_width=self.__max_width,
                min_width=self.__min_width,
            ),
        )

        letter_datas = map(extract_data, croped_letter_images)

        result: list[str] = list()
        for _ in letter_datas:
            predict = self.__predict_one(_)
            if predict is None:
                return None
            result.append(predict)

        return ''.join(result)

    def __predict_one(self, img_data: str) -> str | None:
        for k, v in TRAINING_DATA.items():
            v = cast(set[str], v)
            if img_data in v:
                return k

        return None
