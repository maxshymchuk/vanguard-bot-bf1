import uuid
import bf1api.apiglobals as apiglobals

def rpc_headers() -> dict[str, str]:
    return {'X-GatewaySession': apiglobals.sessionID}

def rpc_request(method: str, params: object) -> dict[str, str | object]:
    return {
        'id': str(uuid.uuid4()),
        'jsonrpc': '2.0',
        'method': method,
        'params': params
    }