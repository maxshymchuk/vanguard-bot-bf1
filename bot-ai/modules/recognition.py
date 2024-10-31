import pytesseract
import numpy as np
from .utils import replace_wrong_symbols, remove_restricted_symbols, common_symbols

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def recognize_text(image, lang = 'eng', available_symbols: str | None = common_symbols) -> str:
    text: str = pytesseract.image_to_string(image, lang=lang, config = f'--psm 7 --oem 3 -c tessedit_char_whitelist={available_symbols}')
    words = text.strip() # string cleanup
    words = replace_wrong_symbols(words) # replace error combinations, must be before removing restricted symbols
    words = remove_restricted_symbols(words, available_symbols) # allow only available symbols
    return words or None

def recognize_image(image):
    img = image.resize((32, 32))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    # prediction = model.predict(img_array)
    # print(np.argmax(prediction))
    # return np.argmax(prediction)