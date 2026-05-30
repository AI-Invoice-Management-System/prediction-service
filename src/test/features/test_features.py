import pandas as pd
import numpy as np
from src.main.features.engine import extract_date_features, apply_mappers

def test_extract_date_features():
    df = pd.DataFrame({
        "due_in_date": pd.to_datetime(["2020-03-13", "2020-03-14"]),  # 13th is Friday (4), 14th is Saturday (5)
        "baseline_create_date": pd.to_datetime(["2020-12-01", "2020-11-01"])
    })
    result = extract_date_features(df)
    
    # weekday/2 == 2 => weekday == 4 (Friday)
    assert result.iloc[0]["_weekday_due_in_date"] == 1
    assert result.iloc[1]["_weekday_due_in_date"] == 0
    
    # month == 12 => 0, else 1
    assert result.iloc[0]["_month_baseline_date"] == 0
    assert result.iloc[1]["_month_baseline_date"] == 1
    
    # weekday == 4 => 1, else 0. 2020-12-01 is Tuesday (1), 2020-11-01 is Sunday (6)
    # Wait, let's check actual weekdays. 
    # 2020-12-01: weekday() in pandas is 1 (Tuesday)
    # 2020-11-01: weekday() in pandas is 6 (Sunday)
    # 2020-10-30: Friday (4)
    
    df2 = pd.DataFrame({
        "baseline_create_date": pd.to_datetime(["2020-10-30", "2020-10-29"])
    })
    result2 = extract_date_features(df2)
    assert result2.iloc[0]["_weekday_baseline_date"] == 1 # Friday
    assert result2.iloc[1]["_weekday_baseline_date"] == 0

def test_apply_mappers():
    df = pd.DataFrame({
        "cust_number": ["C1", "C2"],
        "cust_payment_terms": ["T1", "T2"]
    })
    customer_mapper = {"C1": 10.0}
    terms_mapper = {"T1": 5.0}
    global_mean = 2.0
    
    result = apply_mappers(df, customer_mapper, terms_mapper, global_mean)
    
    assert result.iloc[0]["mean_delay_customer"] == 10.0
    assert result.iloc[1]["mean_delay_customer"] == 2.0
    assert result.iloc[0]["mean_delay_terms"] == 5.0
    assert result.iloc[1]["mean_delay_terms"] == 2.0
