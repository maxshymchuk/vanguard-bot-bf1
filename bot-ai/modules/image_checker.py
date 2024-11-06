import time
import globals
import config
import time
import pygetwindow as gw
from helpers import print_on_same_line
from .integration import check_player_weapons
from .image_enhancer import enhance_image
from .screenshot import ScreenshotManager, crop_image_array
from .recognition import recognize_text
from .interaction_listeners import register_hotkey
from .utils import available_nickname_symbols
import pydirectinput
from .threadpool import ThreadPool

class _ImageCheckerState:
    def __init__(self):
        self.threadpool = ThreadPool()
        self.screenshotmanager = ScreenshotManager()
        self.last_player = None
        self.same_player_count = 0
        self.no_player_count = 0
        self.rotate_key = 'e'

imagecheckstate = None

def player_cycle(active_window: gw.Win32Window) -> None:

    if not active_window:
        return

    #time.sleep(0.35) # Short wait to let icons load in

    # Todo fix if active_window is none or something stupid
    game_img = imagecheckstate.screenshotmanager.capture(active_window.top, active_window.left, active_window.width, active_window.height)

    player_name_img, _ = enhance_image(crop_image_array(game_img, config.player_name_box))
    player = recognize_text(player_name_img, available_nickname_symbols)

    if not player or len(player) < 3: # Max player name length is 3 so if we read less than 3, the round might have ended
        if not globals.round_ended:
            imagecheckstate.no_player_count += 1
            if imagecheckstate.no_player_count == 2:
                globals.round_ended = True
                imagecheckstate.no_player_count = 0
        else:
            pydirectinput.keyDown('f3')
            time.sleep(1)
            return
    elif globals.round_ended:
        globals.round_ended = False
        imagecheckstate.no_player_count = 0

    if player in globals.kick_list:
        print(f'Player {player} already marked for kicking, skipping')
        return

    if player == imagecheckstate.last_player:
        imagecheckstate.same_player_count += 1
        if imagecheckstate.same_player_count == 2:
            imagecheckstate.same_player_count = 0
            # Go other way
            if imagecheckstate.rotate_key == 'e':
                imagecheckstate.rotate_key == 'q'
            else:
                imagecheckstate.rotate_key == 'e'
            print(f'Got stuck, rotating other way using key {imagecheckstate.rotate_key}')
    
    # Dispatch thread to check player weapons and possibly kick
    imagecheckstate.threadpool.submit_task(check_player_weapons, player, player_name_img, game_img, config.should_save_screenshot)

    # go to next player
    pydirectinput.keyDown(imagecheckstate.rotate_key)
    time.sleep(0.05) # Need a short wait to register key presses
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
                        if not globals.bot_cycle_paused:
                            player_cycle(active_window)
                except FileNotFoundError:
                    print('Image not found')
                # except Exception as e:
                #     print(f'Unexpected error: {e}')
        #time.sleep(1) # 1 second interval to check if bot can run