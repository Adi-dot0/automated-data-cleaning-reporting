import pandas as pd


def get_profile(df):
    profile = {}
    profile["total_records"] = int(df.shape[0])
    profile["total_columns"] = int(df.shape[1])
    profile["duplicate_records"] = int(df.duplicated().sum())
    profile["total_missing"] = int(df.isnull().sum().sum())

    missing = df.isnull().sum()
    profile["missing_by_column"] = missing[missing > 0].to_dict()

    col_info = []
    for col in df.columns:
        col_info.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "unique": int(df[col].nunique())
        })
    profile["columns"] = col_info
    return profile


def numeric_summary(df):
    num_cols = df.select_dtypes(include="number")
    if num_cols.empty:
        return pd.DataFrame()
    return num_cols.describe().round(2)


def category_summary(df, top_n=10):
    result = {}
    cat_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in cat_cols:
        result[col] = df[col].value_counts(dropna=False).head(top_n)
    return result
