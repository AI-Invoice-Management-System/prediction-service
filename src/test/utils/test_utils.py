import pandas as pd
from src.main.utils.date_utils import parse_yyyymmdd_or_date

def test_parse_yyyymmdd():
    series = pd.Series(["20200313", "20200313.0"])
    result = parse_yyyymmdd_or_date(series)
    assert result.iloc[0] == pd.Timestamp("2020-03-13")
    assert result.iloc[1] == pd.Timestamp("2020-03-13")

def test_parse_regular_date():
    series = pd.Series(["2020-03-13", "03/13/2020"])
    result = parse_yyyymmdd_or_date(series)
    assert result.iloc[0] == pd.Timestamp("2020-03-13")
    assert result.iloc[1] == pd.Timestamp("2020-03-13")

def test_parse_mixed_dates():
    series = pd.Series(["20200313", "2020-03-14"])
    result = parse_yyyymmdd_or_date(series)
    assert result.iloc[0] == pd.Timestamp("2020-03-13")
    assert result.iloc[1] == pd.Timestamp("2020-03-14")

def test_parse_invalid_date():
    series = pd.Series(["invalid"])
    result = parse_yyyymmdd_or_date(series)
    assert pd.isna(result.iloc[0])
