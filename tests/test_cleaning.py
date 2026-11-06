import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.data_cleaning import clean_column_names, remove_duplicates, clean_data


def test_clean_column_names():
    df = pd.DataFrame({"Customer Name ": [1], "Age (Years)": [2]})
    df = clean_column_names(df)
    assert list(df.columns) == ["customer_name", "age_years"]


def test_remove_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2]})
    df, removed = remove_duplicates(df)
    assert removed == 1
    assert len(df) == 2


def test_clean_data_fills_missing():
    df = pd.DataFrame({"Age": [10, None, 30], "City": ["Delhi", None, "Pune"]})
    cleaned, summary = clean_data(df)
    assert cleaned.isnull().sum().sum() == 0
    assert summary["final_rows"] == 3
