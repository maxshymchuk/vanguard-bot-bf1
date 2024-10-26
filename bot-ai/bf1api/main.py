from bf1api.modules.ea import get_access_token, get_session_id_via_authcode, get_auth_code
from bf1api.modules.gameserver import get_servers_by_persona_ids, search_server, get_player_persona_by_id, get_full_server_details, get_players
from bf1api.modules.rsp import get_personas_by_ids, kick_player
import bf1api.apiglobals as apiglobals

def print_error_message(msg, content):
    print(msg)
    if apiglobals.verbose_errors:
        print('API called returned: ' + str(content))

def init_api(verbose_errors):
    apiglobals.verbose_errors = verbose_errors
    success, apiglobals.access_token = get_access_token()
    if not success:
        print_error_message('Failed to get acceess token', apiglobals.access_token)
        return False
        
    print('Access token: ' + apiglobals.access_token)

    respAuth = get_auth_code()
    if not respAuth.success:
        print('Failed to get auth code')
        return False

    apiglobals.remid2 = respAuth.remid
    apiglobals.sid2 = respAuth.sid

    success, apiglobals.sessionID, apiglobals.myPersonaId = get_session_id_via_authcode(respAuth.code)
    if not success:
        print_error_message('Failed to get session id', apiglobals.sessionID)
        return False
    
    print('Init API success')

    success, name = get_personas_by_ids(apiglobals.myPersonaId)
    if not success:
        print('Failed to get persona for id ' + apiglobals.myPersonaId)
        quit()
    print('You are ' + name)

    return True

def get_server_id(servername: str):
    success, serverinfo = search_server(servername)
    if not success:
        print_error_message('Failed to get server' + servername, serverinfo)
        return False, ''

    if len(serverinfo['result']['gameservers']) > 0:
        gameID = serverinfo['result']['gameservers'][0]['gameId']
    else:
        print('No server found called ' + servername)
        return False, ''
    
    return True, gameID


if __name__ == '__main__':

    if not init_api(True):
        print('Failed to init api')
        quit()

    # success, teams = get_players(gameID)
    # if not success:
    #     print('Failed to get teams for server ' + servername)
    #     quit()

    # for key in teams.keys():
    #     print(key)

    # playername = input("Enter player name to kick ")

    # reason = input("Reason: ")

    # success, details = get_full_server_details(gameID)
    # if not success:
    #     print_error_message('Failed to get server details for id ' + gameID, details)
    #     quit()

    # print(details)

    # details['result']['rspInfo']

    # success, personaID = get_player_persona_by_id(playername)
    # if not success:
    #     print_error_message('Failed to get player ' + playername, personaID)
    #     quit()

    # success, content = kick_player(gameID, personaID, reason)

    # if not success:
    #     print_error_message('Failed to kick player with id ' + str(personaID), content)
    #     quit()

    # print(content)

    # input('Press any key to exit')
