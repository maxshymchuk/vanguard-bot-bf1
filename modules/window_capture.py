import globals
from PIL import ImageGrab

def capture_window(x, y, width, height, save_to_disk = False):
    screenshot = ImageGrab.grab(bbox = (x, y, x + width, y + height))
    if save_to_disk:
        screenshot.save(f'{globals.screenshots_path}/window_screenshot.png')
    return screenshot