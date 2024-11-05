from imageai.Classification.Custom import CustomImageClassification
import json
import numpy as np
import os

weight_file_name = "models/resnet50-bf1ai-test_acc_0.99896_epoch-86.pt"
json_file_name = "models/bf1ai_model_classes.json"
number_of_classes = 0

prediction = None

def load_model():
    global number_of_classes, prediction
    prediction = CustomImageClassification()
    prediction.setModelTypeAsResNet50()
    dir = os.getcwd()
    prediction.setModelPath(os.path.join(dir, weight_file_name))
    prediction.setJsonPath(os.path.join(dir, json_file_name))
    prediction.loadModel()

    with open(json_file_name) as f:
        classes = json.load(f)
        number_of_classes = len(classes.keys())

def predict_icon(image):
    return prediction.classifyImage(image, result_count=number_of_classes)