import json
import requests
from .common import print_error_message
from .. import apiglobals
from .. import endpoints

def get_player_persona_by_name(player_name: str) -> tuple[bool, str | object]:
    headers = {'X-Expand-Results': str(True), 'Authorization': f'Bearer {apiglobals.access_token}'}
    try:
        response = requests.get(f'{endpoints.identity_host}{player_name}', headers=headers)
        if response.status_code == 200:
            return True, json.loads(response.content)['personas']['persona'][0]['personaId']
    except Exception as e:
        print_error_message('Error in get player persona by id request', e)

    return False, json.loads(response.content)