import pandas as pd
import numpy as np
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

import web_services as ws
import streamlit as st

# Make Predictions Services


def get_prediction() -> int:
    """_summary_
    Takes users Input from User Interface returns a Singular Prediction
    Returns:
        _type_: _description_
    """
    features = input_details_to_json()
    prediction = ws.get_prediction(features)
    if prediction is not None:
        return prediction
    else:
        st.error("An error occurred while getting the prediction!")


def get_prediction_document(filename: str, data: pd.DataFrame) -> pd.DataFrame:
    """_summary_
     Takes File Input from User Interface returns a Prediction Dataframe
    Args:
        data (pd.DataFrame): _description_
    """
    predictions_file, sucess = ws.get_prediction_document(filename, data)
    if not sucess:
        st.error(predictions_file)
        return pd.DataFrame([])
    elif predictions_file is not None:
        return predictions_file
    else:
        st.error("An error occurred while getting the file's predictions !")
        return predictions_file


def input_details_to_json() -> dict:
    """_summary_
    Takes Useer input and converts it to json format
    Returns:
        _type_: _description_
    """
    myform_json = {"record": {"id": 0,
                              "file_name": "-",
                              "doctor_first_name": doctor_first_name if len(doctor_first_name.strip()) else "N/A",
                              "doctor_last_name": doctor_last_name if len(doctor_last_name.strip()) else "N/A"},
                   "patient": {"id": 0,
                               "firstname": first_name,
                               "lastname": last_name,
                               "gender": gender,
                               "age": age,
                               "hypertension": 1 if hypertension == "yes" else 0,
                               "heart_disease": 1 if heart_disease == "yes" else 0,
                               "ever_married": ever_married,
                               "work_type": work_type,
                               "Residence_type": residence_type,
                               "avg_glucose_level": avg_glucose_level,
                               "bmi": bmi,
                               "smoking_status": smoking_status
                               }
                   }
    return myform_json


# Data Frame Stylers


def data_frame_style_color_neg(val):
    """_summary_
    Pandas Dataframe Styler
    Args:
        val (_type_): _description_

    Returns:
        _type_: _description_
    """
    color = 'red' if type(val) == str and val == "Risk of Stroke" else 'green'
    return 'color: %s' % color


def float_format(val):
    """_summary_
    Pandas Dataframe Styler
    Args:
        val (_type_): _description_

    Returns:
        _type_: _description_
    """
    return "{:.2f}".format(val)


def data_frame_style_display(data: pd.DataFrame) -> pd.DataFrame:
    """_summary_
    Pandas Dataframe Styler
    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["prediction"] = data["prediction"].apply(
        lambda x: "Risk of Stroke" if x == 1 else "Normal")
    data["age"] = data["age"].apply(lambda x: int(x))
    data["hypertension"] = data["hypertension"].apply(
        lambda x: "Yes" if x == 1 else "No")
    data["heart_disease"] = data["heart_disease"].apply(
        lambda x: "Yes" if x == 1 else "No")
    data["bmi"] = data["bmi"].map(float_format)
    data["avg_glucose_level"] = data["avg_glucose_level"].map(float_format)
    data.drop('record_id', axis=1, inplace=True, errors='ignore')
    data.drop('id', axis=1, inplace=True, errors='ignore')
    st.dataframe(data.style.applymap(
        data_frame_style_color_neg, subset=['prediction']))


# Data Base Services


def search_patient_by_fullname() -> pd.DataFrame:
    """_summary_
    Search for a patient by fullname
    Returns:
        _type_: _description_
    """
    search_results = ws.search_patient_by_fullname(search_patient_first_name,
                                                   search_patient_last_name)
    if search_results is not None:
        return search_results
    else:
        st.error("An error occurred while searching for Patient(s) Record(s)!")


def search_patient_by_window_period() -> pd.DataFrame:
    """_summary_
    Search patient records by Window Period
    Returns:
        pd.DataFrame: _description_
    """
    search_results = ws.search_patient_by_window_period(search_patient_from_date,
                                                        search_patient_to_date)
    if search_results is not None:
        return search_results
    else:
        st.error("An error occurred while searching for Patient(s) Record(s)!")


def search_patients_file_by_date() -> pd.DataFrame:
    """_summary_
    Search File Patients records by Date Created On
    Returns:
        _type_: _description_
    """
    search_results = ws.search_patients_file_by_date(search_file_name,
                                                     search_created_on)

    if search_results is not None:
        return search_results
    else:
        st.error("An error occurred while searching for Patient(s) Record(s)!")


# Form Validations

def validate_search_input_details() -> bool:
    """_summary_
    Validate Inputs from User Interface
    Returns:
        _type_: _description_
    """
    if option == 'Per Patient':
        if len(search_patient_first_name.strip()) == 0 and\
                len(search_patient_last_name.strip()) == 0:
            st.warning("First Name or Last Name is required to Search!")
            return False
    elif option == 'Window Period':
        if search_patient_from_date > search_patient_to_date:
            st.warning(
                "From Date should be strictly greater than To Date to Search!")
            return False
    elif option == 'Per file':
        if len(search_file_name.strip()) == 0:
            st.warning("File name is required to Search!")
            return False
        pattern = re.compile(r'^[a-zA-Z0-9_]+$')
        if not pattern.match(search_file_name):
            st.warning(
                "File name is not a match to the accepted format to Search!")
            return False
    return True


def validate_patient_input_details() -> bool:
    """_summary_
    Validate Patient Inputs from User Interface
    Returns:
        _type_: _description_
    """
    if len(first_name.strip()) == 0:
        st.warning("First Name is required to Add a Patient!")
        return False
    elif len(last_name.strip()) == 0:
        st.warning("Last Name is required to Add a Patient!")
        return False
    return True


# Web Interface Section
st.title("Heart Stroke Prediction")

# CSS Changes for Side Bar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 450px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 450px;
        margin-left: -450px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Singular Prediction Page Section
with st.sidebar.expander("Single Predictions"):
    with st.form(key='my_form', clear_on_submit=True):
        st.title("Patient Form")
        gender_list = np.array(["Male", "Female"])
        yes_no = np.array(["Yes", "No"])
        work_type_lit = np.array(
            ['Private', 'Self employed', 'Govt job', 'children', 'Never worked'])
        residence_type_list = np.array(['Urban', 'Rural'])
        first_name = st.text_input(label='First Name')
        last_name = st.text_input(label='Last Name')
        gender = st.radio("Select your Gender", gender_list)
        age = st.number_input(label='Age', min_value=0, step=1, max_value=150)
        hypertension = st.radio(
            "Did you had Hypertension in the past ?", yes_no)
        heart_disease = st.radio(
            "Did you had Heart Problem in the past ?", yes_no)
        ever_married = st.radio("Have you ever been married ?", yes_no)
        work_type = st.radio("What is your Work Type ?", work_type_lit)
        residence_type = st.radio(
            "What is your Living Environment?", residence_type_list)
        avg_glucose_level = st.number_input(
            label='Enter your Average Glucose Level', min_value=0.0, step=0.1)
        bmi = st.number_input(
            label='Enter your Body Mass Index (bmi)', min_value=0.0, step=0., format="%.2f")
        smoking_status = st.radio(
            "Do you Smoke ?", ('smoked', 'formerly smoked', 'Unknown'))
        doctor_first_name = st.text_input(label='Dc. First Name')
        doctor_last_name = st.text_input(label='Dc. Last Name')
        submit_button = st.form_submit_button(label='Predict')

if submit_button:
    if validate_patient_input_details():
        prediciton = get_prediction()
        message = f"{first_name} {last_name} You are at risk of a stroke !" if prediciton == 1 else f"{first_name} {last_name} You are safe to slay another day :)"
        message_color = 'red' if prediciton == 1 else 'green'
        st.markdown(
            f"<h3 style='text-align: left;color:{message_color}'> {(message)} </h3>", unsafe_allow_html=True)
        if prediciton == 1:
            link_to_visit = "Visit this website for more details on how to prevent Heart Strokes\nhttps://www.cdc.gov/stroke/prevention.htm"
            st.info(link_to_visit)

# File  Prediction Page Section
with st.sidebar.expander("Upload File for Predictions"):
    with st.form(key="predictions", clear_on_submit=True) as form:
        st.title("Select a File to Generate Predictions")
        uploaded_files = st.file_uploader("Choose a CSV file", type={"csv"})
        predict_button = st.form_submit_button("Submit")
        if uploaded_files:
            filename = uploaded_files.name

if predict_button:
    if uploaded_files:
        data = pd.read_csv(uploaded_files)
        data = get_prediction_document(filename, data)
        if data.shape[0] > 0:
            data_frame_style_display(data)
            st.success("Uploaded Successfully!")
    else:
        st.warning("Please Upload a CSV File")

# Prediction Retrival Page Section
with st.sidebar.expander("Retrieve Past Predictions"):
    button = None
    st.title("Select a Search Mode")
    option = st.selectbox('Search Mode', ('< Select Option >',
                          'Per Patient', 'Window Period', 'Per file'))

    with st.form(key="Retrieve patients predictions by full name", clear_on_submit=True) as form_1:

        # Per Patient Full Name Search
        if option == 'Per Patient':
            st.title("Patient Full Name")
            search_patient_first_name = st.text_input(label='First Name')
            search_patient_last_name = st.text_input(label='Last Name')
            button = st.form_submit_button("Get Patient Records")

        elif option == 'Window Period':
            st.title("Select a Window Period")
            search_patient_from_date = st.date_input(
                "From Date", datetime.today() - relativedelta(years=1))
            search_patient_to_date = st.date_input("To Date", datetime.today())
            button = st.form_submit_button("Get Patients Records")

        elif option == 'Per file':
            st.title("Enter File Details")
            st.text(
                " No File extension is Required\nExample:\n'myfile.csv' => your input 'myfile'")
            search_file_name = st.text_input(label='File Name')
            search_created_on = st.date_input("Created On", datetime.today())
            button = st.form_submit_button("Get File Records")

if button:
    if validate_search_input_details():
        if option == 'Per Patient':
            data = search_patient_by_fullname()
            data = pd.DataFrame(data)
            if data.shape[0] > 0:
                data_frame_style_display(data)
            else:
                st.warning("No Records Found")

        elif option == 'Window Period':
            data = search_patient_by_window_period()
            data = pd.DataFrame(data)
            if data.shape[0] > 0:
                data_frame_style_display(data)
            else:
                st.warning("No Records Found")

        elif option == 'Per file':

            data = search_patients_file_by_date()
            data = pd.DataFrame(data)
            if data.shape[0] > 0:
                data_frame_style_display(data)
            else:
                st.warning("No Records Found")
