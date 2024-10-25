from modules.ea import get_access_token, get_session_id_via_authcode, get_auth_code
from modules.gameserver import get_servers_by_persona_ids, search_server, get_player_persona_by_id, get_full_server_details
from modules.rsp import get_personas_by_ids, kick_player
import globals

def print_error_message(msg, content):
    print(msg)
    if globals.verbose_errors:
        print('API called returned: ' + str(content))

def init_api(verbose_errors):
    globals.verbose_errors = verbose_errors
    success, globals.access_token = get_access_token()
    if not success:
        print_error_message('Failed to get acceess token', globals.access_token)
        return False
        
    print('Access token: ' + globals.access_token)

    respAuth = get_auth_code()
    if not respAuth.success:
        print('Failed to get auth code')
        return False

    globals.remid = respAuth.remid
    globals.sid = respAuth.sid

    success, globals.sessionID = get_session_id_via_authcode(respAuth.code)
    if not success:
        print_error_message('Failed to get session id', globals.sessionID)
        return False
    
    print('Init API success')
    return True

if __name__ == '__main__':

    if not init_api(True):
        print('Failed to init api')
        quit()
    
    # playername = 'mystzone44'
    # success, personaID = get_player_persona_by_id(playername)
    # if not success:
    #     print_error_message('Failed to get player ' + playername, personaID)
    #     quit()

    servername = '![VG]Vanguard'
    success, serverinfo = search_server(servername)
    if not success:
        print_error_message('Failed to get server' + servername, serverinfo)
        quit()

    #print(serverinfo)

    if len(serverinfo['result']['gameservers']) > 0:
        gameID = serverinfo['result']['gameservers'][0]['gameId']
    else:
        print('No server found called ' + servername)
        quit()

    # success, playerlist = get_playerlist(gameID)
    # if not success:
    #     print_error_message('Failed to get player list for server ' + servername, playerlist)
    #     #quit()

    # #print(playerlist)

    # success, teams = get_teams(gameID)
    # if not success:
    #     print_error_message('Failed to get teams for server ' + servername, teams)
    #     quit()

    # print(teams)

    success, details = get_full_server_details(gameID)
    if not success:
        print_error_message('Failed to get server details for id ' + gameID, details)
        quit()

    # details['result']['rspInfo']

    print(details)

    # success, content = kick_player(globals.sessionID, gameID, personaID, 'Twat')

    # if not success:
    #     print_error_message('Failed to kick player with id ' + str(personaID), content)
    #     quit()

    # print(content)

    input('Press any key to exit')
