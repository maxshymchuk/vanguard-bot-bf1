import os
from difflib import SequenceMatcher

common_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

available_nickname_symbols = f'{common_symbols}-_[]'
available_weapon_symbols = f'{common_symbols}-/'

# add any error combination tesseract find to fix a word
replaceable = {
    '|': 'I',
    '€': 'e',
    '><': 'x'
}

def replace_wrong_symbols(str: str, wrong_symbols: dict[str, str] = replaceable) -> str:
    for substr in wrong_symbols.keys():
        str = str.replace(substr, wrong_symbols[substr])
    return str

def remove_restricted_symbols(str: str, available_symbols: str | None) -> str:
    if not available_symbols:
        return str
    for letter in str:
        if not letter in available_symbols:
            str = str.replace(letter, '')
    return str

def get_string_similarity(str1: str, str2: str) -> float:
    return SequenceMatcher(None, str1, str2).ratio()

def check_if_file(path: str):
    return os.path.exists(path) and os.path.isfile(path)