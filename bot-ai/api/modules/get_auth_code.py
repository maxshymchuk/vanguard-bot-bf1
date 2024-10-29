import requests
from .common import rest_headers
from ..utils import print_error_message
from .. import endpoints

class ResponseAuth:
    def __init__(self) -> None:
        self.success = False
        self.remid = ''
        self.sid = ''
        self.code = ''
        self.content = ''

def get_auth_code() -> ResponseAuth:
    resp_auth = ResponseAuth()
    try:
        response = requests.get(endpoints.auth_host, headers=rest_headers(), allow_redirects=False)
        if response.status_code == 302:
            location = str(response.headers['location'])
            if '127.0.0.1/success?code=' in location:
                if len(response.cookies) == 2:
                    resp_auth.remid = response.cookies.values()[0]
                    resp_auth.sid = response.cookies.values()[1]
                else:
                    resp_auth.sid = response.cookies.values()[0]

                resp_auth.success = True
                resp_auth.code = location.replace('http://127.0.0.1/success?code=', '')

            resp_auth.content = location
        else:
            resp_auth.content = response.content
    except Exception as e:
        print_error_message('Error in get auth code request', e)

    return resp_auth