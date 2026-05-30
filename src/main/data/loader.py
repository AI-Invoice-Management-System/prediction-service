import pandas as pd
import numpy as np
from pathlib import Path
from src.main.utils.date_utils import parse_yyyymmdd_or_date

def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    return df

def preprocess_training_data(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = {
        "area_business",
        "clear_date",
        "document_create_date",
        "document_create_date.1",
        "due_in_date",
        "baseline_create_date",
        "posting_date",
        "posting_id",
        "buisness_year",
        "invoice_currency",
        "total_open_amount",
        "document type",
        "invoice_id",
        "doc_id",
        "cust_number",
        "cust_payment_terms",
        "isOpen",
    }

    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {sorted(missing_columns)}")

    df1 = df.drop(["area_business"], axis=1)

    df1["document_create_date"] = parse_yyyymmdd_or_date(df1["document_create_date"])
    df1["document_create_date.1"] = parse_yyyymmdd_or_date(df1["document_create_date.1"])
    df1["due_in_date"] = parse_yyyymmdd_or_date(df1["due_in_date"])
    df1["baseline_create_date"] = parse_yyyymmdd_or_date(df1["baseline_create_date"])
    df1["posting_date"] = pd.to_datetime(df1["posting_date"], errors="coerce")
    df1["clear_date"] = pd.to_datetime(df1["clear_date"], errors="coerce").dt.normalize()

    df1 = df1.drop(
        [
            "posting_id",
            "buisness_year",
            "document_create_date",
            "invoice_id",
            "doc_id",
        ],
        axis=1,
        errors="ignore",
    )

    cad_mask = df1["invoice_currency"].eq("CAD")
    df1.loc[cad_mask, "total_open_amount"] = df1.loc[cad_mask, "total_open_amount"] * 0.79
    df1 = df1.drop(["invoice_currency"], axis=1, errors="ignore")

    train_df = df1[df1["clear_date"].notna()].copy()
    train_df["delay"] = (train_df["clear_date"] - train_df["due_in_date"]).dt.days

    train_df = train_df[
        (train_df["document_create_date.1"] <= train_df["baseline_create_date"])
        & (train_df["posting_date"] <= train_df["baseline_create_date"])
        & (train_df["baseline_create_date"] <= train_df["clear_date"])
    ].copy()

    train_df = train_df[train_df["document type"].eq("RV")].copy()
    train_df = train_df.drop(["document type"], axis=1, errors="ignore")

    delay_std = train_df["delay"].std()
    delay_mean = train_df["delay"].mean()

    if delay_std and not np.isnan(delay_std):
        train_df = train_df[
            np.abs((train_df["delay"] - delay_mean) / delay_std) < 10
        ].copy()

    return train_df
