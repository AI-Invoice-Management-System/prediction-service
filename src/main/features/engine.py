import pandas as pd
import numpy as np

def extract_date_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "due_in_date" in df.columns:
        df["_weekday_due_in_date"] = np.where(
            df["due_in_date"].dt.weekday / 2 == 2,
            1,
            0,
        )
    if "baseline_create_date" in df.columns:
        df["_month_baseline_date"] = np.where(
            df["baseline_create_date"].dt.month == 12,
            0,
            1,
        )
        df["_weekday_baseline_date"] = np.where(
            df["baseline_create_date"].dt.weekday == 4,
            1,
            0,
        )
    return df

def apply_mappers(df: pd.DataFrame, 
                  customer_delay_mapper: dict, 
                  payment_terms_delay_mapper: dict, 
                  global_mean_delay: float) -> pd.DataFrame:
    df = df.copy()
    df["mean_delay_customer"] = df["cust_number"].map(customer_delay_mapper).fillna(global_mean_delay)
    df["mean_delay_terms"] = df["cust_payment_terms"].map(payment_terms_delay_mapper).fillna(global_mean_delay)
    return df
