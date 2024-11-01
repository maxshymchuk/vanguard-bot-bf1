import os

def check_if_file(path: str):
    return os.path.exists(path) and os.path.isfile(path)