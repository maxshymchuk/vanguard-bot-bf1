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

def str_to_rgb(str: str) -> tuple[int, int, int]:
    if not str:
        return None
    RGB_CHANNEL_NUM = 3
    split = list(map(int, str.split(',')))
    return tuple(split) if len(split) == RGB_CHANNEL_NUM else None

def configure_positions():
    if not config.change_player_button_coordinate:
        config.change_player_button_coordinate = set_coordinate('Click next/prev player button box')
    if not config.player_name_box:
        config.player_name_box = set_box('player name')
    if not config.weapon_name_box:
        config.weapon_name_box = set_box('weapon name')

def config_to_json():
    config_json = {}
    config_json['window_title'] = config.window_title
    config_json['server_name'] = config.server_name
    config_json['screenshots_path'] = config.screenshots_path
    config_json['weapon_text_similarity_probability'] = config.weapon_text_similarity_probability
    config_json['player_name_similarity_probability'] = config.player_name_similarity_probability
    config_json['discord_webhook'] = config.discord_webhook
    config_json['banned_weapons'] = config.banned_weapons
    config_json['colors'] = {
        'ally_color': ','.join(map(str, config.ally_color)),
        'enemy_color': ','.join(map(str, config.enemy_color)),
        'squad_color': ','.join(map(str, config.squad_color))
    }
    config_json['recognition'] = {
        'change_player_button_coordinate': {
            'x': config.change_player_button_coordinate.x,
            'y': config.change_player_button_coordinate.y
        },
        'player_name_box': {
            'x': config.player_name_box.x,
            'y': config.player_name_box.y,
            'width': config.player_name_box.width,
            'height': config.player_name_box.height
        },
        'weapon_name_box': {
            'x': config.weapon_name_box.x,
            'y': config.weapon_name_box.y,
            'width': config.weapon_name_box.width,
            'height': config.weapon_name_box.height
        }
    }
    return config_json

def json_to_config(config_json):
    if 'window_title' in config_json:
        config.window_title = config_json['window_title']
    if 'server_name' in config_json:
        config.server_name = config_json['server_name']
    if 'screenshots_path' in config_json:
        config.screenshots_path = config_json['screenshots_path']
    if 'weapon_text_similarity_probability' in config_json:
        config.weapon_text_similarity_probability = config_json['weapon_text_similarity_probability']
    if 'player_name_similarity_probability' in config_json:
        config.player_name_similarity_probability = config_json['player_name_similarity_probability']
    if 'discord_webhook' in config_json:
        config.discord_webhook = config_json['discord_webhook']
    if 'banned_weapons' in config_json:
        config.banned_weapons = config_json['banned_weapons']

    if 'colors' in config_json:
        ally_color = str_to_rgb(config_json['colors']['ally_color'])
        if ally_color:
            config.ally_color = ally_color
        enemy_color = str_to_rgb(config_json['colors']['enemy_color'])
        if enemy_color:
            config.enemy_color = enemy_color
        squad_color = str_to_rgb(config_json['colors']['squad_color'])
        if squad_color:
            config.squad_color = squad_color

    is_all_positions_set = True
    if 'recognition' in config_json:
        if 'change_player_button_coordinate' in config_json['recognition']:
            change_player_button_coordinate = config_json['recognition']['change_player_button_coordinate']
            if change_player_button_coordinate:
                is_all_positions_set = False
                config.change_player_button_coordinate = Coordinate(change_player_button_coordinate['x'], change_player_button_coordinate['y'])
        if 'player_name_box' in config_json['recognition']:
            player_name_box = config_json['recognition']['player_name_box']
            if player_name_box:
                is_all_positions_set = False
                config.player_name_box = Box(player_name_box['x'], player_name_box['y'], player_name_box['width'], player_name_box['height'])
        if 'weapon_name_box' in config_json['recognition']:
            weapon_name_box = config_json['recognition']['weapon_name_box']
            if weapon_name_box:
                is_all_positions_set = False
                config.weapon_name_box = Box(weapon_name_box['x'], weapon_name_box['y'], weapon_name_box['width'], weapon_name_box['height'])

    return is_all_positions_set