from dagster import execute_pipeline, pipeline, solid, composite_solid
import os 
import yaml
import pandas as pd
import sklearn #pipenv install scikit-learn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


import logging
logging.basicConfig(level=logging.DEBUG)
#for production: logging.basicConfig(level=logging.WARNING)

##### data prrocessing #####
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

##### Training and evaluation #####
@solid
def split_data(context, X,y):
    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.20)
    # logging.debug(f"\nx_train, y_train: {len(x_train)}, {len(y_train)},\nx_test, y_test: {len(x_test)}, {len(y_test)}")
    # logging.debug(f"\nx_train, y_train: {}, {},\nx_test, y_test: {}, {}".format(len(x_train), len(y_train), len(x_test), len(y_test)))
    # logging.debug(f"\nx_train, y_train: %d, %d,\nx_test, y_test: %d, %d" % (len(x_train), len(y_train), len(x_test), len(y_test)))
    train_test_data = [x_train, y_train, x_test, y_test]
    logging.debug(train_test_data)
    return train_test_data

@solid
def prepare_grid_search(context, param_grid):
    unoptimized_model = RandomForestClassifier(random_state=30)
    # param_grid = {'n_estimators': [5, 10],
    #                   'max_features': ['auto'],
    #                   'max_depth' : [1,2]}
    model = GridSearchCV(unoptimized_model, param_grid) #param_grid=grid2, cv= 5
    return model

@solid
def train_model(context,train_test_data,model):
    x_train = train_test_data[0]
    y_train = train_test_data[1]
    logging.debug(x_train,y_train)
    trained_model = model.fit(x_train, y_train)
    return trained_model


@solid
def evaluate_model(context, trained_model,train_test_data):
    x_test = train_test_data[2]
    y_test = train_test_data[3]
    y_pred = trained_model.predict(x_test)
    logging.info(f"\n{classification_report(y_test, y_pred)}")

@composite_solid
def process_model(train_test_data, model):
    return evaluate_model(train_model(train_test_data, model),train_test_data)