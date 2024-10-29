import requests
import json
from .common import print_error_message, rpc_request
from .. import endpoints

def get_session_id_by_authcode(auth_code: str) -> tuple[bool, str | object, str | None]:
    json_body = rpc_request('Authentication.getEnvIdViaAuthCode', {
        'authCode': auth_code,
        'locale:': 'en-GB'
    })
    try:
        response = requests.post(endpoints.rpc_host, json=json_body)
        if response.status_code == 200:
            json_content = json.loads(response.content)
            return True, json_content['result']['sessionId'], json_content['result']['personaId']
    except Exception as e:
        print_error_message('Error in getting session id from auth code', e)

    return False, json.loads(response.content), None