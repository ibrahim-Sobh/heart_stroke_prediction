import pandas as pd
import json
from datetime import date

import requests

# Interact with FastAPI endpoint
import load_config as config
BACKEND_SERVER = config.get_backend_connection_server()

# Make Predictions Section


def get_prediction(features: dict) -> int:
    """_summary_
    Takes users Input from User Interface returns a Singular Prediction
    Returns:
        _type_: _description_
    """
    url = BACKEND_SERVER + "predict"
    response = requests.get(url, json=features)
    if response.status_code == 200:
        results = response.json()
        prediction = results["prediction"]
        return prediction
    else:
        print(response.status_code)
        return pd.DataFrame([])


def get_prediction_document(filename: str, data: pd.DataFrame) -> pd.DataFrame:
    """_summary_
     Takes File Input from User Interface returns a Prediction Dataframe
    Args:
        data (pd.DataFrame): _description_
    """
    data = data_frame_fix_column_with_Nan_float(data)
    list_of_json = data.to_dict(orient='records')
    data_json = dict()
    data_json["record"] = {"id": 0, "file_name": filename}
    data_json["patient"] = list_of_json
    url = BACKEND_SERVER + "predict_multiple"
    response = requests.get(url, json=data_json)
    if response.status_code == 200:
        result = json.loads(response.content)
        prediction_df = pd.read_json(result, orient='index')
        data["prediction"] = prediction_df["prediction"]
        return data, True
    elif response.status_code == 422:
        return "File is Not withint the Correct Format !", False
    else:
        return pd.DataFrame([]), True


def data_frame_fix_column_with_Nan_float(data):
    """_summary_
    Fix Nan_float issues in dataframe , Pydantic model doesn't like
    Nan's in Float columns Json Encoder doesnt like to deal
    with Nan's in Float columns
    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    float_cols = data.select_dtypes(include=['float64', 'int64']).columns
    str_cols = data.select_dtypes(include=['object']).columns
    data.loc[:, float_cols] = data.loc[:, float_cols].fillna(0.0)
    data.loc[:, str_cols] = data.loc[:, str_cols].fillna('')
    return data

# Data Base Services


def search_patient_by_fullname(first_name: str,
                               last_name: str) -> pd.DataFrame:
    """_summary_
    Search patient records by full name
    Args:
        first_name (str): _description_
        last_name (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    url = BACKEND_SERVER + "search/patient/{firstname}&{lastname}"\
        .format(firstname=first_name if len(first_name) else "%%",
                lastname=last_name if len(last_name) else "%%",)
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        return results
    else:
        return pd.DataFrame([])


def search_patient_by_window_period(from_date: date,
                                    to_date: date) -> pd.DataFrame:
    """_summary_
    Search patient records by Window Period
    Args:
        from_date (date): _description_
        to_date (date): _description_

    Returns:
        pd.DataFrame: _description_
    """
    url = BACKEND_SERVER + "search/patient/period/{fromdate}&{todate}"\
        .format(fromdate=from_date.strftime("%Y-%m-%d"),
                todate=to_date.strftime("%Y-%m-%d"))
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        return results
    else:
        return pd.DataFrame([])


def search_patients_file_by_date(file_name: str,
                                 created_on: date) -> pd.DataFrame:
    """_summary_
    Search File Patients records by Date Created On
    Args:
        file_name (str): _description_
        created_date (date): _description_

    Returns:
        pd.DataFrame: _description_
    """
    url = BACKEND_SERVER + "search/file/{filename}&{createdon}"\
        .format(filename=file_name, createdon=created_on.strftime("%Y-%m-%d"))
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        if results is not None:
            return results
        else:
            return pd.DataFrame([])
    else:
        return None
