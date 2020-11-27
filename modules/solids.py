from dagster import execute_pipeline, pipeline, solid, composite_solid, OutputDefinition, Output, Any
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
import joblib
import sys


#go one folder above and add the path to sys where /models is, to save the trained model
# os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

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
def encode_label(context, df):
    #function to encode the sentiment into 0 or 1
    def encode(sentiment):
        if sentiment == 'Positive':
            return 1
        elif sentiment == 'Negative':
            return 0
    df['label'] = df['sentiment'].map(encode)
    logging.debug(f"\n{df.label.value_counts()}")
    y = df['label']
    return y

@solid
def vectorize_text(context, df):
    x = df['comment']
    vectorizer = CountVectorizer()
    X = CountVectorizer().fit_transform(x).todense()
    joblib.dump(vectorizer,'tmp/vectorizer.pkl')
    return X

##### Training and evaluation #####
@solid(
    output_defs=[
        OutputDefinition(name='train', dagster_type=Any, is_required=True),
        OutputDefinition(name='test', dagster_type=Any, is_required=True),
    ],
)
def split_data(context, X,y):
    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.20)
    # train_test_data = [x_train, y_train, x_test, y_test]
    training_data = [x_train, y_train]
    testing_data = [x_test, y_test]
    joblib.dump(training_data,'data/processed/training_data.pkl')
    joblib.dump(testing_data,'data/processed/testing_data.pkl')
    logging.debug('training and testing data saved in /data/processed')
    # logging.debug(train_test_data)
    yield Output(training_data, 'train')
    yield Output(testing_data, 'test') 

@solid
def prepare_grid(context, key, param_grid):
    # If you want to use a switch pattern design instead of making the paramameter string callable:
    # models = {'rf': RandomForestClassifier(random_state=30),
    #         'reg': LogisticRegression(random_state=31)}
    # if key == 'RandomForestClassifier':
    #     unoptimized_model = models['RandomForestClassifier']
    # elif key == 'LogisticRegression':
    #     unoptimized_model = models['LogisticRegression']

    #make a string callable
    unoptimized_model = eval(key)() 
    grid = GridSearchCV(unoptimized_model, param_grid)
    return grid
    
@solid
def get_best_estimator(context,training_data, grid):
    logging.info(f"grid:\n{grid}")
    x_train = training_data[0]
    y_train = training_data[1]
    logging.debug([x_train, y_train]) #seems that logging.* only takes one argyment, otherwise raises TypeError: not all arguments converted during string formatting
    #fit the data to the grid and search for best parameters
    search = grid.fit(x_train, y_train)
    logging.info(f"best params:\n{search.best_params_}")
    #apply best parameters to the base model
    model = search.best_estimator_
    return model

@solid
def train_model(context, training_data, model):
    x_train = training_data[0]
    y_train = training_data[1]
    #fit model to data
    trained_model = model.fit(x_train, y_train)
    #save model
    joblib.dump(trained_model, 'models/'+ str(trained_model.__eq__).split(' ')[3]+ '.pkl')
    logging.debug("model saved in /models")
    return trained_model

@solid
def evaluate_model(context, testing_data, trained_model):
    x_test = testing_data[0]
    y_test = testing_data[1]
    y_pred = trained_model.predict(x_test)
    logging.info(f"\n{trained_model}:\n{classification_report(y_test, y_pred)}")

@composite_solid
def process_model(training_data, testing_data, prep_grid):
    return evaluate_model(testing_data, train_model(training_data, get_best_estimator(training_data, prep_grid)))