import xgboost as xgb
import pandas as pd
import numpy as np
from typing import Optional, Dict

class DelayPredictor:
    def __init__(self):
        self.model: Optional[xgb.XGBRegressor] = None
        self.customer_delay_mapper: Dict[str, float] = {}
        self.payment_terms_delay_mapper: Dict[str, float] = {}
        self.global_mean_delay: float = 0.0
        self.feature_columns = [
            "total_open_amount",
            "_weekday_due_in_date",
            "_month_baseline_date",
            "_weekday_baseline_date",
            "mean_delay_customer",
            "mean_delay_terms",
        ]

    def train(self, train_df: pd.DataFrame):
        self.global_mean_delay = float(train_df["delay"].mean())

        self.customer_delay_mapper = (
            train_df.groupby("cust_number")["delay"]
            .mean()
            .astype(float)
            .to_dict()
        )

        self.payment_terms_delay_mapper = (
            train_df.groupby("cust_payment_terms")["delay"]
            .mean()
            .astype(float)
            .to_dict()
        )

        # Features are already extracted or need to be extracted here?
        # In current main.py, they are extracted in train_model after load_and_prepare
        # Let's assume train_df has these columns already, or we add them.
        
        # We need to make sure mean_delay_customer/terms are in train_df
        train_df = train_df.copy()
        train_df["mean_delay_customer"] = (
            train_df["cust_number"]
            .map(self.customer_delay_mapper)
            .fillna(self.global_mean_delay)
        )
        train_df["mean_delay_terms"] = (
            train_df["cust_payment_terms"]
            .map(self.payment_terms_delay_mapper)
            .fillna(self.global_mean_delay)
        )

        x_train = train_df[self.feature_columns]
        y_train = train_df["delay"]

        self.model = xgb.XGBRegressor(
            objective="reg:squarederror",
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            random_state=42,
        )
        self.model.fit(x_train, y_train)

    def predict(self, features_df: pd.DataFrame) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model is not trained yet")
        return self.model.predict(features_df[self.feature_columns])

    def get_aging_bucket(self, delay: float) -> str:
        if delay <= 0:
            return "0-0 days"
        if delay <= 15:
            return "1-15 days"
        if delay <= 30:
            return "16-30 days"
        if delay <= 45:
            return "31-45 days"
        if delay <= 60:
            return "46-60 days"
        return "> 60 days"
