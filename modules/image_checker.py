import time
import pygetwindow as gw
import globals
from PIL import Image
from modules.window_capture import capture_window
from modules.recognition import recognize_text, recognize_image

def check_image():
    while not globals.threads_stop.is_set():
        with globals.threads_lock:
            if globals.current_window:
                if gw.getActiveWindow().title == globals.window_title:
                    x, y, width, height = globals.current_window.left, globals.current_window.top, globals.current_window.width, globals.current_window.height
                    capture_window(x, y, width, height, True)
                    try:
                        image = Image.open(f'{globals.screenshots_path}/window_screenshot.png')
                        recognize_text(image)
                        # recognize_image(image)
                    except:
                        print('Image not found')
                else:
                    print('Window must be active')
            else:
                print('Window not found')
        time.sleep(1) # 1 second interval to check if bot can run