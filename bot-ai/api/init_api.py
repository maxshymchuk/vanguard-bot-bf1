import os
from dotenv import load_dotenv
from .modules import get_access_token, get_auth_code, get_session_id_by_authcode, get_persona_by_id
from .utils import print_error_message
from . import apiglobals

load_dotenv()

def init() -> bool:
    apiglobals.sid = os.getenv('SID')
    apiglobals.remid = os.getenv('REMID')

    success, apiglobals.access_token = get_access_token()
    if not success:
        print_error_message('Failed to get access token')
        return False, None

    resp_auth = get_auth_code()
    if not resp_auth.success:
        print_error_message('Failed to get auth code')
        return False, None

    apiglobals.remid = resp_auth.remid
    apiglobals.sid = resp_auth.sid

    success, session_id_or_error, persona_id = get_session_id_by_authcode(resp_auth.code)
    if not success:
        print_error_message('Failed to get session id', session_id_or_error)
        return False, None

    apiglobals.session_id = session_id_or_error
    apiglobals.my_persona_id = persona_id

    success, name_or_error = get_persona_by_id(apiglobals.my_persona_id)
    if not success:
        print_error_message('Failed to get persona for id', name_or_error)
        return False, None

    return True, name_or_error