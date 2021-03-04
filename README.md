# ML with DAGs  ❄️
🙀 👉🏼 See a guided tour of Dagster and the DAG generated from this program at:

Dagster is a data orchestrator for machine learning, analytics, and ETL.
It lets you define pipelines in terms of the data flow between reusable, logical components, then test locally and run anywhere. With a unified view of pipelines and the assets they produce, Dagster can schedule and orchestrate Pandas, Spark, SQL, or anything else that Python can invoke. It makes testing easier and deploying faster 😎.

This application is a simple text classifier using sklearn.

- The script creates a single pipeline which:
	- processes the data, 
	- searches for optimal parameters between a logistic regression and a random forest,
	- train and test the model
  
![alt text](https://github.com/stephanBV/ML_with_DAGs/blob/main/img/dagster_pipeline_drawio.jpg)

Step 1. Clone this repository 👯‍♂️
```
git clone https://github.com/stephanBV/ML_with_DAGs.git
cd ML_with_DAGs
````
Step 2. Create a virtual environment 👾 (Optional) 
```
python3 -m virtualenv venv
source venv/bin/activate
```
Step 3. Install dependencies 
```
pip install -r requirements.txt
```
Step 4. Launch Dagster's UI 
```
python3 -m dagit -f script.py
```
Step 5. On the main page, at the top, click on Playground. 
![alt text](https://github.com/stephanBV/ML_with_DAGs/blob/main/img/playground.png)

Then, drag-and-drop the config.yml of the cloned repository to the Playground page.

Step 6. Click on Launch Execution at the bottom right of the Playground page.

Reminder:
For a guided tour of the UI with our application, you can head to a pretty article on Hackernoon: 

or check the pdf version in ./pdf/quick_start_with_ML_and_Dagster.pdf
