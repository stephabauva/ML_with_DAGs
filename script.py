#!/usr/bin/python3
# import requests

# response = requests.get('https://httpbin.org/ip')

# print('Your IP is {0}'.format(response.json()['origin']))
from dagster import execute_pipeline, pipeline, solid
from modules.solids import *
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# print(os.getcwd() == os.path.join(os.path.dirname(__file__))) #True 

@pipeline
def my_pipeline():
    # train_test_split(vectorize_text(get_xy(label_data(create_dataframe(open_csv())))))
    df = label_data(create_dataframe())
    train_test(vectorize_text(df),get_y_encoded(df))

if __name__ == "__main__":
    #read raw data
    execute_pipeline(my_pipeline)

        