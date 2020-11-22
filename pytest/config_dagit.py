# from dagster import execute_solid
# from script import *
import pandas as pd

config_create_dataframe = {
    "solids": {
        "create_dataframe": {
            "inputs": {
                "csv_path": {"value": "data/raw/comments_train.csv"}
            }
        }
    }
}

#create fataframe for test on solid 'label_data' 
col = ['sentiment']
data = [ 'Positive','Negative','Positive']
df = pd.DataFrame(data, columns=col)

config_label_data = {
    "solids": {
        "label_data":{
            "inputs":{
                "df":{"value": df}
            }
        }
    }
}
# print(config_open_csv)
# print(config_create_dataframe )
# result = execute_pipeline(my_pipeline, run_config=run_config)