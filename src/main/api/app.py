import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pathlib import Path
from typing import Optional

from src.main.api.schemas import InvoiceRequest, PredictionResponse
from src.main.data.loader import load_data, preprocess_training_data
from src.main.features.engine import extract_date_features, apply_mappers
from src.main.models.predictor import DelayPredictor

app = FastAPI(
    title="Invoice Payment Delay Prediction API",
    description="FastAPI service for predicting invoice payment delay and aging bucket.",
    version="1.0.0",
)

predictor: Optional[DelayPredictor] = None
CSV_PATH = Path("1806126.csv")
MODEL_PATH = Path("model.pkl")

@app.on_event("startup")
def startup_event():
    global predictor
    if MODEL_PATH.exists():
        print(f"Loading model from {MODEL_PATH}...")
        with open(MODEL_PATH, "rb") as f:
            predictor = pickle.load(f)
    else:
        print("Model file not found. Training new model...")
        df = load_data(CSV_PATH)
        train_df = preprocess_training_data(df)
        train_df = extract_date_features(train_df)
        predictor = DelayPredictor()
        predictor.train(train_df)

@app.get("/")
def root():
    return {
        "message": "Invoice payment delay prediction API is running",
        "docs": "/docs",
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(invoice: InvoiceRequest):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model is not initialized")
        
    due_in_date = pd.to_datetime(invoice.due_in_date, errors="coerce")
    baseline_create_date = pd.to_datetime(invoice.baseline_create_date, errors="coerce")

    if pd.isna(due_in_date) or pd.isna(baseline_create_date):
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Prepare features for single prediction
    features_data = {
        "cust_number": [invoice.cust_number],
        "cust_payment_terms": [invoice.cust_payment_terms],
        "due_in_date": [due_in_date],
        "baseline_create_date": [baseline_create_date],
        "total_open_amount": [invoice.total_open_amount]
    }
    df_single = pd.DataFrame(features_data)
    df_single = extract_date_features(df_single)
    df_single = apply_mappers(df_single, 
                              predictor.customer_delay_mapper, 
                              predictor.payment_terms_delay_mapper, 
                              predictor.global_mean_delay)

    try:
        delay_pred = predictor.predict(df_single)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    predicted_delay = float(delay_pred)
    predicted_clear_date = due_in_date + pd.Timedelta(days=round(predicted_delay))
    
    return PredictionResponse(
        predicted_delay_days=predicted_delay,
        predicted_clear_date=predicted_clear_date.strftime("%Y-%m-%d"),
        aging_bucket=predictor.get_aging_bucket(predicted_delay)
    )
