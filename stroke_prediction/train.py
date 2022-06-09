from stroke_prediction.data_processing import (pipeline,
                                               build_model,
                                               evaluate_model)


def make_model(df):
    xtrain, ytrain, xtest, ytest = pipeline(df)
    build_model(xtrain, ytrain)
    return evaluate_model(xtest, ytest)
