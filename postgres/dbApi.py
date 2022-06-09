from database import SessionLocal
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
