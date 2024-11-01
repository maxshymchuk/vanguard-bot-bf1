import api
import globals

def get_server_map() -> tuple[bool, str | None]:
    success, server_details_or_error = api.get_server_details_by_game_id(globals.game_id)
    if not success:
        return False, None

    server_map = server_details_or_error['result']['mapNamePretty']
    return True, server_map