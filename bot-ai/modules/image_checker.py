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

class _ImageCheckerState:
    def __init__(self):
        self.screenshotmanager = ScreenshotManager()
        num_workers = 4
        self.threadpool = ThreadPool(num_workers)
        self.last_player = None
        self.last_player_count = 0
        self.rotate_key = 'e'

imagecheckstate = None

def get_map_change() -> bool:
    success, current_map = get_server_map()
    if success:
        if current_map != globals.current_map:
            globals.current_map = current_map
            return True
    return False

def player_cycle() -> None:

    time.sleep(0.1) # Short wait to let icons load in

    player_name_img = imagecheckstate.screenshotmanager.capture_box(config.player_name_box)
    player = recognize_text(player_name_img, available_nickname_symbols)

    if not player or len(player) < 3: # Max player name length is 3 so if we read less than 3, the round might have ended
        globals.round_ended = get_map_change()
    elif globals.round_ended:
        globals.round_ended = False

    if globals.round_ended:
        pydirectinput.keyDown('f3')
        time.sleep(1)

    if player == imagecheckstate.last_player:
        imagecheckstate.last_player_count += 1
        if imagecheckstate.last_player_count == 2:
            imagecheckstate.last_player_count = 0
            # Go other way
            if imagecheckstate.rotate_key == 'e':
                imagecheckstate.rotate_key == 'q'
            else:
                imagecheckstate.rotate_key == 'e'
            print(f'Got stuck, rotating other way using key {imagecheckstate.rotatekey}')

    weapon_icon_img = imagecheckstate.screenshotmanager.capture_box(config.weapon_icon_box)
    weapon = recognize_text(imagecheckstate.screenshotmanager.capture_box(config.weapon_name_box))
    
    # Dispatch thread to check player weapons and possibly kick
    imagecheckstate.threadpool.submit_task(check_player_weapons, player, weapon_icon_img, weapon)

    # go to next player
    if not globals.bot_cycle_paused:
        pydirectinput.keyDown(imagecheckstate.rotate_key)
        time.sleep(0.1) # Need a short wait to register key presses
        pydirectinput.keyUp(imagecheckstate.rotate_key)

def check_image_thread() -> None:
    # Setup
    register_hotkey()

    global imagecheckstate
    imagecheckstate = _ImageCheckerState()

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
        #time.sleep(1) # 1 second interval to check if bot can run