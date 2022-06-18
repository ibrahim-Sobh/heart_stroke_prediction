# Strokes and Heart Failure Predictions Model

## Users :
* Medical professionals
* Clinics / hospitals
* Medical devices

## Usage Description:

* After providing the necessary information to the health professionals of the user or inputting his or her personal & health information on the medical device.
Our model will use the the information provided by the user above to predict the probability of him having a stroke. 
After it will display a detailed result about the patient status and possible precautions or advices to visit a professional

## Chosen features:
Our application will use both :
* Data ingestion and data ingestion to collect our data based on the user inputs.
* Pipeline retraining,  to retrain our model to make it even more accurate ( we are talking about heart failure and predictions so our model needs highly critical.)


## Dataset: 
* 11 clinical features for predicting stroke events:
https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset
* Heart Failure Prediction:
https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction

## Postgres Database Setup :

1. Make sure to install database dependencies [psycopg2, python-dotenv, sqlalchemy],check stroke_heart_prediciton/requirements.txt
2. Create a (.env) file in the main Root =>  stroke_heart_prediciton/.env
3. (.env) File Should Contain:
```
POSTGRES_USER=[User]
POSTGRES_PASSWORD=[Password]
POSTGRES_SERVER=[Server]
POSTGRES_PORT=[Port]
POSTGRES_DB=[Database]

```
4. Open terminal and go to Cd stroke_heart_prediciton/postgres 
5. Run Python createdb.py to create the tables & relationships in your database

## Execute Program:

1. uvicorn  main:app --host 0.0.0.0 --port 8000

2. streamlit run web_interface.py


![Screenshot 2022-04-27 at 6 56 27 PM](https://user-images.githubusercontent.com/49615833/165579996-2b784dfc-404d-40c8-99ee-c8ec92497faa.png)
