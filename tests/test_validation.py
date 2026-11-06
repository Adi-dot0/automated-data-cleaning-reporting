import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.data_validation import validate_data, quality_score


def test_quality_score_clean_data():
    df = pd.DataFrame({"email": ["a@gmail.com", "b@gmail.com"], "age": [20, 30]})
    assert quality_score(df) == 100.0


def test_validate_finds_bad_email():
    df = pd.DataFrame({"email": ["good@gmail.com", "bad-email"]})
    report = validate_data(df)
    assert report["email_check"]["invalid_count"] == 1


def test_validate_finds_duplicates():
    df = pd.DataFrame({"a": [1, 1]})
    report = validate_data(df)
    assert report["duplicate_rows"] == 1
