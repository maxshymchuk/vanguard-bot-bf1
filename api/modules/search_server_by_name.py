import json
import requests
from .common import rpc_headers, rpc_request
from ..utils import print_error_message
from .. import endpoints

def search_server_by_name(server_name: str) -> tuple[bool, object]:
    json_body = rpc_request('GameServer.searchServers', {
        'filterJson': "{\"version\":6,\"name\":\"" + server_name + "\"}",
        'game': 'tunguska',
        'limit': '30',
        'protocolVersion': '3779779'
    })
    try:
        response = requests.post(endpoints.rpc_host, headers=rpc_headers(), json=json_body)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print_error_message('Failed to search for server ' + server_name, e)

    return False, json.loads(response.content)