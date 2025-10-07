import time
import globals
import config
import time
import pygetwindow as gw
from helpers import print_on_same_line
from .integration import check_player_weapons
from threading import Lock
import pydirectinput
pydirectinput.FAILSAFE = False
from .threadpool import ThreadPool
from models import Classifier

class _ImageCheckerState:
    def __init__(self, num_workers):
        self.threadpool = ThreadPool(num_workers)
        self.lock = Lock()
        self.classifier = Classifier()

imagecheckstate = None

def player_cycle(active_window: gw.Win32Window) -> None:

    time.sleep(config.rotate_delay) # Can provide short wait to let icons load in

    # Dispatch thread to check player weapons and possibly kick
    imagecheckstate.threadpool.submit_task(check_player_weapons, imagecheckstate.lock, imagecheckstate.classifier, active_window, config.should_save_screenshot)

    # if config.should_save_screenshot:
    #     imagecheckstate.screenshotmanager.new_folder(player)
    #     imagecheckstate.screenshotmanager.save_screenshots([(player_name_img, player), (game_img, 'game')])

    with imagecheckstate.lock:
        if globals.round_ended:
            pydirectinput.keyDown('f5')
            time.sleep(0.05)
            pydirectinput.keyUp('f5')
            time.sleep(1)
            return
        
        # go to next player
        pydirectinput.keyDown(globals.rotate_key)
        time.sleep(0.001) # Need a short wait to register key presses
        pydirectinput.keyUp(globals.rotate_key)

def check_image_thread() -> None:

    global imagecheckstate
    imagecheckstate = _ImageCheckerState(config.rotation_threads)

    while not globals.threads_stop.is_set():
        with globals.threads_lock:
            if not globals.current_window:
                print_on_same_line(f'Window ({config.window_title}) not active')
            else:
                try:
                    if not globals.bot_cycle_paused:
                        with globals.teams_lock:
                            if globals.player_count_too_low:
                                return
                            player_cycle(globals.current_window)
                except FileNotFoundError:
                    print('Image not found')
                except Exception as e:
                    print(f'Unexpected error: {e}')
        #time.sleep(1) # 1 second interval to check if bot can run