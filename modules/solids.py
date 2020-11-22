from dagster import execute_pipeline, pipeline, solid
import os 
import yaml
import pandas as pd
import sklearn #pipenv install scikit-learn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.DEBUG)
#for production: logging.basicConfig(level=logging.WARNING)

@solid
def create_dataframe(context, csv_path:str):
    df = pd.read_csv(csv_path)
    logging.debug(f"\n{df.describe()}")
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
    logging.debug(f"\n{df.label.value_counts()}")
    return df

@solid
def get_y_encoded(context,df):
    y = df['label']
    return y

@solid
def vectorize_text(context, df):
    x = df['comment']
    X = CountVectorizer().fit_transform(x).todense()
    return X

@solid
def train_test(context, X,y):
    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.20)
    logging.debug(f'\nx_train, y_train: {len(x_train)}, {len(y_train)},\nx_test, y_test: {len(x_test)}, {len(y_test)}')
    return x_train, x_test, y_train, y_test