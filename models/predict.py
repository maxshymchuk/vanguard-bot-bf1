import json
from PIL import Image
import onnxruntime as ort
import numpy as np
from models.preprocess import Preprocessor

weight_file_name = "models/bf1ai.onnx"
json_file_name = "models/bf1ai_model_classes.json"

class Classifier:
    def __init__(self):
        with open(json_file_name) as f:
            self.classes = json.load(f)
            self.number_of_classes = len(self.classes.keys())
        self.ort_session = ort.InferenceSession(weight_file_name)

        self.preprocesser = Preprocessor()
        print('Icon model loaded')

    def predict_icon(self, image):
        img = Image.fromarray(image).convert("RGB")
        img = self.preprocesser.preprocess(img)
        
        outputs = self.ort_session.run(None, {"input": img})
        exp_scores = np.exp(outputs[0] - np.max(outputs[0]))
        probabilities = exp_scores / np.sum(exp_scores)
        top_prediction = np.argmax(probabilities)
        return self.classes[str(top_prediction)], probabilities[0][top_prediction]