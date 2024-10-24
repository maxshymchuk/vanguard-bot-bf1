import pytesseract
import numpy as np
from modules.utils import replace_wrong_symbols, remove_restricted_symbols
from modules.utils import available_symbols
# from tensorflow.keras.models import load_model

# we need to train the model for weapon icons
# model = load_model('image_recognition_model.h5')

def recognize_text(image) -> list:
    text = pytesseract.image_to_string(image, lang = 'eng', config = f'--psm 7 --oem 3 -c tessedit_char_whitelist={available_symbols}')
    words = text.strip().split(' ') # string cleanup and split to array
    words = map(replace_wrong_symbols, words) # replace error combinations, must be before removing restricted symbols
    words = map(remove_restricted_symbols, words) # allow only available symbols
    words = filter(None, words) # filter out empty strings
    return list(words) or []

def recognize_image(image):
    img = image.resize((32, 32))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    # prediction = model.predict(img_array)
    # print(np.argmax(prediction))
    # return np.argmax(prediction)