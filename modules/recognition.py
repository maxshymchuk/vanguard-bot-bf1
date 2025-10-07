import pytesseract
from .utils import replace_wrong_symbols, remove_restricted_symbols, common_symbols

pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'

def recognize_text(image, available_symbols: str | None = common_symbols) -> str:
    text: str = pytesseract.image_to_string(image, lang = 'bf1', config = f'--psm 7 --oem 3 -c tessedit_char_whitelist={available_symbols}')
    words = text.strip() # string cleanup
    words = replace_wrong_symbols(words) # replace error combinations, must be before removing restricted symbols
    words = remove_restricted_symbols(words, available_symbols) # allow only available symbols
    return words or None