import time
import globals
import config
import time
import os
import math
import pygetwindow as gw
from pynput.mouse import Controller, Button
from PIL import Image, ImageGrab
from .integration import find_and_kick_player
from .image_enhancer import enhance_image, enhance_weapon_image
from .screen_capture import capture_screen
from .recognition import recognize_text, recognize_image
from .utils import available_nickname_symbols, available_weapon_symbols, get_string_similarity

# TODO: Other weapons/vehicle detection, include isMaximized in area calculation

# def kill_feed_box(isMaximized = False) -> Box:
#     width = 0.3 * globals.current_window.width
#     height = 0.028 * globals.current_window.height
#     x = globals.current_window.left + globals.current_window.width - width
#     y = globals.current_window.top + (10 if isMaximized else 40) # remove window title bar, maybe possible get right size from globals.current_window
#     return Box(x, y, width, height)

def save_log(screenshot, mask, players) -> None:
    postfix = f'{math.trunc(time.time())}'
    path = f'{config.screenshots_path}/screenshot-{postfix}'
    os.makedirs(path)
    Image.fromarray(mask).save(f'{path}/mask.png')
    screenshot.save(f'{path}/screenshot.png')
    if players:
        with open(f'{path}/text.txt', 'w') as f:
            f.write(players)

def save_img(screenshot, weapon, path):
    screenshot.save(f'{path}/{weapon}-{math.trunc(time.time())}.png')

def save_weapon_and_player(player_name_img, player_mask, player, weapon_img, weapon_mask, weapon):
    postfix = f'{math.trunc(time.time())}'
    path = f'{config.screenshots_path}/screenshot-{postfix}'
    os.makedirs(path)
    Image.fromarray(player_mask).save(f'{path}/player_mask.png')
    Image.fromarray(weapon_mask).save(f'{path}/weapon_mask.png')
    player_name_img.save(f'{path}/player_name.png')
    weapon_img.save(f'{path}/weapon.png')
    if player or weapon:
        with open(f'{path}/text.txt', 'w') as f:
            if player:
                f.write(player)
            if weapon:
                f.write('\n' + weapon)

mouse = Controller()

def check_image(active_window) -> None:
    player_name_img = capture_screen(config.player_name_box.x, config.player_name_box.y, config.player_name_box.width, config.player_name_box.height)
    enhanced_player_image, player_mask = enhance_image(player_name_img)
    player = recognize_text(enhanced_player_image, available_nickname_symbols)

    player_weapon_img = capture_screen(config.weapon_name_box.x, config.weapon_name_box.y, config.weapon_name_box.width, config.weapon_name_box.height)
    enhanced_weapon_image, weapon_mask = enhance_weapon_image(player_weapon_img)
    weapon = recognize_text(enhanced_weapon_image, available_weapon_symbols)

    # player_weapon_icon = ImageGrab.grab(bbox = (1230, 740, 1367, 835)) TEMP VALUES FOR TRAINING IMAGE COLLECTING
    # save_weapon_and_player(player_name_img, player_mask, player, player_weapon_img, weapon_mask, weapon)

    if player and weapon:
        print(f"Player {player} using weapon {weapon}")
        for banned_weapon in config.banned_weapons.keys():
            probability = get_string_similarity(weapon, banned_weapon)
            if probability >= config.weapon_text_similarity_probability:
                print(f'Kick Player {player} for using {config.banned_weapons[banned_weapon]}! Probability {probability}')
                save_weapon_and_player(player_name_img, player_mask, player, player_weapon_img, weapon_mask, weapon)
                find_and_kick_player(player, f'No {config.banned_weapons[banned_weapon]}, Read Rules')
                break

    # go to next player
    mouse.position = config.change_player_button_coordinate.x, config.change_player_button_coordinate.y
    mouse.press(Button.left)
    mouse.release(Button.left)

def check_image_thread() -> None:
    while not globals.threads_stop.is_set():
        with globals.threads_lock:
            if not globals.current_window:
                print(f'Window ({config.window_title}) not found')
            else:
                try:
                    active_window = gw.getActiveWindow()
                    if not active_window.title == config.window_title:
                        print(f'Window ({config.window_title}) must be active')
                    else:
                        check_image(active_window)
                except FileNotFoundError:
                    print('Image not found')
                except Exception as e:
                    print(f'Unexpected error: {e}')
        time.sleep(1) # 1 second interval to check if bot can run