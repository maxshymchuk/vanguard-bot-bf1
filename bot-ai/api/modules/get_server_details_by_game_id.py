import json
import requests
from .common import rpc_headers, rpc_request
from ..utils import print_error_message
from .. import endpoints

def get_server_details_by_game_id(game_id: str) -> tuple[bool, object]:
    json_body = rpc_request('GameServer.getServerDetails', {
        'game': 'tunguska',
        'gameId': game_id
    })
    try:
        response = requests.post(endpoints.rpc_host, headers=rpc_headers(), json=json_body)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print_error_message('Failed to find server with game id ' + game_id, e)

    return False, json.loads(response.content)