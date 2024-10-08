available_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-'

# add any error combination tesseract find to fix a word (use only restricted symbols as keys)
replaceable = {
    '|': 'I',
    '€': 'e',
    '><': 'x'
}

def replace_wrong_symbols(str: str) -> str:
    for substr in replaceable.keys():
        str = str.replace(substr, replaceable[substr])
    return str

def remove_restricted_symbols(str: str) -> str:
    for letter in str:
        if not letter in available_symbols:
            str = str.replace(letter, '')
    return str