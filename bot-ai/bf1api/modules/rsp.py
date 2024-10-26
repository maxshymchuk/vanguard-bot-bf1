import json
import requests
import bf1api.apiglobals as apiglobals
from bf1api.modules.common import rsp_headers, rsp_request

def get_personas_by_ids(personaID: str) -> tuple[bool, str | object]:
    content = ''
    jsonBody = rsp_request('RSP.getPersonasByIds', {
        'game': 'tunguska',
        'personaIds': [personaID]
    })
    try:
        response = requests.post(apiglobals.bf1host, headers=rsp_headers(), json=jsonBody)
        content = json.loads(response.content)
        if response.status_code == 200:
            return True, content['result'][personaID]['displayName']
    except Exception as e:
        print("Error getting persona by id " + str(e))

    return False, content

def kick_player(gameID: str, personaID: str, reason: str) -> tuple[bool, object]:
    jsonBody = rsp_request('RSP.kickPlayer', {
        'game': 'tunguska',
        'gameId': gameID,
        'personaId': personaID,
        'reason': reason
    })
    try:
        response = requests.post(apiglobals.bf1host, headers=rsp_headers(), json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Error kicking player with id ' + str(personaID) + ' error: ' + str(e))

    return False, json.loads(response.content)