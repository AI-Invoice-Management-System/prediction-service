import pytest
from fastapi.testclient import TestClient
import pandas as pd
from src.main.api.app import app
import src.main.api.app as app_module

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_predict_success(monkeypatch):
    # Mock the predictor
    class MockPredictor:
        def __init__(self):
            self.customer_delay_mapper = {}
            self.payment_terms_delay_mapper = {}
            self.global_mean_delay = 0.0
            
        def predict(self, df):
            return [5.5]
            
        def get_aging_bucket(self, delay):
            return "1-15 days"

    mock_predictor = MockPredictor()
    monkeypatch.setattr(app_module, "predictor", mock_predictor)

    payload = {
        "cust_number": "0200769623",
        "cust_payment_terms": "NAH4",
        "due_in_date": "2020-03-13",
        "baseline_create_date": "2020-02-27",
        "total_open_amount": 54273.28
    }
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_delay_days"] == 5.5
    assert data["aging_bucket"] == "1-15 days"
    assert "predicted_clear_date" in data

def test_predict_invalid_date(monkeypatch):
    # Mock the predictor so it's not None
    class MockPredictor:
        def __init__(self):
            self.customer_delay_mapper = {}
            self.payment_terms_delay_mapper = {}
            self.global_mean_delay = 0.0
    monkeypatch.setattr(app_module, "predictor", MockPredictor())

    payload = {
        "cust_number": "0200769623",
        "cust_payment_terms": "NAH4",
        "due_in_date": "invalid-date",
        "baseline_create_date": "2020-02-27",
        "total_open_amount": 54273.28
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid date format"

def test_predict_not_initialized(monkeypatch):
    monkeypatch.setattr(app_module, "predictor", None)
    payload = {
        "cust_number": "0200769623",
        "cust_payment_terms": "NAH4",
        "due_in_date": "2020-03-13",
        "baseline_create_date": "2020-02-27",
        "total_open_amount": 54273.28
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 503
    assert response.json()["detail"] == "Model is not initialized"
