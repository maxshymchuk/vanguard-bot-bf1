import config
from queue import Queue
from pynput.mouse import Listener
from classes import Box, Coordinate

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

def configure_positions():
    if not config.change_player_button_coordinate:
        config.change_player_button_coordinate = set_coordinate('Click next/prev player button box')
    if not config.player_name_box:
        config.player_name_box = set_box('player name')
    if not config.weapon_name_box:
        config.weapon_name_box = set_box('weapon name')