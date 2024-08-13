"""
Record Mouse and Keyboard Movements into TXT file - Python
log of actions in a txt file to be then read and reproduced by pyautogui.

pip install pynput

@since 2024年1月25日 21:29:50
"""

from pynput import mouse
import logging

logging.basicConfig(filename="mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_move(x, y):
    # print('Pointer moved to {0}'.format((x, y)))
    if x < 15 or y < 15:
        # Stop listener
        # Call pynput.mouse.Listener.stop from anywhere, raise StopException or return False from a callback to stop the listener.
        return False

def on_click(x, y, button, pressed):
    # Button.left Released at (2587, 489)
    print('{0} {1} at {2} '.format(button, 'Pressed' if pressed else 'Released', (x, y)))
    if pressed:
        logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

# Collect events until released
# A mouse listener is a threading.Thread, and all callbacks will be invoked from the thread.
with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    listener.join()

