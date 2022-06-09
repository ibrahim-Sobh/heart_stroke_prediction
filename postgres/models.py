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
    prediciton =Column(Boolean, default=False)
    records =relationship('Record')
    
class Record(Base):
    __tablename__ ='record'
    id= Column(Integer,primary_key=True,autoincrement=True, nullable=True)
    file_name=Column(Text,nullable=True)
    doctor_first_name=Column(Text,nullable=True)
    doctor_last_name=Column(Text,nullable=True)
    createdon=  Column(DateTime(timezone=True), server_default=func.now())
