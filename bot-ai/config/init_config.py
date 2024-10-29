import globals
import config
import os
from queue import Queue
from pynput.mouse import Listener
from classes import Box, Coordinate

def next_player_button_coordinate() -> Coordinate:
    x = globals.current_window.left + 0.65625 * globals.current_window.width
    y = globals.current_window.top + 0.1185 * globals.current_window.height
    return Coordinate(x, y)

def player_name_box(isMaximized = False) -> Box:
    width = 0.15 * globals.current_window.width
    height = 0.03 * globals.current_window.height
    x = globals.current_window.left + 0.695 * globals.current_window.width
    y = globals.current_window.top + 0.62 * globals.current_window.height
    return Box(x, y, width, height)

def player_weapon_box(isMaximized = False) -> Box:
    width = 0.072 * globals.current_window.width
    height = 0.028 * globals.current_window.height
    x = globals.current_window.left + 0.658 * globals.current_window.width
    y = globals.current_window.top + 0.76 * globals.current_window.height
    return Box(x, y, width, height)

click_queue = Queue()
def on_click(x, y, button, pressed):
    if pressed:
        click_queue.put((x, y))
        return False

def click_listener(message: str) -> tuple[int, int]:
    with Listener(on_click=on_click) as listener:
        print(message)
        listener.join()
    return click_queue.get()

def set_coordinate(name: str) -> Coordinate:
    x, y = click_listener(name)
    return Coordinate(x, y)

def set_box(name: str) -> Box:
    x, y = click_listener(f'Click top-left {name} corner')
    right, bottom = click_listener(f'Click bottom-right {name} corner')
    height = abs(bottom) - abs(y) # screen coordinates increase downwards so bottom > top
    width = abs(right) - abs(x)
    return Box(x, y, width, height)

def read_config():
    with open(config.config_path, 'r') as f:
        lines = f.read().splitlines()
        next_player_button_x, next_player_button_y, \
        player_name_x, player_name_y, player_name_width, player_name_height, \
        weapon_name_x, weapon_name_y, weapon_name_width, weapon_name_height = map(int, lines)
    config.next_player_button = Coordinate(next_player_button_x, next_player_button_y)
    config.player_name = Box(player_name_x, player_name_y, player_name_width, player_name_height)
    config.weapon_name = Box(weapon_name_x, weapon_name_y, weapon_name_width, weapon_name_height)
    print('Config read')

def setup_config():
    config.next_player_button = set_coordinate('Click next/prev player button box')
    config.player_name = set_box('player name')
    config.weapon_name = set_box('weapon name')
    with open(config.config_path, 'w') as f:
        f.write(str(config.next_player_button.x) + '\n' + str(config.next_player_button.y) + '\n')
        f.write(str(config.player_name.x) + '\n' + str(config.player_name.y) + '\n' + str(config.player_name.width) + '\n' + str(config.player_name.height) + '\n')
        f.write(str(config.weapon_name.x) + '\n' + str(config.weapon_name.y) + '\n' + str(config.weapon_name.width) + '\n' + str(config.weapon_name.height))
    print('Config set')

def init():
    if globals.config_inited:
        return
    if config.should_read_config:
        if os.path.isfile(config.config_path):
            read_config()
        else:
            setup_config()
    else:
        config.next_player_button = next_player_button_coordinate()
        config.player_name = player_name_box()
        config.weapon_name = player_weapon_box()
    globals.config_inited = True