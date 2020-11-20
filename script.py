#!/usr/bin/python3
# import requests

# response = requests.get('https://httpbin.org/ip')

# print('Your IP is {0}'.format(response.json()['origin']))
from dagster import execute_pipeline, pipeline, solid
import os 
import yaml
import pandas as pd
import sklearn #pipenv install scikit-learn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
# print(os.getcwd() == os.path.join(os.path.dirname(__file__))) #True
@solid
def open_csv(context, csv_path):
    #define the root path of the project, based on this file location
    # root = os.path.dirname(__file__)
    # #open config file
    # with open('config.yml', 'r') as f:
    #     config = yaml.load(f, Loader = yaml.BaseLoader)
    #define location of raw data
    #raw_data = os.path.join(root,config['solids']['read_csv']['inputs']['csv_path']['value'])
    f = open(csv_path, "r")
    return f

@solid
def create_dataframe(context, data):
    df = pd.read_csv(data)
    return df

@solid
def label_data(context, df):
    #function to encode the sentiment into 0 or 1
    def encode(sentiment):
        if sentiment == 'Positive':
            return 1
        elif sentiment == 'Negative':
            return 0
    df['label'] = df['sentiment'].map(encode)
    return df

@solid
def get_xy(context,df):
    x = df['comment']
    y = df['label']
    print(x)
    return x,y

@solid
def vectorize_text(context, xy):
    x = xy[0]
    X = CountVectorizer().fit_transform(x).todense()
    return X, xy

@solid
def train_test(context, Xxy):
    y = Xxy[1][1]
    X = Xxy[0]
    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.20)
    print(f'x_train, y_train: {len(x_train)}, {len(y_train)}')
    print(f'x_test, y_test: {len(x_test)}, {len(y_test)}')
    return x_train, x_test, y_train, y_test 

@pipeline
def my_pipeline():
    # train_test_split(vectorize_text(get_xy(label_data(create_dataframe(open_csv())))))
    train_test(vectorize_text(get_xy(label_data(create_dataframe(open_csv())))))

if __name__ == "__main__":
    #read raw data
    execute_pipeline(my_pipeline)

        