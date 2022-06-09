from data_processing import pipeline
import pickle


def make_prediction(X):
    X = pipeline(X)
    file = "../models/classifier.pickle"
    classifier = pickle.load(open(file, "rb"))
    return classifier.predict(X)
