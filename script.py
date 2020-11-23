#!/usr/bin/python3
# import requests

# response = requests.get('https://httpbin.org/ip')

# print('Your IP is {0}'.format(response.json()['origin']))
from dagster import execute_pipeline, pipeline, solid, repository
from modules.solids import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# print(os.getcwd() == os.path.join(os.path.dirname(__file__))) #True 

@pipeline
def data_pipeline():
    # train_test_split(vectorize_text(get_xy(label_data(create_dataframe(open_csv())))))
    df = label_data(create_dataframe())
    train_test_data = split_data(vectorize_text(df),get_y_encoded(df))
    grid1 = prepare_grid_search()
    # process_model1 = process_model.alias('process_random_forest')
    process_model(train_test_data,grid1)

# @pipeline
# def train_evaluate_pipeline(train_test_data):
    #fro reusable solids -> see https://docs.dagster.io/tutorial/advanced_solids#reusable-solids

    ##create aliases to apply different parameters where reusing a solid, i.e. grid_searCV()
    # optimized_model1 = grid_search.alias('grid_search_random_forest')
    # unoptimized_model = LogisticRegression(random_state=31)
    # optimized_model2 = grid_searchCV(unoptimized_model).alias('grid_search_logistic_regression')
    # #call the composiet solids
    # process_model(train_test_data,optimized_model1())
    # process_model(train_test_data,optimized_model2())

# @repository
# def my_repository():
#     return [data_pipeline, train_evaluate_pipeline]


if __name__ == "__main__":
    execute_pipeline(data_pipeline)
    # execute_pipeline(train_evaluate_pipeline)

        