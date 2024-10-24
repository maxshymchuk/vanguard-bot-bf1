import time
import globals
import time
import os
import math
import pygetwindow as gw
from PIL import Image
from modules.image_enhancer import enhance_image, enhance_weapon_image
from modules.screen_capture import capture_screen
from modules.recognition import recognize_text, recognize_image
from pynput.mouse import Controller, Button
from difflib import SequenceMatcher

# TODO: Other weapons/vehicle detection, include isMaximized in area calculation

def player_name_area(isMaximized = False) -> tuple[int, int, int, int]:
    width = 0.15 * globals.current_window.width
    height = 0.03 * globals.current_window.height
    x = 0.695 * globals.current_window.width
    y = 0.62 * globals.current_window.height
    return x, y, width, height

def player_weapon_area(isMaximized = False) -> tuple[int, int, int, int]:
    width = 0.072 * globals.current_window.width
    height = 0.028 * globals.current_window.height
    x = 0.658 * globals.current_window.width
    y = 0.76 * globals.current_window.height
    return x, y, width, height

def kill_feed_area(isMaximized = False) -> tuple[int, int, int, int]:
    width = 0.3 * globals.current_window.width
    height = 0.028 * globals.current_window.height
    x = globals.current_window.left + globals.current_window.width - width
    y = globals.current_window.top + (10 if isMaximized else 40) # remove window title bar, maybe possible get right size from globals.current_window
    return x, y, width, height

def save_log(screenshot, mask, players) -> None:
    postfix = f'{math.trunc(time.time())}'
    path = f'{globals.screenshots_path}/screenshot-{postfix}'
    os.makedirs(path)
    Image.fromarray(mask).save(f'{path}/mask.png')
    screenshot.save(f'{path}/screenshot.png')
    with open(f'{path}/text.txt', 'w') as f:
        f.write(' '.join(players))

def check_image() -> None:
    mouse = Controller()
    smg_text = "SMG 08I8 Factory"
    while not globals.threads_stop.is_set():
        with globals.threads_lock:
            if not globals.current_window:
                print(f'Window ({globals.window_title}) not found')
            else:
                try:
                    active_window = gw.getActiveWindow()
                    if not active_window.title == globals.window_title:
                        print(f'Window ({globals.window_title}) must be active')
                    else:
                        player_name_img = capture_screen(*player_name_area(active_window.isMaximized))
                        image_with_text, mask = enhance_image(player_name_img)
                        players = recognize_text(image_with_text)
                        if len(players) > 0:
                            player_weapon_img = capture_screen(*player_weapon_area(active_window.isMaximized))
                            enhanced_weapon_image, weapon_mask = enhance_weapon_image(player_weapon_img)
                            weapon_text = recognize_text(enhanced_weapon_image)

                            #save_log(player_name_img, mask, players)

                            # this is kinda inefficient because we can write a new recognize_text to return a string and not a list but its fine for now
                            separator = ' ' 
                            weapon_string = separator.join(weapon_text) 

                            print(f"Player {players[0]} using weapon {weapon_string}")

                            probability = SequenceMatcher(None, weapon_string, smg_text).ratio()
                            # 0.9 probability is arbitrary right now
                            if(probability > 0.9):
                                print(f"Kick Player {players[0]} for using SMG08! Probability {probability}")
                                save_log(player_weapon_img, weapon_mask, weapon_text)

                        # go to next player
                        mouse.position = (globals.current_window.width * 0.65625, globals.current_window.height * 0.1185)
                        mouse.press(Button.left)
                        mouse.release(Button.left)
                except FileNotFoundError:
                    print('Image not found')
                except Exception as e:
                    print(f'Unexpected error: {e}')
        time.sleep(1) # 1 second interval to check if bot can run