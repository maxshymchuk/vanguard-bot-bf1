import json
import requests
import bf1api.apiglobals as apiglobals
from bf1api.modules.common import rsp_headers, rsp_request

def get_player_persona_by_id(player_name: str) -> tuple[bool, str | object]:
    headers = {'X-Expand-Results': str(True), 'Authorization': f'Bearer {apiglobals.access_token}'}
    try:
        response = requests.get(f'{apiglobals.host2}{player_name}', headers=headers)
        if response.status_code == 200:
            return True, json.loads(response.content)['personas']['persona'][0]['personaId']
    except Exception as e:
        print("Error in get player persona by id request " + str(e))
    
    return False, json.loads(response.content)

def get_servers_by_persona_ids(personaID: str) -> tuple[bool, object]:
    jsonBody = rsp_request('GameServer.getServersByPersonaIds', {
        'game': 'tunguska',
        'personaIds': [personaID]
    })
    try:
        response = requests.post(apiglobals.bf1host, headers=rsp_headers(), json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print("Error getting server by persona id " + str(e))

    return False, json.loads(response.content)

def get_players(gameID: str) -> tuple[bool, dict]:
    params = {'gameID': gameID}
    teams = dict()
    try:
        response = requests.get(apiglobals.gametools, params=params)
        if response.status_code == 200:
            parsed_content = json.loads(response.content)
            team1 = parsed_content['teams'][0]['players']
            team2 = parsed_content['teams'][1]['players']
            team1.extend(team2)
            for player in team1:
                # We also need to append the platoon tag because it shows up in third person view
                if player['platoon']:
                    teams['[' + player['platoon'] + ']' + player['name']] = player['player_id']
                else:
                    teams[player['name']] =  player['player_id']
            return True, teams
    except Exception as e:
        print('Failed to get playerlist for game ID ' + gameID + ' error: ' + str(e))

    return False, dict()


def search_server(serverName: str) -> tuple[bool, object]:
    jsonBody = rsp_request('GameServer.searchServers', {
        'filterJson': "{\"version\":6,\"name\":\"" + serverName + "\"}",
        'game': 'tunguska',
        'limit': '30',
        'protocolVersion': '3779779'
    })
    try:
        response = requests.post(apiglobals.bf1host, headers=rsp_headers(), json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Failed to search for server ' + serverName + ' error: ' + str(e))

    return False, json.loads(response.content)

def get_full_server_details(gameID: str) -> tuple[bool, object]:
    jsonBody = rsp_request('GameServer.getFullServerDetails', {
        'game': 'tunguska',
        'gameId': gameID
    })
    try:
        response = requests.post(apiglobals.bf1host, headers=rsp_headers(), json=jsonBody)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print('Failed to find server with gameID ' + gameID + ' error: ' + str(e))

    return False, json.loads(response.content)