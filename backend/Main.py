from fastapi import FastAPI, UploadFile, Form
import pandas as pd
from io import StringIO
from automl.trainer import train_model
from automl.predictor import predict

app = FastAPI()

@app.post("/automl/train")
async def train(file: UploadFile, target: str = Form(...)):
    df = pd.read_csv(StringIO((await file.read()).decode()))
    return {"status": train_model(df, target)}

@app.post("/automl/predict")
async def make_prediction(file: UploadFile):
    df = pd.read_csv(StringIO((await file.read()).decode()))
    result = predict(df)
    return {"predictions": result}
