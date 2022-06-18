
import pandas as pd
import numpy as np
import json

from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests
import streamlit as st

# interact with FastAPI endpoint
BACKEND ="http://0.0.0.0:8005/"


# Make Predictions Section

def get_prediction():
    """_summary_
    Takes users Input from User Interface returns a Prediction
    Returns:
        _type_: _description_
    """
    features= input_details_to_json()
    url =BACKEND + "predcit"
    response = requests.get(url, json=features)
    if response.status_code ==200:
        results=response.json()
        prediction = results["prediction"]
        return prediction
    else:
        st.error("An error occurred while getting the prediction!")

def get_prediction_document(data :pd.DataFrame):
    """_summary_
     Takes File Input from User Interface returns a Prediction Dataframe 
     Displays the Data Frame on the Screen
    Args:
        data (pd.DataFrame): _description_
    """
    data=data_frame_fix_column_with_Nan_float(data)
    list_of_json= data.to_dict(orient='records')
    data_json =dict()
    data_json["record"] ={ "id": 0,"file_name": filename}
    data_json["patient"] =list_of_json
    url =BACKEND + "predcit_multiple"
    response = requests.get(url, json=data_json)
    if response.status_code == 200:
        result = json.loads(response.content)
        prediction_df = pd.read_json(result, orient ='index') 
        data["prediction"]=prediction_df["prediction"]
        return data
    else:
        st.error("An error occurred while parsinf the file's predictions !")

def data_frame_style_color_neg(val):
    """_summary_
    Pandas Dataframe Styler
    Args:
        val (_type_): _description_

    Returns:
        _type_: _description_
    """
    color = 'red' if type(val) == str and val=="Risk of Stroke" else 'green'
    return 'color: %s' %color


def data_frame_fix_column_with_Nan_float(data):
    """_summary_
    Fix Nan_float issues in dataframe , Pydantic model doesnt like Nan's in Float columns
    Json Encoder doesnt like to deal with Nan's in Float columns
    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    float_cols = data.select_dtypes(include=['float64','int64']).columns
    str_cols = data.select_dtypes(include=['object']).columns
    data.loc[:, float_cols]=data.loc[:, float_cols].fillna(0.0)
    data.loc[:, str_cols]=data.loc[:, str_cols].fillna('')
    return data


def input_details_to_json():
    """_summary_
    
    Returns:
        _type_: _description_
    """
    myform_json= {  "record": { "id": 0,
                                "file_name": "N/A",
                                "doctor_first_name": doctor_first_name if len(doctor_first_name.strip()) else "N/A",
                                "doctor_last_name": doctor_last_name if len(doctor_last_name.strip()) else "N/A"},
                    "patient": {    "id" :0,
                                    "firstname": first_name,
                                    "lastname": last_name,
                                    "gender": gender,
                                    "age" : age,
                                    "hypertension": 1 if hypertension=="yes" else 0,
                                    "heart_disease": 1 if heart_disease=="yes" else 0,
                                    "ever_married" : ever_married,
                                    "work_type": work_type,
                                    "Residence_type": residence_type,
                                    "avg_glucose_level": avg_glucose_level,
                                    "bmi": bmi,
                                    "smoking_status": smoking_status
                                }
                    }
    return myform_json

# Data Base Querying 
def search_patient_by_fullname():
    """_summary_
    Search for a patient by fullname
    Returns:
        _type_: _description_
    """
    url =BACKEND + "patient/search/{firstname}&{lastname}"\
        .format(firstname=search_patient_first_name if len(search_patient_first_name) else "%%",
                lastname=search_patient_last_name if len(search_patient_last_name) else "%%",)
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        results=response.json()
        return results
    else:
        st.error("An error occurred while searching for the patient!")
    
# Form Validations

def validate_search_input_details():
    """_summary_
    Validate Inputs from User Interface
    Returns:
        _type_: _description_
    """
    if len(search_patient_first_name.strip())==0 and len(search_patient_last_name.strip())==0:
        st.warning("First Name or Last Name is required to Search!")
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
    with st.form(key='my_form' ,clear_on_submit=True):
        st.title("Patient Form")
        gender_list = np.array(["Male", "Female"])
        yes_no = np.array(["Yes", "No"])
        work_type_lit = np.array(['Private', 'Self employed', 'Govt job', 'children', 'Never worked'])
        residence_type_list = np.array(['Urban', 'Rural'])
        first_name = st.text_input(label='First Name')
        last_name = st.text_input(label='Last Name')
        gender = st.radio("Select your Gender", gender_list)
        age = st.number_input(label='Age', min_value=0, step=1, max_value=150)
        hypertension = st.radio("Did you had Hypertension in the past ?", yes_no)
        heart_disease = st.radio("Did you had Heart Problem in the past ?", yes_no)
        ever_married = st.radio("Have you ever been married ?", yes_no)
        work_type = st.radio("What is your Work Type ?", work_type_lit)
        residence_type = st.radio("What is your Living Environment?", residence_type_list)
        avg_glucose_level = st.number_input(label='Enter your Average Glucose Level', min_value=0.0, step=0.1)
        bmi = st.number_input(label='Enter your Body Mass Index (bmi)', min_value=0.0, step=0.,format="%.2f")
        smoking_status = st.radio("Do you Smoke ?", ('smoked','formerly smoked','Unknown'))
        doctor_first_name = st.text_input(label='Dc. First Name')
        doctor_last_name = st.text_input(label='Dc. Last Name')
        submit_button = st.form_submit_button(label='Predict')

if submit_button :
    prediciton = get_prediction()
    message = f"{first_name} {last_name} You are at risk of a stroke !" if prediciton == 1 else  "you are safe to slay another day :)"
    message_color = 'red' if prediciton == 1 else  'green'
    st.markdown(f"<h3 style='text-align: left;color:{message_color}'> {(message)} </h3>", unsafe_allow_html=True)
    link_to_visit ="https://www.cdc.gov/stroke/prevention.htm"
  
# File  Prediction Page Section
with st.sidebar.expander("Upload File for Predictions"):
    with st.form(key="predictions",clear_on_submit=True) as form:
        st.title("Select a File to Generate Predictions")
        uploaded_files = st.file_uploader("Choose a CSV file")
        if uploaded_files:
            st.write("filename:", uploaded_files.name)
            filename=uploaded_files.name
        else:
            filename="N/A"
        predict_button = st.form_submit_button("Submit")
        if filename != "N/A" and predict_button:
            st.success("File sent")

if predict_button :
    data = pd.read_csv(uploaded_files)
    data=get_prediction_document(data)
    data["prediction"] = data["prediction"].apply(lambda x:"Risk of Stroke" if x == 1 else "Normal")
    st.dataframe(data.style.applymap(data_frame_style_color_neg,subset=['prediction']))

# Prediction Retrival Page Section
with st.sidebar.expander("Retrieve Past Predictions"):
    button =None
    st.title("Select a Search Mode")
    option = st.selectbox('Search Mode',('< Select Option >','Per Patient', 'Window Period', 'Per file'))

   
    with st.form(key="Retrieve patients predictions by full name",clear_on_submit=True) as form_1:
    
     # Per Patient Full Name Search
        if option == 'Per Patient':
            st.title("Patient")
            st.title("Full Name")
            search_patient_first_name = st.text_input(label='First Name')
            search_patient_last_name = st.text_input(label='Last Name')
            button = st.form_submit_button("Get Patient Records")   
        
        elif option=='Window Period':
            st.title("Select a Window Period")
            st.title("Dates Between")
            from_date = st.date_input("From Date",datetime.today() - relativedelta(years=1))
            to_date  = st.date_input("To Date",datetime.today())
            button = st.form_submit_button("Get Patients Records")
            
        elif option=='Per file':
            st.title("Enter File Details")
            st.title("Details")
            file_name = st.text_input(label='File Name')
            created_on  = st.date_input("Created On",datetime.today())
            button = st.form_submit_button("Get Patients Records")
    
         
        
    # # per Window Period Search       
    # elif option=='Window Period':
    #         st.title("Select a Window Period")
    #         with st.form(key="Retrieve patients predictions by window period",clear_on_submit=True) as form_2:
    #             st.title("Dates Between")
    #             from_date = st.date_input("From Date",datetime.today() - relativedelta(years=1))
    #             to_date  = st.date_input("To Date",datetime.today())
    #             search_button_file = st.form_submit_button("Get Patients Records")
    #             if search_button_file:
    #                 pass
                
    # # Per File Search          
    # elif option=='Per file':
    #         st.title("Enter File Details")
    #         with st.form(key="Retrieve patients predictions by file",clear_on_submit=True) as form_3:
    #             st.title("Details")
    #             file_name = st.text_input(label='File Name')
    #             created_on  = st.date_input("Created On",datetime.today())
    #             submit_button_patient = st.form_submit_button("Get Patients Records")
    #             if submit_button_patient:
    #                 pass
if button :
    if option == 'Per Patient':
       if validate_search_input_details():
           data = search_patient_by_fullname()
           data = pd.DataFrame(data)
           if data.shape[0] > 0:
                data["prediction"] = data["prediction"].apply(lambda x:"Risk of Stroke" if x == 1 else "Normal")
                data.drop('record_id', axis=1, inplace=True)
                st.dataframe( data.style.applymap(data_frame_style_color_neg,subset=['prediction']))
           else:
               st.warning("No Records Found")
          
    elif option=='Window Period':
        pass
        
    elif option=='Per file':
        pass
          
         

                
   
        




