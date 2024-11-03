import config

def print_error_message(msg: str, content = None) -> None:
    print(msg)
    if config.verbose and content:
        print('API called returned: ' + str(content))