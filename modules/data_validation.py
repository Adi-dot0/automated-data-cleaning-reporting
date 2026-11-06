import pandas as pd
import re

email_pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def check_emails(df):
    for col in df.columns:
        if "email" in col.lower():
            values = df[col].dropna().astype(str)
            bad = values[~values.apply(lambda x: bool(email_pattern.match(x)))]
            return {"column": col, "invalid_count": int(len(bad)), "invalid_values": bad.head(5).tolist()}
    return None


def check_negative(df):
    result = {}
    for col in df.select_dtypes(include="number").columns:
        count = int((df[col] < 0).sum())
        if count > 0:
            result[col] = count
    return result


def check_dates(df):
    result = {}
    for col in df.columns:
        if "date" in col.lower():
            parsed = pd.to_datetime(df[col], errors="coerce", format="mixed")
            result[col] = int(parsed.isnull().sum() - df[col].isnull().sum())
    return result


def quality_score(df):
    # simple score out of 100, based on missing, duplicates and invalid emails
    if df.empty or df.size == 0:
        return 0

    total_cells = df.size
    missing_ratio = df.isnull().sum().sum() / total_cells
    dup_ratio = df.duplicated().sum() / len(df) if len(df) else 0

    score = 100
    score -= missing_ratio * 50
    score -= dup_ratio * 30

    email_check = check_emails(df)
    if email_check and len(df):
        score -= (email_check["invalid_count"] / len(df)) * 20

    return round(max(0, min(100, score)), 1)


def validate_data(df):
    report = {}
    report["missing_total"] = int(df.isnull().sum().sum())
    report["duplicate_rows"] = int(df.duplicated().sum())
    report["email_check"] = check_emails(df)
    report["negative_values"] = check_negative(df)
    report["date_issues"] = check_dates(df)

    # columns with more than 50% missing are flagged
    high_missing = []
    for col in df.columns:
        if len(df) and df[col].isnull().mean() > 0.5:
            high_missing.append(col)
    report["high_missing_columns"] = high_missing
    report["quality_score"] = quality_score(df)
    return report
