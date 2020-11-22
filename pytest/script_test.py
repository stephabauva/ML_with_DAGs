from dagster import execute_pipeline, execute_solid
from config_dagit import *

import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug(sys.path)
from context import script
from script import *



if __name__ == "__main__":
    result = execute_pipeline(my_pipeline)
    assert result.success

# run_config = {
#     "solids": {
#         "open_csv": {"inputs": {"csv_path": {"value": "data/raw/comments_train.csv"}}}
#     }
# }

def test_create_dataframe():
    res = execute_solid(create_dataframe,run_config=config_create_dataframe)
    assert res.success

def test_label_data():
    res = execute_solid(label_data, run_config=config_label_data)
    assert res.success