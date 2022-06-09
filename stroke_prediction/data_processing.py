import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import pickle

pd.options.mode.chained_assignment = None  # default='warn'


def split_test_train(df):

    X = df.iloc[:, :-1]
    Y = df.iloc[:, -1]
    xtrain, xtest, ytrain, ytest = train_test_split(X,
                                                    Y,
                                                    random_state=43,
                                                    test_size=0.33)
    return (xtrain,
            xtest,
            ytrain,
            ytest)


def reformat_work_type(df):

    df["work_type"] = df["work_type"].replace("Self-employed", "Self employed")
    df["work_type"] = df["work_type"].replace("Govt_job", "Govt job")
    df["work_type"] = df["work_type"].replace("children", "Children")
    df["work_type"] = df["work_type"].replace("Never_worked", "Never worked")

    return df


def rename_columns(df):

    df = df.rename(columns={"heart_disease": "heart disease",
                            "avg_glucose_level": "avg glucose level",
                            "ever_married": "ever married",
                            "Residence_type": "residence type",
                            "work_type": "work type",
                            "smoking_status": "smoking status"})
    return df


def format_df(df):

    xtrain, xtest, ytrain, ytest = split_test_train(df)
    xtrain = reformat_work_type(xtrain)
    xtrain = rename_columns(xtrain)
    return xtrain, xtest, ytrain, ytest


def format_inference_df(df):

    df = reformat_work_type(df)
    df = rename_columns(df)
    return df


def fit_KNN_missing_values(df):

    file = "../models/imputer_KNN.pickle"
    imputer = KNNImputer(n_neighbors=5)
    imputer.fit(df[["bmi"]])
    pickle.dump(imputer, open(file, "wb"))

    return df


def transform_imputer(df):

    file = "../models/imputer_KNN.pickle"
    imputer = pickle.load(open(file, "rb"))
    df["bmi"] = imputer.transform(df[["bmi"]])
    return df


def preprocess_gender(df):

    df = df.replace("Male", 0)
    df = df.replace("Female", 1)
    other_inde = df[df["gender"] == "Other"].index
    df = df.drop(other_inde)
    return df, other_inde


def fit_scaler(df):

    cols = ["age", "avg glucose level", "bmi"]
    file = "../models/Scaler.pickle"
    scaler = MinMaxScaler()
    scaler.fit(df[cols])
    pickle.dump(scaler, open(file, "wb"))


def transfom_scaler(df):

    cols = ["age", "avg glucose level", "bmi"]
    file = "../models/Scaler.pickle"
    scaler = pickle.load(open(file, "rb"))
    df[cols] = scaler.transform(df[cols])
    return df


def preprocess_residence(df):

    df = df.replace("Urban", 0)
    df = df.replace("Rural", 1)
    return df


def preprocess_ever_married(df):

    df = df.replace("Yes", 0)
    df = df.replace("No", 1)
    return df


def fit_encoder(df):

    file = "../models/OneHot.pickle"
    enc = OneHotEncoder(handle_unknown="ignore", sparse=False)
    enc.fit(df[["work type", "smoking status"]])

    pickle.dump(enc, open(file, "wb"))


def transform_encoder(df):

    file = "../models/OneHot.pickle"
    enc = pickle.load(open(file, "rb"))
    list_name = enc.get_feature_names_out(["work type", "smoking status"])
    df[list_name] = enc.transform(df[["work type", "smoking status"]])
    df = df.drop(columns=["work type", "smoking status"])
    return df


def fit_scaler_encoder(df):

    fit_KNN_missing_values(df)
    fit_encoder(df)
    fit_scaler(df)


def transform_scaler_encoder(df):

    df = transform_imputer(df)
    df = transform_encoder(df)
    df = transfom_scaler(df)
    return df


def store_id(df):
    df_ids = df["id"]
    df = df.drop(columns=["id"])
    return df_ids, df


def build_model(xtrain, ytrain):

    file = "../models/classifier.pickle"
    classifier = LogisticRegression(max_iter=3000,penalty='l1', solver='liblinear')
    classifier.fit(xtrain, ytrain)
    pickle.dump(classifier, open(file, "wb"))
    return classifier


def pipeline(df):
    
    if "stroke" in df.columns :
        mask_0=df["stroke"]==0
        mask_1=df["stroke"]==1
        df_0=df[mask_0]
        df_1=df[mask_1]
        df_0=df_0.iloc[:1000,:]
        df=pd.concat((df_0,df_1))
        xtrain, xtest, ytrain, ytest = format_df(df)

        fit_scaler_encoder(xtrain)
        xtrain = transform_scaler_encoder(xtrain)
        xtrain, ind = preprocess_gender(xtrain)

        ytrain = ytrain.drop(index=ind)
        xtrain = preprocess_ever_married(xtrain)
        xtrain = preprocess_residence(xtrain)
        ids, xtrain = store_id(xtrain)
        return xtrain, ytrain, xtest, ytest
    else :
        if "firstname" in df.columns:
            df = df.loc[:,[col for col in df.columns if col not in ['firstname', ' lastname', ' dob']]]
            
        df = format_inference_df(df)
        if df["bmi"].isnull().sum() > 0:
            df = transform_imputer(df)
        df, ind = preprocess_gender(df)
        df = preprocess_ever_married(df)
        df = preprocess_residence(df)
        df = transform_scaler_encoder(df)
        ids, df = store_id(df)
        return df


def evaluate_model(xtest, ytest):
    xtest = pipeline(xtest)
    file = "../models/classifier.pickle"
    classifier = pickle.load(open(file, "rb"))
    return classifier.score(xtest, ytest)
