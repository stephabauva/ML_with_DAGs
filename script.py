#!/usr/bin/python3
from dagster import execute_pipeline, pipeline, solid, repository
from modules.solids import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

@pipeline
def data_pipeline():
    df = create_dataframe()
    training_data, testing_data = split_data(vectorize_text(df),encode_label(df))
    #The parts below could eventually be a second pipeline. if so, just comment the rest of this function, i.e. from line 14 to line 19. 
    #for rf
    grid1 = prepare_grid.alias('prepare_grid_random_forest')
    #for log reg
    grid2 = prepare_grid.alias('prepare_grid_logistic_regression')

    process_model(training_data, testing_data, grid1())
    process_model(training_data, testing_data,grid2())
    
# If you want to create two pipelines: data preprocessing + Grid/train/test, uncomment the following block.
# @pipeline
# def train_evaluate_pipeline(train_test_data):
    ##for more info on reusable solids -> see https://docs.dagster.io/tutorial/advanced_solids#reusable-solids

    ##create aliases to apply different parameters where reusing a solid, i.e. grid_searCV()
    # optimized_model1 = grid_search.alias('prepare_grid_random_forest')
    # unoptimized_model = LogisticRegression(random_state=31)
    # optimized_model2 = grid_searchCV(unoptimized_model).alias('prepare_grid_logistic_regression')
    # #call the composite solids
    # process_model(train_test_data,optimized_model1())
    # process_model(train_test_data,optimized_model2())
    
#You can also create a repository within Dagster that will contain the two pipelines:
# @repository
# def my_repository():
#     return [data_pipeline, train_evaluate_pipeline]


if __name__ == "__main__":
    execute_pipeline(data_pipeline)
    #for the second pipeline, uncomment:
    # execute_pipeline(train_evaluate_pipeline)

        
