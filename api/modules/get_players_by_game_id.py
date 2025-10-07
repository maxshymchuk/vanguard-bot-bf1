import json
import requests
from ..utils import print_error_message
from .. import endpoints
import globals

def get_players_by_game_id(game_id: str) -> tuple[bool, dict]:
    params = {'gameID': game_id}
    teams = dict()
    try:
        response = requests.get(endpoints.gametools, params=params)
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

            # Also remove anyone from the kick list no longer in the game
            globals.kick_list.intersection_update(teams)

            return True, teams
    except Exception as e:
        print_error_message('Failed to get playerlist for game id ' + game_id, e)

    return False, dict()