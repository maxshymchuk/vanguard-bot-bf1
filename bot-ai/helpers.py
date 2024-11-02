import os
import sys

def check_if_file(path: str):
    return os.path.exists(path) and os.path.isfile(path)

def delete_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def print_on_same_line(text: str):
    print(text)
    delete_last_line()