from matplotlib.pyplot import text
from database import Base
from sqlalchemy import DateTime,String,Boolean,Integer,Float,Column,Text
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import  relationship


class Patient(Base):
    __tablename__ ='patient'
    id= Column(Integer,primary_key=True,autoincrement=True, nullable=True)
    record_id=Column(Integer,ForeignKey("record.id"))
    firstname= Column(String(35),nullable=False)
    lastname= Column(String(35),nullable=False)
    gender = Column(String(8),nullable=False)
    age = Column(Float,nullable=False)
    hypertension= Column(Boolean, default=False)
    heart_disease= Column(Boolean, default=False)
    ever_married= Column(String(35),nullable=False)
    work_type=  Column(String(35),nullable=False)
    Residence_type=  Column(String(35),nullable=False)
    avg_glucose_level=Column(Float,nullable=False)
    bmi= Column(Float,nullable=False)
    smoking_status= Column(String(35),nullable=False)
    prediction =Column(Boolean, default=False)
    records =relationship('Record')
    
class Record(Base):
    __tablename__ ='record'
    id= Column(Integer,primary_key=True,autoincrement=True, nullable=True)
    file_name=Column(Text,nullable=True)
    doctor_first_name=Column(Text,nullable=True)
    doctor_last_name=Column(Text,nullable=True)
    createdon=  Column(DateTime(timezone=True), server_default=func.now())



class Data_ingested(Base):
    __tablename__ ='data_ingested'
    id = Column(Integer, primary_key=True,autoincrement=True, nullable=True)
    firstname = Column(String(35), nullable=True)
    lastname = Column(String(35), nullable=True)
    gender = Column(String(8), nullable=True)
    age = Column(Float, nullable=True)
    hypertension = Column(Boolean, default=True)
    heart_disease = Column(Boolean, default=True)
    ever_married = Column(String(35), nullable=True)
    work_type =  Column(String(35), nullable=True)
    Residence_type =  Column(String(35), nullable=True)
    avg_glucose_level = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    smoking_status = Column(String(35), nullable=True)
    prediction = Column(Boolean, default=True)
    quality = Column(Boolean, default=True)
    datetime = Column(DateTime(timezone=True), server_default=func.now())