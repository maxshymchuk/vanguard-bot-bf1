import time
import globals
import config
import time
import os
import math
import pygetwindow as gw
from pynput.mouse import Controller, Button
from PIL import Image, ImageGrab
from .integration import check_player_weapons, find_and_kick_player, get_server_map
from .image_enhancer import enhance_image, enhance_weapon_image
from .screen_capture import capture_screen
from .recognition import recognize_text
from .utils import available_nickname_symbols, available_weapon_symbols
import asyncio

def save_weapon_and_player(player_name_img, player_mask, player, weapon_img, weapon_mask, weapon, weapon_icon_img, prediction, probability):
    postfix = f'{math.trunc(time.time())}-{weapon}'
    path = f'{config.screenshots_path}/screenshot-{postfix}'
    os.makedirs(path)
    Image.fromarray(player_mask).save(f'{path}/player_mask.png')
    Image.fromarray(weapon_mask).save(f'{path}/weapon_mask.png')
    player_name_img.save(f'{path}/player_name.png')
    weapon_img.save(f'{path}/weapon.png')
    weapon_icon_img.save(f'{path}/weapon_icon.png')
    if player or weapon:
        with open(f'{path}/text.txt', 'w') as f:
            f.write(f'Prediction: ' + str(prediction) + ' with probability ' + str(probability) + '\n')
            if player:
                f.write(player)
            if weapon:
                f.write('\n' + weapon)

mouse = Controller()
lock = asyncio.Lock()
loop = asyncio.get_event_loop()

async def check_round_ended():
    async with lock:
        success, current_map = get_server_map()
        if success:
            if current_map != globals.current_map:
                globals.current_map = current_map
                globals.round_ended = True
    

def check_image(active_window) -> None:
    player_name_img = capture_screen(config.player_name_box.x, config.player_name_box.y, config.player_name_box.width, config.player_name_box.height)
    enhanced_player_image, player_mask = enhance_image(player_name_img)
    player = recognize_text(enhanced_player_image, available_symbols=available_nickname_symbols)

    weapon_img = capture_screen(config.weapon_name_box.x, config.weapon_name_box.y, config.weapon_name_box.width, config.weapon_name_box.height)
    enhanced_weapon_image, weapon_mask = enhance_weapon_image(weapon_img)
    weapon = recognize_text(enhanced_weapon_image, available_symbols=available_weapon_symbols)

    weapon_icon_img = capture_screen(config.weapon_icon_box.x, config.weapon_icon_box.y, config.weapon_icon_box.width, config.weapon_icon_box.height)

    # TODO: Save probabilities too?
    if config.should_save_screenshot:
            save_weapon_and_player(player_name_img, player_mask, player, weapon_img, weapon_mask, weapon, weapon_icon_img, '', 0)

    mouse.position = config.change_player_button_coordinate.x, config.change_player_button_coordinate.y

    if player:
        if globals.round_ended:
            globals.round_ended = False

        isBanned, bannedWeapon, prediction, probability = check_player_weapons(weapon_icon_img, weapon)
        print(f'Player {player} using weapon {weapon} in category {prediction} with probability {str(probability)}')
        if isBanned:
            find_and_kick_player(player, f'No {bannedWeapon}, Read Rules')
    else:
        if not globals.round_ended:
            asyncio.run_coroutine_threadsafe(check_round_ended(), loop)
        else:
            mouse.position = config.third_person_view_button_coordinate.x, config.third_person_view_button_coordinate.y

    # go to next player
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
                    if active_window and not active_window.title == config.window_title:
                        print(f'Window ({config.window_title}) must be active')
                    else:
                        check_image(active_window)
                except FileNotFoundError:
                    print('Image not found')
                except Exception as e:
                    print(f'Unexpected error: {e}')
        time.sleep(1) # 1 second interval to check if bot can run