import json
import requests
import bf1api.apiglobals as apiglobals
from bf1api.modules.common import rpc_headers, rpc_request

def get_persona_by_id(personaID: str) -> tuple[bool, str | object]:
    content = ''
    jsonBody = rpc_request('RSP.getPersonasByIds', {
        'game': 'tunguska',
        'personaIds': [personaID]
    })
    try:
        response = requests.post(apiglobals.bf1host, headers=rpc_headers(), json=jsonBody)
        content = json.loads(response.content)
        if response.status_code == 200:
            return True, content['result'][personaID]['displayName']
    except Exception as e:
        print("Error getting persona by id " + str(e))

    return False, content

def kick_player(gameID: str, personaID: str, reason: str) -> tuple[bool, object]:
    jsonBody = rpc_request('RSP.kickPlayer', {
        'game': 'tunguska',
        'gameId': gameID,
        'personaId': personaID,
        'reason': reason
    })
    try:
        response = requests.post(apiglobals.bf1host, headers=rpc_headers(), json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Error kicking player with id ' + str(personaID) + ' error: ' + str(e))

    return False, json.loads(response.content)