import time
import globals
import config
import time
import os
import math
import pygetwindow as gw
from PIL import Image
from helpers import print_on_same_line
from .integration import check_player_weapons, find_and_kick_player, get_server_map
from .image_enhancer import enhance_image, enhance_weapon_image
from .screenshot import ScreenshotManager
from .recognition import recognize_text
from .interaction_listeners import register_hotkey, mouse_click_on
from .utils import available_nickname_symbols, available_weapon_symbols, common_symbols, string_is_similar_to
import pydirectinput
from .threadpool import ThreadPool

screenshotmanager = None
threadpool = None

def get_map_change() -> bool:
    success, current_map = get_server_map()
    if success:
        if current_map != globals.current_map:
            globals.current_map = current_map
            return True
    return False

def player_cycle() -> None:

    time.sleep(0.1) # Short wait to let icons load in

    player_name_img = screenshotmanager.capture_box(config.player_name_box)
    player = recognize_text(player_name_img, available_nickname_symbols)

    if player:
        weapon_icon_img = screenshotmanager.capture_box(config.weapon_icon_box)
        weapon = recognize_text(screenshotmanager.capture_box(config.weapon_name_box))
        # Dispatch thread to check player weapons and possibly kick
        threadpool.submit_task(check_player_weapons, player, weapon_icon_img, weapon)

    # go to next player
    if not globals.bot_cycle_paused:
        pydirectinput.keyDown('e')
        time.sleep(0.1) # Need a short wait to register key presses
        pydirectinput.keyUp('e')

def check_image_thread() -> None:
    # Setup
    register_hotkey()
    global screenshotmanager
    screenshotmanager = ScreenshotManager()

    # Create Thread Pool
    num_workers = 4
    global threadpool
    threadpool = ThreadPool(num_workers)

    while not globals.threads_stop.is_set():
        with globals.threads_lock:
            if not globals.current_window:
                print_on_same_line(f'Window ({config.window_title}) not found')
            else:
                try:
                    active_window = gw.getActiveWindow()
                    if active_window and not active_window.title == config.window_title:
                        print_on_same_line(f'Window ({config.window_title}) must be active')
                        time.sleep(1)
                    else:
                        player_cycle()
                except FileNotFoundError:
                    print('Image not found')
                except Exception as e:
                    print(f'Unexpected error: {e}')
        time.sleep(1) # 1 second interval to check if bot can run