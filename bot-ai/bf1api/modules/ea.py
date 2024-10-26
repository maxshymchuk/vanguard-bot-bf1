import requests
import bf1api.apiglobals as apiglobals
import uuid
import json

class ResponseAuth:
    def __init__(self) -> None:
        self.success = False
        self.remid = ''
        self.sid = ''
        self.code = ''
        self.content = ''

def get_access_token():
    content = ''
    try:
        headers = {'Cookie': f"remid={apiglobals.remid2};sid={apiglobals.sid2};"}
        response = requests.get(apiglobals.host1, headers=headers)
        content = json.loads(response.content)

        if response.status_code == 200:
            return True, content["access_token"]
    
    except Exception as e:
        print("Error in access token request " + str(e))

    return False, content

def get_auth_code() -> ResponseAuth:
    headers = {'Cookie': f"remid={apiglobals.remid2};sid={apiglobals.sid2};"}
    respAuth = ResponseAuth()
    try:
        response = requests.get(apiglobals.host, headers=headers, allow_redirects=False)
    
        if response.status_code == 302:
            location = str(response.headers['location'])
            if '127.0.0.1/success?code=' in location:
                if len(response.cookies) == 2:
                    respAuth.remid = response.cookies.values()[0]
                    respAuth.sid = response.cookies.values()[1]
                else:
                    respAuth.sid = response.cookies.values()[0]
                
                respAuth.success = True
                respAuth.code = location.replace('http://127.0.0.1/success?code=', '')

            respAuth.content = location
        else:
            respAuth.content = response.content
    except Exception as e:
        print("Error in get auth code " + str(e))

    return respAuth

def get_session_id_via_authcode(authCode: str):
    try:
        jsonBody = {'jsonrpc': '2.0',
                    'method':'Authentication.getEnvIdViaAuthCode',
                    'params': {
                        'authCode': authCode,
                        'locale:': 'en-GB'
                    },
                    'id': str(uuid.uuid4())}
        
        response = requests.post(apiglobals.bf1host, json=jsonBody)

        if response.status_code == 200:
            jsonContent = json.loads(response.content)
            return True, jsonContent['result']['sessionId'], jsonContent['result']['personaId']

    except Exception as e:
        print("Error in getting session id from auth code " + str(e))

    return False, json.loads(response.content), ''