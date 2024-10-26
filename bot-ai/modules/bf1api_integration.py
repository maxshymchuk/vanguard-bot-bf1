from bf1api.modules.rsp import kick_player
from bf1api.modules.gameserver import get_players
from modules.utils import get_string_similarity
import globals

def _kick(playerName: str, reason: str, personaId) -> bool:

    # -------------------------------------------------------------------------------
    # Don't kick yet, must test we aren't generating false positives
    # success, content = kick_player(globals.gameID, personaId, reason)
    # -------------------------------------------------------------------------------

    if True:
        print('Kicked player ' + playerName + ' for reason: ' + reason + '!')
        return True
    else:
        print('Found player ' + playerName + ' but failed to kick him, JSON: ' + str(content))
        return False    

def _search_for_and_kick_player(playerName: str, reason: str, teams) -> bool:

    if playerName in teams.keys():
        return _kick(playerName, reason, teams[playerName])

    highestProbability = 0
    mostLikelyName = ''
    for teamPlayerName in teams.keys():
        probability = get_string_similarity(playerName, teamPlayerName) 
        if probability > highestProbability:
            highestProbability = probability
            mostLikelyName = teamPlayerName

    print('For player ' + playerName + ' best probability is ' + str(highestProbability) + ' for possible name ' + mostLikelyName)
    if highestProbability > globals.playerNameSimilarityProbability:
        print('Attempted kick player ' + playerName + ' is likely to have name ' + mostLikelyName + ' with probability ' + str(highestProbability))
        return _kick(playerName, reason, teams[mostLikelyName])
    
    return False

def find_and_kick_player(playerName: str, reason: str) -> bool:

    if _search_for_and_kick_player(playerName, reason, find_and_kick_player.teams):
        return True
    
    # Worst case we have to get the player list again and search
    success, find_and_kick_player.teams = get_players(globals.gameID)

    if not success:
        print('Failed to get player list ' + str(find_and_kick_player.teams))
        return False

    # Search again
    if _search_for_and_kick_player(playerName, reason, find_and_kick_player.teams):
        return True

    # Give up :(
    print('Giving up kicking player ' + playerName + 'could not find him in teams')
    return False

find_and_kick_player.teams = dict() # Playername : PersonaID dict