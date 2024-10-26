import json
import requests
import bf1api.apiglobals as apiglobals
import uuid

def get_personas_by_ids(personaID):
    content = ''
    try:
        jsonBody = {'jsonrpc': '2.0',
                    'method':'RSP.getPersonasByIds',
                    'params': {
                        'game': 'tunguska',
                        'personaIds': [personaID]
                    },
                    'id': str(uuid.uuid4())}
        
        headers = {'X-GatewaySession': apiglobals.sessionID}
        response = requests.post(apiglobals.bf1host, headers=headers, json=jsonBody)
        content = json.loads(response.content)
        if response.status_code == 200:
            return True, content['result'][personaID]['displayName']
    except Exception as e:
        print("Error getting persona by id " + str(e))

    return False, content

def kick_player(gameID, personaID, reason):
    try:
        jsonBody = {'jsonrpc': '2.0',
                'method':'RSP.kickPlayer',
                'params': {
                    'game': 'tunguska',
                    'gameId': gameID,
                    'personaId': personaID,
                    'reason': reason
                },
                'id': str(uuid.uuid4())}
        headers = {'X-GatewaySession': apiglobals.sessionID}

        response = requests.post(apiglobals.bf1host, headers=headers, json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Error kicking player with id ' + str(personaID) + ' error: ' + str(e))

    return False, json.loads(response.content)