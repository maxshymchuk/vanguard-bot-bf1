import json
import requests
from .common import rpc_headers, rpc_request
from ..utils import print_error_message
from .. import endpoints

def kick_player(game_id: str, persona_id: str, reason: str) -> tuple[bool, object]:
    json_body = rpc_request('RSP.kickPlayer', {
        'game': 'tunguska',
        'gameId': game_id,
        'personaId': persona_id,
        'reason': reason
    })
    try:
        response = requests.post(endpoints.rpc_host, headers=rpc_headers(), json=json_body)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print_error_message('Error kicking player with id ' + str(persona_id), e)

    return False, json.loads(response.content)