# ML with DAGs
#
Dagster is a data orchestrator for machine learning, analytics, and ETL.
It lets you define pipelines in terms of the data flow between reusable, logical components, then test locally and run anywhere. With a unified view of pipelines and the assets they produce, Dagster can schedule and orchestrate Pandas, Spark, SQL, or anything else that Python can invoke. It makes testing easier and deploying faster.
This application is a simple text classifier using sklearn.

The script creates a single pipeline which:
	-processes the data, 
	-searches for optimal parameters between a logistic regression and a random forest,
	-train and test the model
  
