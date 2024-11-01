import config
from classes import Box, Coordinate

def str_to_rgb(str: str) -> tuple[int, int, int]:
    if not str:
        return None
    RGB_CHANNEL_NUM = 3
    split = list(map(int, str.split(',')))
    return tuple(split) if len(split) == RGB_CHANNEL_NUM else None

def config_to_json():
    config_json = {}
    config_json['window_title'] = config.window_title
    config_json['server_name'] = config.server_name
    config_json['screenshots_path'] = config.screenshots_path
    config_json['weapon_text_similarity_probability'] = config.weapon_text_similarity_probability
    config_json['player_name_similarity_probability'] = config.player_name_similarity_probability
    config_json['icon_probability'] = config.icon_probability
    config_json['discord_webhook_url'] = config.discord_webhook_url
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
        } if config.change_player_button_coordinate else None,
        'third_person_view_button_coordinate': {
            'x': config.third_person_view_button_coordinate.x,
            'y': config.third_person_view_button_coordinate.y
        } if config.third_person_view_button_coordinate else None,
        'player_name_box': {
            'x': config.player_name_box.x,
            'y': config.player_name_box.y,
            'width': config.player_name_box.width,
            'height': config.player_name_box.height
        } if config.player_name_box else None,
        'weapon_icon_box': {
            'x': config.weapon_icon_box.x,
            'y': config.weapon_icon_box.y,
            'width': config.weapon_icon_box.width,
            'height': config.weapon_icon_box.height
        } if config.weapon_icon_box else None,
        'weapon_name_box': {
            'x': config.weapon_name_box.x,
            'y': config.weapon_name_box.y,
            'width': config.weapon_name_box.width,
            'height': config.weapon_name_box.height
        } if config.weapon_name_box else None
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
    if 'icon_probability' in config_json:
        config.icon_probability = config_json['icon_probability']
    if 'discord_webhook_url' in config_json:
        config.discord_webhook_url = config_json['discord_webhook_url']
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
        if 'third_person_view_button_coordinate' in config_json['recognition']:
            third_person_view_button_coordinate = config_json['recognition']['third_person_view_button_coordinate']
            if third_person_view_button_coordinate:
                is_all_positions_set = False
                config.third_person_view_button_coordinate = Coordinate(third_person_view_button_coordinate['x'], third_person_view_button_coordinate['y'])
        if 'player_name_box' in config_json['recognition']:
            player_name_box = config_json['recognition']['player_name_box']
            if player_name_box:
                is_all_positions_set = False
                config.player_name_box = Box(player_name_box['x'], player_name_box['y'], player_name_box['width'], player_name_box['height'])
        if 'weapon_icon_box' in config_json['recognition']:
            weapon_icon_box = config_json['recognition']['weapon_icon_box']
            if weapon_icon_box:
                is_all_positions_set = False
                config.weapon_icon_box = Box(weapon_icon_box['x'], weapon_icon_box['y'], weapon_icon_box['width'], weapon_icon_box['height'])
        if 'weapon_name_box' in config_json['recognition']:
            weapon_name_box = config_json['recognition']['weapon_name_box']
            if weapon_name_box:
                is_all_positions_set = False
                config.weapon_name_box = Box(weapon_name_box['x'], weapon_name_box['y'], weapon_name_box['width'], weapon_name_box['height'])

    return is_all_positions_set