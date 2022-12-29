import argparse
import os

from scipy.stats import truncnorm
import numpy as np
import pandas as pd
import torch

from ant_api.yolo import yolo_detect_img


def get_normal_distribution(mean, low, upp, sd=1, num_samples=1000):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd).rvs(num_samples)


def get_probabilities_distribution(probabilities: list, num_samples=1000):
    num_values = len(probabilities)
    return [np.random.choice(np.arange(num_values), p=probabilities) for i in range(num_samples)]


if __name__== '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_path')
    args = parser.parse_args()

    niger_size = get_normal_distribution(mean=8.75, low=7.5, upp=10)
    niger_date = get_normal_distribution(mean=7.5, low=5, upp=10, sd=2).round().astype(int)
    niger_paunch = get_probabilities_distribution([0.9, 0.09, 0.01])
    niger_thorax = get_probabilities_distribution([0.9, 0.09, 0.01])
    niger_place = get_probabilities_distribution([0.2, 0.3, 0.3, 0.15, 0.05])

    flavus_size = get_normal_distribution(mean=8.35, low=7.2, upp=9.5)
    flavus_date = get_normal_distribution(mean=7.5, low=5, upp=10, sd=2).round().astype(int)
    flavus_place = get_probabilities_distribution([0.2, 0.3, 0.3, 0.15, 0.05])
    flavus_paunch = get_probabilities_distribution([0.01, 0.05, 0.94])
    flavus_thorax = get_probabilities_distribution([0.01, 0.05, 0.94])

    vagus_size = get_normal_distribution(mean=14.5, low=13, upp=16)
    vagus_date = get_normal_distribution(mean=2.5, low=1, upp=4, sd=2).round().astype(int)
    vagus_place = get_probabilities_distribution([0.4, 0.45, 0.05, 0.05, 0.05])
    vagus_paunch = get_probabilities_distribution([0.97, 0.02, 0.01])
    vagus_thorax = get_probabilities_distribution([0.97, 0.02, 0.01])

    herculeanus_size = get_normal_distribution(mean=16, low=14, upp=18)
    hercualeanus_time = get_normal_distribution(mean=4, low=3, upp=5, sd=2).round().astype(int)
    herculeanus_place = get_probabilities_distribution([0.45, 0.4, 0.05, 0.05, 0.05])
    herculeanus_paunch = get_probabilities_distribution([0.97, 0.02, 0.01])
    herculeanus_thorax = get_probabilities_distribution([0.04, 0.95, 0.01])

    size = np.concatenate([niger_size, flavus_size, vagus_size, herculeanus_size])
    place = np.concatenate([niger_place, flavus_place, vagus_place, herculeanus_place])
    paunch = np.concatenate([niger_paunch, flavus_paunch, vagus_paunch, herculeanus_paunch])
    thorax = np.concatenate([niger_thorax, flavus_thorax, vagus_thorax, herculeanus_thorax])

    niger_images = ['../data/test/lasius_niger/' + img_name for img_name in
                    os.listdir('../data/test/lasius_niger')]
    flavus_images = ['../data/test/lasius_flavus/' + img_name for img_name in
                     os.listdir('../data/test/lasius_flavus')]
    vagus_images = ['../data/test/camponotus_vagus/' + img_name for img_name in
                    os.listdir('../data/test/camponotus_vagus')]
    herculeanus_images = ['../data/test/camponotus_herculeanus/' + img_name for img_name in
                          os.listdir('../data/test/camponotus_herculeanus')]


    weights = '/home/a.yasinetski/PycharmProjects/Study/Antertainment/ml/ml_models/last.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights, force_reload=True)
    pathes = [herculeanus_images, vagus_images, flavus_images, niger_images]
    results = []
    for images_path in pathes:
        results.append(model(images_path))

    classes = []
    for result in results:
        annotations = result.pandas().xyxy
        cur_classes = []

        for annotation in annotations:
            values, counts = np.unique(annotation['class'].values, return_counts=True)
            if annotation['class'].values.size !=0:
                cur_classes.append(values[counts.argmax()])

        cur_classes = np.array(cur_classes)
        while cur_classes.shape[0] < 1000:
            cur_classes = np.concatenate([cur_classes, cur_classes])
        else:
            cur_classes = cur_classes[:1000]

        classes.append(cur_classes)

    classes = np.concatenate(classes)
    targets = np.concatenate([np.full(1000, 0), np.full(1000, 1), np.full(1000, 2), np.full(1000, 3)])

    out = pd.DataFrame({'thorax': thorax, 'paunch': paunch, 'size': size, 'predict': classes, 'target': targets})
    out.to_csv('../data/test.csv', index=False)
