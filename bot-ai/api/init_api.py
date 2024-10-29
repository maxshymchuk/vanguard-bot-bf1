from .modules import get_access_token, get_auth_code, get_session_id_by_authcode, get_persona_by_id
from .utils import print_error_message
from . import apiglobals

def init() -> bool:
    success, apiglobals.access_token = get_access_token()
    if not success:
        print_error_message('Failed to get acceess token')
        return False

    resp_auth = get_auth_code()
    if not resp_auth.success:
        print_error_message('Failed to get auth code')
        return False

    apiglobals.remid2 = resp_auth.remid
    apiglobals.sid2 = resp_auth.sid

    success, session_id_or_error, persona_id = get_session_id_by_authcode(resp_auth.code)
    if not success:
        print_error_message('Failed to get session id', session_id_or_error)
        return False

    apiglobals.session_id = session_id_or_error
    apiglobals.my_persona_id = persona_id

    success, name_or_error = get_persona_by_id(apiglobals.my_persona_id)
    if not success:
        print_error_message('Failed to get persona for id', name_or_error)
        return False

    print('You are ' + name_or_error)

    return True