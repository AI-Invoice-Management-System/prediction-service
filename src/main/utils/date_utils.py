import pandas as pd

def parse_yyyymmdd_or_date(series: pd.Series) -> pd.Series:
    """
    Convert mixed date columns safely.

    Handles values like:
    - 20200313
    - 20200313.0
    - '2020-03-13'
    """
    as_string = (
        series
        .astype("string")
        .str.replace(r"\.0$", "", regex=True)
        .str.strip()
    )

    numeric_date = pd.to_datetime(as_string, format="%Y%m%d", errors="coerce")
    regular_date = pd.to_datetime(as_string, format="mixed", errors="coerce")

    return numeric_date.fillna(regular_date)
