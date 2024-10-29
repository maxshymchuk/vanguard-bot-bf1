from api import search_server_by_name

def get_server_id_and_fullname(server_name: str) -> tuple[bool, str | None, str | None]:
    success, server_info_or_error = search_server_by_name(server_name)
    if not success:
        return False, None, None

    servers = server_info_or_error['result']['gameservers']
    if len(servers) > 0:
        return True, servers[0]['gameId'], servers[0]['name']
    else:
        print('No server found called ' + server_name)
        return False, None, None