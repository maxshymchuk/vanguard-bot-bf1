import json
import requests
import globals
import uuid

def get_player_persona_by_id(player_name: str) :
    headers = {'X-Expand-Results': str(True), 
               'Authorization': f'Bearer {globals.access_token}'}
    try:
        response = requests.get(f'{globals.host2}{player_name}', headers=headers)

        if response.status_code == 200:
            return True, json.loads(response.content)['personas']['persona'][0]['personaId']

    except Exception as e:
        print("Error in get player persona by id request " + str(e))
    
    return False, json.loads(response.content)

def get_servers_by_persona_ids(personaID):
    try:
        jsonBody = {'jsonrpc': '2.0',
                'method':'GameServer.getServersByPersonaIds',
                'params': {
                    'game': 'tunguska',
                    'personaIds': [personaID]
                },
                'id': str(uuid.uuid4())}
        headers = {'X-GatewaySession': globals.sessionID}

        response = requests.post(globals.bf1host, headers=headers, json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print("Error getting server by persona id " + str(e))

    return False, json.loads(response.content)

# def get_playerlist(gameID):
#     try:
#         jsonBody = {'jsonrpc': '2.0',
#                 'method':'GameServer.getPersonaIdsBySlot',
#                 'params': {
#                     'game': 'tunguska',
#                     'gameId': gameID
#                 },
#                 'id': str(uuid.uuid4())}
#         headers = {'X-GatewaySession': globals.sessionID}

#         response = requests.post(globals.bf1host, headers=headers, json=jsonBody)
#         if response.status_code == 200:
#             return True, json.loads(response.content)
#     except Exception as e:
#         print('Failed to get playerlist for game ID ' + gameID + ' error: ' + str(e))

#     return False, json.loads(response.content)


def search_server(serverName):
    try:
        jsonBody = {'jsonrpc': '2.0',
                'method':'GameServer.searchServers',
                'params': {
                    'filterJson': "{\"version\":6,\"name\":\"" + serverName + "\"}",
                    'game': 'tunguska',
                    'limit': '30',
                    'protocolVersion': '3779779'
                },
                'id': str(uuid.uuid4())}
        headers = {'X-GatewaySession': globals.sessionID}

        response = requests.post(globals.bf1host, headers=headers, json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Failed to search for server ' + serverName + ' error: ' + str(e))

    return False, json.loads(response.content)

def get_full_server_details(gameID):
    try:
        jsonBody = {'jsonrpc': '2.0',
                'method':'GameServer.getFullServerDetails',
                'params': {
                    'game': 'tunguska',
                    'gameId': gameID
                },
                'id': str(uuid.uuid4())}
        headers = {'X-GatewaySession': globals.sessionID}

        response = requests.post(globals.bf1host, headers=headers, json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Failed to find server with gameID ' + gameID + ' error: ' + str(e))

    return False, json.loads(response.content)