from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from joblib import load
import numpy as np
import os

MODEL_PATH = os.getenv('MODEL_PATH', 'models/model.pkl')

app = FastAPI(
    title='Readmission Risk API',
    version='1.0.0',
    description='Prediz probabilidade de readmissão em 30 dias (dados sintéticos).'
)

class PatientFeatures(BaseModel):
    age: int = Field(ge=0, le=120)
    sex: int = Field(ge=0, le=1, description='0=f, 1=m')
    length_of_stay: float = Field(ge=0)
    comorbidities: int = Field(ge=0)
    prior_readmissions: int = Field(ge=0)
    medication_count: int = Field(ge=0)
    lab_score: float
    discharge_type: int = Field(ge=0, le=2)

class PredictionResponse(BaseModel):
    readmission_proba: float
    threshold: float
    readmitted_30d: int

def _load_model():
    return load(MODEL_PATH)

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/predict', response_model=PredictionResponse)
def predict(features: PatientFeatures, threshold: float = 0.5):
    model = _load_model()
    x = np.array(
        [
            [
                features.age,
                features.sex,
                features.length_of_stay,
                features.comorbidities,
                features.prior_readmissions,
                features.medication_count,
                features.lab_score,
                features.discharge_type,
            ]
        ]
    )
    proba = float(model.predict_proba(x)[0, 1])
    y_hat = int(proba >= threshold)
    return {
        'readmission_proba': proba,
        'threshold': threshold,
        'readmitted_30d': y_hat,
    }
