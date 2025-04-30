from pycaret.classification import setup, compare_models, save_model
import pandas as pd

def train_model(data: pd.DataFrame, target: str):
    clf = setup(data=data, target=target, silent=True, session_id=123)
    best_model = compare_models()
    save_model(best_model, 'models/model')
    return "Model trained and saved successfully."
