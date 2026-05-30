import pandas as pd
import numpy as np
from src.main.models.predictor import DelayPredictor

def test_aging_bucket():
    predictor = DelayPredictor()
    assert predictor.get_aging_bucket(-5) == "0-0 days"
    assert predictor.get_aging_bucket(0) == "0-0 days"
    assert predictor.get_aging_bucket(10) == "1-15 days"
    assert predictor.get_aging_bucket(20) == "16-30 days"
    assert predictor.get_aging_bucket(40) == "31-45 days"
    assert predictor.get_aging_bucket(50) == "46-60 days"
    assert predictor.get_aging_bucket(100) == "> 60 days"

def test_model_training_and_prediction():
    # Create dummy training data
    train_df = pd.DataFrame({
        "cust_number": ["C1", "C2", "C1", "C2"] * 25,
        "cust_payment_terms": ["T1", "T2", "T1", "T2"] * 25,
        "total_open_amount": np.random.rand(100) * 1000,
        "_weekday_due_in_date": [0, 1] * 50,
        "_month_baseline_date": [1, 1] * 50,
        "_weekday_baseline_date": [0, 0] * 50,
        "delay": [5.0, 15.0, 5.0, 15.0] * 25
    })
    
    predictor = DelayPredictor()
    predictor.train(train_df)
    
    assert predictor.model is not None
    assert predictor.global_mean_delay == 10.0
    assert predictor.customer_delay_mapper["C1"] == 5.0
    assert predictor.customer_delay_mapper["C2"] == 15.0

    # Test prediction
    test_df = pd.DataFrame({
        "total_open_amount": [500.0],
        "_weekday_due_in_date": [0],
        "_month_baseline_date": [1],
        "_weekday_baseline_date": [0],
        "mean_delay_customer": [5.0],
        "mean_delay_terms": [5.0]
    })
    
    prediction = predictor.predict(test_df)
    assert len(prediction) == 1
    assert isinstance(prediction[0], (float, np.float32))
