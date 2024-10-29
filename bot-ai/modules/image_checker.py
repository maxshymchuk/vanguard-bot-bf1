import time
import globals
import time
import os
import math
import pygetwindow as gw
from PIL import Image, ImageGrab
from modules.image_enhancer import enhance_image, enhance_weapon_image
from modules.screen_capture import capture_screen
from modules.recognition import recognize_text, recognize_image
from pynput.mouse import Controller, Button, Listener
from queue import Queue
from modules.utils import available_nickname_symbols, available_weapon_symbols, get_string_similarity
from modules.bf1api_integration import find_and_kick_player

# TODO: Other weapons/vehicle detection, include isMaximized in area calculation

def next_player_button_position() -> tuple[int, int]:
    x = globals.current_window.left + 0.65625 * globals.current_window.width
    y = globals.current_window.top + 0.1185 * globals.current_window.height
    return x, y

def player_name_area(isMaximized = False) -> tuple[int, int, int, int]:
    width = 0.15 * globals.current_window.width
    height = 0.03 * globals.current_window.height
    x = globals.current_window.left + 0.695 * globals.current_window.width
    y = globals.current_window.top + 0.62 * globals.current_window.height
    return x, y, width, height

def player_weapon_area(isMaximized = False) -> tuple[int, int, int, int]:
    width = 0.072 * globals.current_window.width
    height = 0.028 * globals.current_window.height
    x = globals.current_window.left + 0.658 * globals.current_window.width
    y = globals.current_window.top + 0.76 * globals.current_window.height
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
    if players:
        with open(f'{path}/text.txt', 'w') as f:
            f.write(players)

def save_img(screenshot, weapon, path):
    screenshot.save(f'{path}/{weapon}-{math.trunc(time.time())}.png')

def save_weapon_and_player(player_name_img, player_mask, player, weapon_img, weapon_mask, weapon):
    postfix = f'{math.trunc(time.time())}'
    path = f'{globals.screenshots_path}/screenshot-{postfix}'
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
    player_name_img = capture_screen(globals.player_name_x, globals.player_name_y, globals.player_name_width, globals.player_name_height)
    enhanced_player_image, player_mask = enhance_image(player_name_img)
    player = recognize_text(enhanced_player_image, available_nickname_symbols)

    player_weapon_img = capture_screen(globals.weapon_name_x, globals.weapon_name_y, globals.weapon_name_width, globals.weapon_name_height)
    enhanced_weapon_image, weapon_mask = enhance_weapon_image(player_weapon_img)
    weapon = recognize_text(enhanced_weapon_image, available_weapon_symbols)

    # player_weapon_icon = ImageGrab.grab(bbox = (1230, 740, 1367, 835)) TEMP VALUES FOR TRAINING IMAGE COLLECTING

    # save_weapon_and_player(player_name_img, player_mask, player, player_weapon_img, weapon_mask, weapon)

    if player and weapon:
        print(f"Player {player} using weapon {weapon}")

        for banned_weapon in globals.banned_weapons.keys():
            probability = get_string_similarity(weapon, banned_weapon)
            if probability >= globals.weaponTextSimilarityProbability:
                print(f"Kick Player {player} for using {globals.banned_weapons[banned_weapon]}! Probability {probability}")
                save_weapon_and_player(player_name_img, player_mask, player, player_weapon_img, weapon_mask, weapon)
                find_and_kick_player(player, f'No {globals.banned_weapons[banned_weapon]}, Read Rules')
                break


    # go to next player
    mouse.position = globals.next_player_button_x, globals.next_player_button_y
    mouse.press(Button.left)
    mouse.release(Button.left)

click_queue = Queue()
def on_click(x, y, button, pressed):
    if pressed:
        click_queue.put((x, y))
        return False

def click_listener(message: str):
    with Listener(on_click=on_click) as listener:
        print(message)
        listener.join()
    return click_queue.get()

def set_areas(area: str):
    x, y = click_listener(f"Click top-left {area} corner")
    right, bottom = click_listener(f"Click bottom-right {area} corner")
    height = abs(bottom) - abs(y) # screen coordinates increase downwards so bottom > top
    width = abs(right) - abs(x) 
    return x, y, width, height

def read_config():
    with open(f'config.txt', 'r') as f:
        lines = f.read().splitlines()
        globals.next_player_button_x, globals.next_player_button_y, \
        globals.player_name_x, globals.player_name_y, globals.player_name_width, globals.player_name_height, \
        globals.weapon_name_x, globals.weapon_name_y, globals.weapon_name_width, globals.weapon_name_height = map(int, lines)
    print('Config read')

def setup_config():
    global next_player_button_x, next_player_button_y, player_name_x, player_name_y, player_name_width, player_name_height, weapon_name_x, weapon_name_y, weapon_name_width, weapon_name_height
    next_player_button_x, next_player_button_y = click_listener("Click next player box")
    player_name_x, player_name_y, player_name_width, player_name_height = set_areas("player name")
    weapon_name_x, weapon_name_y, weapon_name_width, weapon_name_height = set_areas("weapon name")

    with open(f'config.txt', 'w') as f:
        f.write(str(next_player_button_x) + '\n' + str(next_player_button_y) + '\n')
        f.write(str(player_name_x) + '\n' + str(player_name_y) + '\n' + str(player_name_width) + '\n' + str(player_name_height) + '\n')
        f.write(str(weapon_name_x) + '\n' + str(weapon_name_y) + '\n' + str(weapon_name_width) + '\n' + str(weapon_name_height) + '\n')

def check_image_thread() -> None:
    hasReadConfig = False
    shouldReadConfig = False # If this is false we use the defaults set in next_player_button_position etc. In future we can just put these defaults in the config.txt file to begin with
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
                        if shouldReadConfig:
                            if not os.path.isfile('config.txt'):
                                setup_config()
                            else:
                                if not hasReadConfig:
                                    read_config()
                                    hasReadConfig = True
                        else:
                            globals.next_player_button_x, globals.next_player_button_y = next_player_button_position()
                            globals.player_name_x, globals.player_name_y, globals.player_name_width, globals.player_name_height = player_name_area()
                            globals.weapon_name_x, globals.weapon_name_y, globals.weapon_name_width, globals.weapon_name_height = player_weapon_area()

                        check_image(active_window)
                except FileNotFoundError:
                    print('Image not found')
                except Exception as e:
                    print(f'Unexpected error: {e}')
        time.sleep(1) # 1 second interval to check if bot can run