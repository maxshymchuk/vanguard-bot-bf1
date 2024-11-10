import api
import globals
import time
import config

def get_player_count() -> tuple[bool, int | None]:
    success, server_details_or_error = api.get_server_details_by_game_id(globals.game_id)
    if not success:
        return False, None

    player_count = server_details_or_error['result']['slots']['Soldier']['current']
    return True, player_count

def get_player_count_thread(lock) -> None:
    while not globals.threads_stop.is_set():
        success, player_count = get_player_count()
        if success:
            if player_count < config.minimum_player_count:
                with lock:
                    prevStatus = globals.player_count_too_low
                    globals.player_count_too_low = True
                if prevStatus != player_count < config.minimum_player_count:
                    print(f'Player count {player_count} is now less than minimum player count {config.minimum_player_count}, kicking disabled')
            else:
                with lock:
                    prevStatus = globals.player_count_too_low
                    globals.player_count_too_low = False
                if prevStatus != player_count < config.minimum_player_count:
                    print(f'Player count {player_count} is now greater than or equal to minimum player count {config.minimum_player_count}, kicking enabled')
        globals.threads_stop.wait(30)
        time.sleep(3)