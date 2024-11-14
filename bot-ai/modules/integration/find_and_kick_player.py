import globals
import config
import api
from modules.utils import get_string_similarity

def _kick(player_name: str, reason: str, persona_id) -> bool:

    with globals.kick_lock:
        if player_name in globals.kick_list:
            print(f'Player {player_name} already marked for kicking, skipping')
            return True
        
        globals.kick_list.add(player_name)

        # -------------------------------------------------------------------------------
        success, content = api.kick_player(globals.game_id, persona_id, reason)
        # -------------------------------------------------------------------------------
        if success:
            print('Kicked player ' + player_name + ' for reason: ' + reason + '!')
            globals.players_kicked += 1
            config.kick_webhook.send(fr"""
```
✅KICK
    Name: {player_name}
    Kick Reason: {reason}
    PID: {persona_id}
```""", username=config.my_username)
            return True
        else:
            print('Found player ' + player_name + ' but failed to kick him with reason ' + reason)
            if config.verbose:
                print(f'Error: {str(content)}')
            config.webhook.send(fr"""
```
❌KICK FAILED
    Name: {player_name}
    Kick Reason: {reason}
    PID: {persona_id}
```""", username=config.my_username)
        return False

def _search_for_and_kick_player(player_name: str, reason: str) -> bool:

    if player_name in globals.teams.keys():
        _kick(player_name, reason, globals.teams[player_name])
        return True

    highest_probability = 0
    most_likely_name = ''
    for team_player_name in globals.teams.keys():
        probability = get_string_similarity(player_name, team_player_name)
        if probability > highest_probability:
            highest_probability = probability
            most_likely_name = team_player_name

    #print('For player ' + player_name + ' best probability is ' + str(highest_probability) + ' for possible name ' + most_likely_name)
    if highest_probability > config.player_name_similarity_probability:
        #print('Attempted kick player ' + player_name + ' is likely to have name ' + most_likely_name + ' with probability ' + str(highest_probability))

        if most_likely_name in globals.teams.keys():
            _kick(most_likely_name, reason, globals.teams[most_likely_name])
            return True

    return False

def find_and_kick_player(player_name: str, reason: str) -> bool:

    with globals.teams_lock:
        if _search_for_and_kick_player(player_name, reason):
            return True

        print('Getting player list again')

        # Worst case we have to get the player list again and search
        success, globals.teams = api.get_players_by_game_id(globals.game_id)

        if not success:
            print('Failed to get player list ' + str(globals.teams))
            return False

        # Search again
        if _search_for_and_kick_player(player_name, reason):
            return True

    # Give up :(
    print('Giving up kicking player ' + player_name + ' could not find him in teams')
    return False