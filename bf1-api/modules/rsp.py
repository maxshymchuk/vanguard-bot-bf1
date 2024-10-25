import json
import requests
import globals
import uuid

# def get_teams(gameID, method):
#     try:
#         jsonBody = {'jsonrpc': '2.0',
#                 'method':'RSP.getPersonaIdsBySlots',
#                 'params': {
#                     'game': 'tunguska',
#                     'gameId': gameID,
#                 },
#                 'id': str(uuid.uuid4())}
#         headers = {'X-GatewaySession': globals.sessionID}

#         response = requests.post(globals.bf1host, headers=headers, json=jsonBody)
#         if response.status_code == 200:
#             return True, json.loads(response.content)
#     except Exception as e:
#         print('Error getting teams' + str(e))

#     return False, json.loads(response.content)

def get_personas_by_ids(personaID):
    try:
        jsonBody = {'jsonrpc': '2.0',
                    'method':'RSP.getPersonasByIds',
                    'params': {
                        'game': 'tunguska',
                        'personaIds': [personaID]
                    },
                    'id': str(uuid.uuid4())}
        
        headers = {'X-GatewaySession': globals.sessionID}
        response = requests.post(globals.bf1host, headers=headers, json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)['result'][personaID]['displayName']
    except Exception as e:
        print("Error getting persona by id " + str(e))

    return False, json.loads(response.content)

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
        headers = {'X-GatewaySession': globals.sessionID}

        response = requests.post(globals.bf1host, headers=headers, json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Error kicking player with id ' + str(personaID) + ' error: ' + str(e))

    return False, json.loads(response.content)