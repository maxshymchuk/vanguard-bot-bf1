import api
import globals
import time

def get_player_count() -> tuple[bool, int | None]:
    success, server_details_or_error = api.get_server_details_by_game_id(globals.game_id)
    if not success:
        return False, None

    player_count = server_details_or_error['result']['slots']['Soldier']['current']
    return True, player_count

def get_player_count_thread(lock) -> None:
    while not globals.threads_stop.is_set():
        with lock:
            success, player_count = get_player_count()
            if success:
                globals.player_count = player_count
        time.sleep(30)