import globals
import config
import api
from modules.utils import get_string_similarity

def _kick(player_name: str, reason: str, persona_id) -> bool:

    # -------------------------------------------------------------------------------
    # Don't kick yet, must test we aren't generating false positives
    # success, content = api.kick_player(globals.game_id, persona_id, reason)
    # -------------------------------------------------------------------------------
    if True:
        print('Kicked player ' + player_name + ' for reason: ' + reason + '!')
#         config.webhook.send(fr"""
# ```
# ✅KICK(TEST NOT ACTUAL KICK)
#     Name: {player_name}
#     Kick Reason: {reason}
#     PID: {persona_id}
# ```""", username="VG_Vanguard")
        return True
    else:
        print('Found player ' + player_name + ' but failed to kick him with reason ' + reason + '\nJSON: ' + str(content))
        config.webhook.send(fr"""
```
❌KICK
    Name: {player_name}
    Kick Reason: {reason}
    PID: {persona_id}
```""", username="VG_Vanguard")
        return False

def _search_for_and_kick_player(player_name: str, reason: str, teams) -> bool:

    if player_name in teams.keys():
        return _kick(player_name, reason, teams[player_name])

    highest_probability = 0
    most_likely_name = ''
    for team_player_name in teams.keys():
        probability = get_string_similarity(player_name, team_player_name)
        if probability > highest_probability:
            highest_probability = probability
            most_likely_name = team_player_name

    print('For player ' + player_name + ' best probability is ' + str(highest_probability) + ' for possible name ' + most_likely_name)
    if highest_probability > config.player_name_similarity_probability:
        print('Attempted kick player ' + player_name + ' is likely to have name ' + most_likely_name + ' with probability ' + str(highest_probability))

        if most_likely_name in teams.keys():
            return _kick(most_likely_name, reason, teams[most_likely_name])

    return False

def find_and_kick_player(player_name: str, reason: str) -> bool:

    if _search_for_and_kick_player(player_name, reason, find_and_kick_player.teams):
        return True

    print('Getting player list again')

    # Worst case we have to get the player list again and search
    success, find_and_kick_player.teams = api.get_players_by_game_id(globals.game_id)

    if not success:
        print('Failed to get player list ' + str(find_and_kick_player.teams))
        return False

    # Search again
    if _search_for_and_kick_player(player_name, reason, find_and_kick_player.teams):
        return True

    # Give up :(
    print('Giving up kicking player ' + player_name + ' could not find him in teams')
    return False

find_and_kick_player.teams = dict() # { player_name : persona_id } dict