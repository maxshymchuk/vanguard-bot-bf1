import api
import globals
import time
import config

def get_players() -> tuple[bool, dict]:
    return api.get_players_by_game_id(globals.game_id)

def get_players_thread() -> None:
    while not globals.threads_stop.is_set():
        success, teams = api.get_players_by_game_id(globals.game_id)
        if success:
            player_count = len(teams)
            with globals.teams_lock:
                globals.teams = teams
                if player_count < config.minimum_player_count:
                    prevStatus = globals.player_count_too_low
                    globals.player_count_too_low = True
                    if prevStatus != player_count < config.minimum_player_count:
                        print(f'Player count {player_count} is now less than minimum player count {config.minimum_player_count}, kicking disabled')
                else:
                    prevStatus = globals.player_count_too_low
                    globals.player_count_too_low = False
                    if prevStatus != player_count < config.minimum_player_count:
                        print(f'Player count {player_count} is now greater than or equal to minimum player count {config.minimum_player_count}, kicking enabled')
        globals.threads_stop.wait(15)
        time.sleep(3)