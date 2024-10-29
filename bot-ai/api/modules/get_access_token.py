import json
import requests
from .common import print_error_message, rest_headers
from .. import endpoints

def get_access_token() -> tuple[bool, str | None]:
    try:
        response = requests.get(endpoints.access_host, headers=rest_headers())
        content = json.loads(response.content)
        if response.status_code == 200:
            return True, content["access_token"]
    except Exception as e:
        print_error_message('Error in access token request', e)

    return False, None