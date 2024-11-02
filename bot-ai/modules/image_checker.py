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
from .screen_capture import capture_screen
from .recognition import recognize_text
from .interaction_listeners import listen_keyboard_key_press, mouse_click_on
from .utils import available_nickname_symbols, available_weapon_symbols, common_symbols, string_is_similar_to

def save_weapon_and_player(player_name_img, player_mask, player, weapon_img, weapon_mask, weapon, weapon_icon_img, prediction, probability, spectator_text_img):
    postfix = f'{math.trunc(time.time())}-{weapon}'
    path = f'{config.screenshots_path}/screenshot-{postfix}'
    os.makedirs(path)
    Image.fromarray(player_mask).save(f'{path}/player_mask.png')
    Image.fromarray(weapon_mask).save(f'{path}/weapon_mask.png')
    player_name_img.save(f'{path}/player_name.png')
    weapon_img.save(f'{path}/weapon.png')
    weapon_icon_img.save(f'{path}/weapon_icon.png')
    Image.fromarray(spectator_text_img).save(f'{path}/spectator_text.png')
    if player or weapon:
        with open(f'{path}/text.txt', 'w') as f:
            f.write(f'Prediction: ' + str(prediction) + ' with probability ' + str(probability) + '\n')
            if player:
                f.write(player)
            if weapon:
                f.write('\n' + weapon)

def get_map_change() -> bool:
    success, current_map = get_server_map()
    if success:
        if current_map != globals.current_map:
            globals.current_map = current_map
            return True
    return False

def check_image(active_window) -> None:
    time.sleep(0.05) # Let everything load in

    spectator_text_image = capture_screen(config.spectator_text_box.x, config.spectator_text_box.y, config.spectator_text_box.width, config.spectator_text_box.height)
    enhanced_spectator_text_image, spec_mask = enhance_weapon_image(spectator_text_image)
    spectator_text = recognize_text(enhanced_spectator_text_image, available_symbols=common_symbols)

    if not spectator_text or (not string_is_similar_to(spectator_text, "SPECTATOR", 0.7) and not string_is_similar_to(spectator_text, "KILLED BY", 0.7)):
        print("no spectator text")
        if get_map_change():
            print('Round ended')
            globals.round_ended = True
    elif globals.round_ended:
            print('Round started again')
            globals.round_ended = False

    if globals.round_ended and not globals.bot_cycle_paused:
        mouse_click_on(config.player_view_button_coordinate.x, config.player_view_button_coordinate.y)
        time.sleep(1)
        mouse_click_on(config.third_person_view_button_coordinate.x, config.third_person_view_button_coordinate.y)
        return

    player_name_img = capture_screen(config.player_name_box.x, config.player_name_box.y, config.player_name_box.width, config.player_name_box.height)
    enhanced_player_image, player_mask = enhance_image(player_name_img)
    player = recognize_text(enhanced_player_image, available_symbols=available_nickname_symbols)

    weapon_img = capture_screen(config.weapon_name_box.x, config.weapon_name_box.y, config.weapon_name_box.width, config.weapon_name_box.height)
    enhanced_weapon_image, weapon_mask = enhance_weapon_image(weapon_img)
    weapon = recognize_text(enhanced_weapon_image, available_symbols=available_weapon_symbols)

    weapon_icon_img = capture_screen(config.weapon_icon_box.x, config.weapon_icon_box.y, config.weapon_icon_box.width, config.weapon_icon_box.height)

    # TODO: Save probabilities too?


    if player:
        if globals.round_ended:
            globals.round_ended = False

        isBanned, bannedWeapon, prediction, probability = check_player_weapons(weapon_icon_img, weapon)
        #print(f'Player {player} using weapon {weapon} in category {prediction} with probability {str(probability)}')
        if isBanned:
            find_and_kick_player(player, f'No {bannedWeapon}, Read Rules')
            if config.should_save_screenshot:
                save_weapon_and_player(player_name_img, player_mask, player, weapon_img, weapon_mask, weapon, weapon_icon_img, prediction, probability, spec_mask)

    # go to next player
    if not globals.bot_cycle_paused:
        mouse_click_on(config.change_player_button_coordinate.x, config.change_player_button_coordinate.y)

def check_image_thread() -> None:
    listen_keyboard_key_press()
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
                        check_image(active_window)
                except FileNotFoundError:
                    print('Image not found')
                except Exception as e:
                    print(f'Unexpected error: {e}')
        # time.sleep(1) # 1 second interval to check if bot can run