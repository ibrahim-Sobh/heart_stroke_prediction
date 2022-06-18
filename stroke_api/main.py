import sys
sys.path.insert(0,'../stroke_prediction')
sys.path.insert(0,'../postgres')

import pandas as pd

# ML API
from stroke_prediction.inference import make_prediction

#FastAPI
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from json import dumps
from typing import List
from datetime import datetime

# Postgres init
import dbApi as db
import models

# FastAPI init
app = FastAPI()


# BaseModels from FastAPI
class Patient(BaseModel):
    id: int
    firstname : str
    lastname : str
    gender: str
    age: float
    hypertension: int
    heart_disease: int
    ever_married: str
    work_type: str
    Residence_type: str
    avg_glucose_level:Optional[float] = 0.0
    bmi: Optional[float]=0.0
    smoking_status:str

    class Config:
        # Serialize our sql into json 
        orm_mode= True
        
class Patient_in_db(Patient):
    record_id :int
    prediction: int
        
class Record(BaseModel):
    id: Optional[int] = 0
    file_name: Optional[str] = "N/A"
    doctor_first_name:Optional[str] = "N/A"
    doctor_last_name:Optional[str] = "N/A"
    createdon: Optional[datetime] = datetime.now()

    class Config:
        # Serialize our sql into json 
        orm_mode= True
        
# Databse Calls
def save_patient_record(record:Record,patient:Patient,result)->int:
   
    new_record = models.Record(
          file_name=record.file_name,
          doctor_first_name=record.doctor_first_name,
          doctor_last_name=record.doctor_last_name,
          createdon= datetime.now()
    )
    
    record_id_in_db = db.create_record(new_record)
    patient_in_db = Patient_in_db(**patient.dict(), record_id=record_id_in_db,prediction= result)
    new_patient =models.Patient(
        record_id=patient_in_db.record_id,
        firstname=patient_in_db.firstname,
        lastname=patient_in_db.lastname,
        gender=patient_in_db.gender,
        age=patient_in_db.age,
        hypertension=patient_in_db.hypertension,
        heart_disease=patient_in_db.heart_disease,
        ever_married=patient_in_db.ever_married,
        work_type=patient_in_db.work_type,
        Residence_type=patient_in_db.Residence_type,
        avg_glucose_level=patient_in_db.avg_glucose_level,
        bmi=patient_in_db.bmi,
        smoking_status=patient_in_db.smoking_status,
        prediction = patient_in_db.prediction
        )
    result=db.insert_patient(new_patient)
    return result

def save_list_patients_record(record:Record,patients,prediction_results)->int:
   
    new_record = models.Record(
          file_name=record.file_name,
          doctor_first_name=record.doctor_first_name,
          doctor_last_name=record.doctor_last_name,
          createdon= datetime.now()
    )
    
    record_id_in_db = db.create_record(new_record)
    
    list_of_patients=[]
    for patient ,result  in zip(patients,prediction_results):
        new_patient =models.Patient(
            record_id=record_id_in_db,
            firstname=patient.firstname,
            lastname=patient.lastname,
            gender=patient.gender,
            age=patient.age,
            hypertension=patient.hypertension,
            heart_disease=patient.heart_disease,
            ever_married=patient.ever_married,
            work_type=patient.work_type,
            Residence_type=patient.Residence_type,
            avg_glucose_level=patient.avg_glucose_level,
            bmi=patient.bmi,
            smoking_status=patient.smoking_status,
            prediction =result
            )
        list_of_patients.append(new_patient)
    result=db.insert_patients(list_of_patients)
    return result


# ML Calls
def make_one_prediction(record:Record,patient: Patient)->dict:
    pd_dict = patient.dict()
    prediction_df= pd.DataFrame.from_dict([pd_dict])
    prediction_df.drop(['firstname','lastname'], axis = 1,inplace=True)
    prediction=int(make_prediction(prediction_df)[0])
    save_patient_record(record,patient,prediction)
    return {"prediction": prediction}

def make_mulitple_prediction(record:Record,patients: List[Patient]):
    records= [dict(patients[patienindex]) for patienindex in range(len(patients))]
    prediction_df= pd.DataFrame.from_records(records)
    prediction_df.drop(['firstname','lastname'], axis = 1,inplace=True)
    prediction_df["prediction"]=make_prediction(prediction_df)
    results = list(prediction_df["prediction"])
    save_list_patients_record(record,patients,results)
    return dumps(prediction_df.to_dict('index'))
    
@app.get("/")
def read_root():
    return {"message": "We are ready to go !"}

@app.get("/predcit")
async def predict(record:Record,patient: Patient):
    result= make_one_prediction(record,patient)
    return result

@app.get("/predcit_multiple")
async def predict_file(record:Record,patient: List[Patient]):
    print(record)
    result = make_mulitple_prediction(record,patient)
    return result

@app.get("/patient/search/{firstname}&{lastname}",response_model=List[Patient_in_db],status_code=200)
async def get_patient_by_name(firstname:str,lastname:str):
    patients= db.get_patient_by_full_name(firstname,lastname)
    return patients


@app.get("/patient/{patient_id}")
async def get_patient_by_id(item_id: int):
    pass
    
