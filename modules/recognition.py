import pytesseract
import numpy as np
# from tensorflow.keras.models import load_model

# we need to train the model for weapon icons
# model = load_model('image_recognition_model.h5')

def recognize_text(image):
    text = pytesseract.image_to_string(image)
    print(text)
    return text

def recognize_image(image):
    img = image.resize((32, 32))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    # prediction = model.predict(img_array)
    # print(np.argmax(prediction))
    # return np.argmax(prediction)