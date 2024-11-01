import api
import globals

def get_players() -> tuple[bool, dict]:
    return api.get_players_by_game_id(globals.game_id)