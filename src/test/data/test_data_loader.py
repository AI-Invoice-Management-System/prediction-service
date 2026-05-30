import pandas as pd
import pytest
from pathlib import Path
from src.main.data.loader import load_data, preprocess_training_data

def test_load_data(tmp_path):
    csv_file = tmp_path / "test.csv"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_csv(csv_file, index=False)
    
    loaded_df = load_data(csv_file)
    assert len(loaded_df) == 2
    assert list(loaded_df.columns) == ["col1", "col2"]

def test_load_data_not_found():
    with pytest.raises(FileNotFoundError):
        load_data(Path("non_existent.csv"))

def test_preprocess_training_data():
    # Minimal columns required by preprocess_training_data
    data = {
        "area_business": [1, 1],
        "clear_date": ["2020-04-01", "2020-04-10"],
        "document_create_date": [20200320, 20200320],
        "document_create_date.1": [20200320, 20200320],
        "due_in_date": [20200325, 20200325],
        "baseline_create_date": [20200320, 20200320],
        "posting_date": ["2020-03-20", "2020-03-20"],
        "posting_id": [1, 1],
        "buisness_year": [2020, 2020],
        "invoice_currency": ["USD", "CAD"],
        "total_open_amount": [100.0, 100.0],
        "document type": ["RV", "RV"],
        "invoice_id": [123, 124],
        "doc_id": [123, 124],
        "cust_number": ["C1", "C2"],
        "cust_payment_terms": ["T1", "T2"],
        "isOpen": [0, 0]
    }
    df = pd.DataFrame(data)
    
    processed_df = preprocess_training_data(df)
    
    assert "delay" in processed_df.columns
    # 2020-04-01 - 2020-03-25 = 7 days
    assert processed_df.iloc[0]["delay"] == 7
    # 2020-04-10 - 2020-03-25 = 16 days
    assert processed_df.iloc[1]["delay"] == 16
    
    # CAD conversion: 100 * 0.79 = 79.0
    # Note: row 1 is CAD
    assert processed_df.iloc[1]["total_open_amount"] == 79.0
    
    # Check dropped columns
    assert "area_business" not in processed_df.columns
    assert "invoice_currency" not in processed_df.columns

def test_preprocess_missing_columns():
    df = pd.DataFrame({"invalid": [1]})
    with pytest.raises(ValueError, match="CSV is missing required columns"):
        preprocess_training_data(df)
