from pycaret.classification import load_model, predict_model
import pandas as pd

def predict(data: pd.DataFrame):
    model = load_model('models/model')
    predictions = predict_model(model, data=data)
    return predictions.to_dict(orient="records")
