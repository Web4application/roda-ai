from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load("models/trained_model.pkl")

class Input(BaseModel):
    features: list

@app.post("/predict")
def predict(data: Input):
    prediction = model.predict([data.features])
    return {"prediction": int(prediction[0])}
