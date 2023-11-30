
"""
https://pypi.org/project/PyScreeze/

The Locate Functions
You can visually locate something on the screen if you have an image file of it.

"""
import pyscreeze, pyautogui

button7location = pyscreeze.locateOnScreen('calc7key.png')

button7x, button7y = pyscreeze.center(button7location)

# clicks the center of where the 7 button was found
pyautogui.click(button7x, button7y)
