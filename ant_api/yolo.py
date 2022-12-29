import pickle

import pandas as pd
import torch
from PIL import Image
import numpy as np

from model.ant_input import AntInput


def yolo_get_label(img_path):
    weights = '/home/a.yasinetski/PycharmProjects/Study/Antertainment/ml/ml_models/last.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights, force_reload=True)
    img = Image.open('static/' + img_path)
    results = model(img)
    img = results.render()[0]
    img = Image.fromarray(img)
    save_path = 'static/predict.jpg'
    img.save(save_path)
    annotation = results.pandas().xyxy[0]
    values, counts = np.unique(annotation['class'].values, return_counts=True)
    label = values[counts.argmax()]
    return label


def predict_label(img_path, ant_input: AntInput):
    color_coding = {'BLACK': 0,
                    'BROWN': 1,
                    'YELLOW': 2}

    clf = pickle.load(open('../ml/ml_models/xgb_clf.pkl', 'rb'))
    ant_info = pd.DataFrame({
        'thorax': [color_coding[ant_input.thorax_color]],
        'paunch': [color_coding[ant_input.paunch_color]],
        'size': [ant_input.length],
        'predict': [yolo_get_label(img_path)]
    })
    label = clf.predict(ant_info)[0]
    label_code ={
        0: 1,
        1: 0,
        2: 3,
        3: 2
    }
    return label_code[label]
