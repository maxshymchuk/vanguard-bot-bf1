import json
import requests
from .common import print_error_message, rpc_headers, rpc_request
from .. import endpoints

def get_persona_by_id(persona_id: str) -> tuple[bool, str | object]:
    content = ''
    json_body = rpc_request('RSP.getPersonasByIds', {
        'game': 'tunguska',
        'personaIds': [persona_id]
    })
    try:
        response = requests.post(endpoints.rpc_host, headers=rpc_headers(), json=json_body)
        content = json.loads(response.content)
        if response.status_code == 200:
            return True, content['result'][persona_id]['displayName']
    except Exception as e:
        print_error_message('Error getting persona by id', e)

    return False, content