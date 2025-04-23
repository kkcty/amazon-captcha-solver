# Amazon captcha Solver
forked from [a-maliarov/amazoncaptcha](https://github.com/a-maliarov/amazoncaptcha), 
change python version to 3.13+.

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