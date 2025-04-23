from __future__ import annotations

from importlib.resources import read_text
from json import loads


LETTERS = 'ABCEFGHJKLMNPRTUXY'

TRAINING_DATA: dict[str, set[str]] = {
    _: set(loads(read_text('amazon_captcha_solver.training_data', f'{_}.json', encoding='utf-8')))
    for _ in LETTERS
}
