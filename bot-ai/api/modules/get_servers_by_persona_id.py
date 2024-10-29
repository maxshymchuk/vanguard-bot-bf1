import json
import requests
from .common import print_error_message, rpc_headers, rpc_request
from .. import endpoints

def get_servers_by_persona_id(persona_id: str) -> tuple[bool, object]:
    json_body = rpc_request('GameServer.getServersByPersonaIds', {
        'game': 'tunguska',
        'personaIds': [persona_id]
    })
    try:
        response = requests.post(endpoints.rpc_host, headers=rpc_headers(), json=json_body)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print_error_message('Error getting server by persona id', e)

    return False, json.loads(response.content)