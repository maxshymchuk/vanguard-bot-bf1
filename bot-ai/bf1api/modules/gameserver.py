import json
import requests
import bf1api.apiglobals as apiglobals
import uuid

def get_player_persona_by_id(player_name: str) :
    headers = {'X-Expand-Results': str(True), 
               'Authorization': f'Bearer {apiglobals.access_token}'}
    try:
        response = requests.get(f'{apiglobals.host2}{player_name}', headers=headers)

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
        headers = {'X-GatewaySession': apiglobals.sessionID}

        response = requests.post(apiglobals.bf1host, headers=headers, json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print("Error getting server by persona id " + str(e))

    return False, json.loads(response.content)

def get_players(gameID) -> dict:
    try:
        params = {'gameID': gameID}
        teams = dict()
        response = requests.get(apiglobals.gametools, params=params)
        if response.status_code == 200:
            parsed_content = json.loads(response.content)
            team1 = parsed_content['teams'][0]['players']
            teams.update([(player['name'], player['player_id']) for player in team1])
            team2 = parsed_content['teams'][1]['players']
            teams.update([(player['name'], player['player_id']) for player in team2])
            return True, teams
    except Exception as e:
        print('Failed to get playerlist for game ID ' + gameID + ' error: ' + str(e))

    return False, dict()


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
        headers = {'X-GatewaySession': apiglobals.sessionID}

        response = requests.post(apiglobals.bf1host, headers=headers, json=jsonBody)
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
        headers = {'X-GatewaySession': apiglobals.sessionID}

        response = requests.post(apiglobals.bf1host, headers=headers, json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Failed to find server with gameID ' + gameID + ' error: ' + str(e))

    return False, json.loads(response.content)