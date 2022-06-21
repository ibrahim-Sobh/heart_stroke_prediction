from datetime import datetime
from venv import create
from database import SessionLocal
from sqlalchemy import or_,and_, extract
from models import Patient, Record
from typing import List

DB = SessionLocal()


def create_record(new_record:Record) -> int:
    """_summary_
    Insert a record into the records table

    Args:
        new_record (models.Record): _description_

    Returns:
        int: record id
    """
    DB.add(new_record)
    DB.flush()
    DB.commit()
    return new_record.id


def insert_patient(new_patient:Patient) -> int:
    """_summary_
    Insert a patient into the patients table

    Args:
        new_patient (models.Patient_in_db): _description_

    Returns:
        int: patient 
    """
    DB.add(new_patient)
    DB.flush()
    DB.commit()
    return new_patient



def insert_patients(list_of_patients: List[Patient]) -> int:
    """_summary_
    Insert a list of patients into the patients table

    Args:
        new_patient (models.Patient_in_db): _description_

    Returns:
        int: List[Patients]
    """
    DB.add_all(list_of_patients)
    DB.commit()
    return list_of_patients 

def get_patient_by_full_name(first_name: str, last_name: str) -> List[Patient]:
    """_summary_
    Get a patient from the patients table

    Args:
        first_name (str): _description_
        last_name (str): _description_

    Returns:
        models.Patient: _description_
    """
    return DB.query(Patient).outerjoin(Record).filter(Record.file_name== "-",
                                                      and_(Patient.firstname.ilike("%"+first_name+"%"),
                                                           Patient.lastname.ilike("%"+last_name+"%"))).all()
        
def get_patients_by_window_period(filter :dict) -> List[Patient]:
    """_summary_

    Args:
        filter (dict): _description_

    Returns:
        List[Patient]: _description_
    """
    return DB.query(Patient).outerjoin(Record).filter(Record.file_name== "-",
                                                        extract('year', Record.createdon).between(filter["from_year"],(filter["to_year"])),
                                                        extract('month', Record.createdon).between(filter["from_month"],(filter["to_month"])),
                                                        extract('day', Record.createdon).between(filter["from_day"],(filter["to_day"])),).all()
       

def get_patients_file_by_date (filename:str, year: int, month:int, day :int) -> Patient:
    """_summary_
    Get a patient from the patients table

    Args:
        filename (str): _description_
        date (str): _description_

    Returns:
        models.Patient: _description_
    """
    file_header =DB.query(Record).filter(Record.file_name.ilike("%"+filename+"%",),
                                         Record.doctor_first_name== "N/A",Record.doctor_last_name== "N/A",
                                                      extract('year', Record.createdon) == year,
                                                        extract('month', Record.createdon) == month,
                                                        extract('day', Record.createdon)==day).first()
    if file_header is None:
        return None
    id =file_header.id
    # left join to get all the records for the patient
    return DB.query(Patient).outerjoin(Record).filter(Record.id==id).all()


    
  
   