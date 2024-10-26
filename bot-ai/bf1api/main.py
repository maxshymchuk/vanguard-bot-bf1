from bf1api.modules.ea import get_access_token, get_session_id_via_authcode, get_auth_code
from bf1api.modules.gameserver import get_servers_by_persona_ids, search_server, get_player_persona_by_id, get_full_server_details, get_players
from bf1api.modules.rsp import get_persona_by_id, kick_player
import bf1api.apiglobals as apiglobals

def print_error_message(msg: str, content = None) -> None:
    print(msg)
    if apiglobals.verbose_errors and content:
        print('API called returned: ' + str(content))

def init_api(verbose_errors: bool) -> bool:
    apiglobals.verbose_errors = verbose_errors
    success, apiglobals.access_token = get_access_token()
    if not success:
        print_error_message('Failed to get acceess token')
        return False
        
    print('Access token: ' + apiglobals.access_token)

    respAuth = get_auth_code()
    if not respAuth.success:
        print_error_message('Failed to get auth code')
        return False

    apiglobals.remid2 = respAuth.remid
    apiglobals.sid2 = respAuth.sid

    success, sessionIdOrError, personaId = get_session_id_via_authcode(respAuth.code)
    if not success:
        print_error_message('Failed to get session id', sessionIdOrError)
        return False
    
    apiglobals.sessionID = sessionIdOrError
    apiglobals.myPersonaId = personaId

    print('Auth Code:', respAuth.code)
    print('Session ID:', apiglobals.sessionID)
    print('Persona ID:', apiglobals.myPersonaId)

    print('Init API success')

    success, nameOrError = get_persona_by_id(apiglobals.myPersonaId)
    if not success:
        print_error_message('Failed to get persona for id', nameOrError)
        return False
    
    print('You are ' + nameOrError)

    return True

def get_server_id_and_fullname(servername: str) -> tuple[bool, str | None, str | None]:
    success, serverinfoOrError = search_server(servername)
    if not success:
        print_error_message('Failed to get server' + servername, serverinfoOrError)
        return False, None, None

    servers = serverinfoOrError['result']['gameservers']
    if len(servers) > 0:
        return True, servers[0]['gameId'], servers[0]['name']
    else:
        print('No server found called ' + servername)
        return False, None, None

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
