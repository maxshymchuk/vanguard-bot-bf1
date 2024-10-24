common_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

available_nickname_symbols = f'{common_symbols}-_'
available_weapon_symbols = f'{common_symbols}-/'

# add any error combination tesseract find to fix a word (use only restricted symbols as keys)
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