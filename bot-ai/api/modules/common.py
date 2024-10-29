import uuid
import config
from .. import apiglobals

def rest_headers() -> dict[str, str]:
    return {'Cookie': f'remid={apiglobals.remid2};sid={apiglobals.sid2};'}

def rpc_headers() -> dict[str, str]:
    return {'X-GatewaySession': apiglobals.session_id}

def rpc_request(method: str, params: object) -> dict[str, str | object]:
    return {
        'id': str(uuid.uuid4()),
        'jsonrpc': '2.0',
        'method': method,
        'params': params
    }

def print_error_message(msg: str, content = None) -> None:
    print(msg)
    if config.verbose_errors and content:
        print('API called returned: ' + str(content))