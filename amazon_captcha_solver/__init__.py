"""
## usage:
```python
from amazon_captcha_solver import solve

# file path
predict = solve('captcha.png')

# file object
with open('captcha.png', 'rb') as fp:
    predict = solve(fp)

# pillow image
predict = solve(Image.open('captcha.png'))

# playwright screenshot-bytes
captcha_image_div = page.locator('css=form[action="/errors/validateCaptcha"] div.a-text-center')
predict = solve(captcha_image_div.screenshot())
```
"""

from ._resources import LETTERS
from ._solver import solve
from ._utils import read_image


__all__ = [
    'solve',
    'read_image',
]
