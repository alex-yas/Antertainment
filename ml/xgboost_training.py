import pickle

from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import pandas as pd

if __name__ == '__main__':
    datasets = {
        'train': pd.read_csv('../data/train.csv'),
        'test': pd.read_csv('../data/test.csv')
    }

    targets = {
        data_type: data['target']
        for data_type, data in datasets.items()
    }

    features = {
        data_type: data.drop(columns=['target'])
        for data_type, data in datasets.items()
    }

    clf = XGBClassifier()
    clf.fit(features['train'], targets['train'])
    targets['pred'] = clf.predict(features['test'])

    print(classification_report(targets['test'], targets['pred']))
    file = open('ml_models/xgb_clf.pkl', 'wb')
    pickle.dump(clf, file)
