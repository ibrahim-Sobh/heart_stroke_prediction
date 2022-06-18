from database import SessionLocal
from sqlalchemy import or_,and_
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
    return DB.query(Patient).filter(and_(Patient.firstname.ilike("%"+first_name+"%"),
                                        Patient.lastname.ilike("%"+last_name+"%"))).all()
    
def  get_patient_by_date (filename:str, date: str) -> Patient:
    """_summary_
    Get a patient from the patients table

    Args:
        filename (str): _description_
        date (str): _description_

    Returns:
        models.Patient: _description_
    """
    q = DB.query(Patient).outerjoin(Record).filter(Record.id == Patient.record_id,
                                                   Record.file_name == filename).filter(Record.createdon == date)
  
   