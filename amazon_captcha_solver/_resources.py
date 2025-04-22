from __future__ import annotations

from importlib.resources import read_text
from json import loads
from typing import cast

from .type_hints import TrainingDataType


SUPPORT_LETTERS = (
    'A',
    'B',
    'C',
    'E',
    'F',
    'G',
    'H',
    'J',
    'K',
    'L',
    'M',
    'N',
    'P',
    'R',
    'T',
    'U',
    'X',
    'Y',
)

TRAINING_DATA = cast(
    TrainingDataType,
    {
        _: set(loads(read_text('amazon_captcha_solver.training_data', f'{_}.json', encoding='utf-8')))
        for _ in SUPPORT_LETTERS
    },
)
