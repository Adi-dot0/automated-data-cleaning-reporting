import pandas as pd
import re


def clean_column_names(df):
    new_cols = []
    for col in df.columns:
        c = str(col).strip().lower()
        c = re.sub(r"[^a-z0-9]+", "_", c)
        c = c.strip("_")
        new_cols.append(c)
    df = df.copy()
    df.columns = new_cols
    return df


def trim_text(df):
    df = df.copy()
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    # blank strings are also missing values
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    # if a text column is mostly numbers, make it numeric (e.g. Age stored as text)
    for col in df.columns:
        if df[col].dtype == object:
            converted = pd.to_numeric(df[col], errors="coerce")
            if len(df) and converted.notna().sum() >= df[col].notna().sum() * 0.8 and converted.notna().sum() > 0:
                df[col] = converted
    return df


def handle_missing(df, numeric_fill="median", category_fill="mode", drop_rows=False):
    df = df.copy()
    if drop_rows:
        before = len(df)
        df = df.dropna()
        return df, before - len(df)

    filled = 0
    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            if numeric_fill == "mean":
                value = df[col].mean()
            else:
                value = df[col].median()
            df[col] = df[col].fillna(value)
        else:
            if category_fill == "mode":
                mode_vals = df[col].mode()
                value = mode_vals[0] if len(mode_vals) > 0 else "Unknown"
                df[col] = df[col].fillna(value)
            else:
                df[col] = df[col].fillna("Unknown")
        filled += int(missing)
    return df, filled


def remove_duplicates(df):
    before = len(df)
    df = df.drop_duplicates()
    return df, before - len(df)


def try_convert_dates(df):
    df = df.copy()
    for col in df.columns:
        if "date" in col.lower():
            try:
                converted = pd.to_datetime(df[col], errors="coerce", format="mixed")
                # only keep conversion if most values converted ok
                if converted.notna().sum() >= len(df) * 0.5:
                    df[col] = converted.dt.strftime("%Y-%m-%d")
            except Exception:
                pass
    return df


def clean_data(df, numeric_fill="median", category_fill="mode", drop_rows=False):
    log = []
    original_rows = len(df)

    df = clean_column_names(df)
    log.append("Standardized column names to lowercase with underscores")

    df = trim_text(df)
    log.append("Removed extra spaces from text values")

    df, dup_removed = remove_duplicates(df)
    log.append(f"Removed {dup_removed} duplicate rows")

    df, missing_handled = handle_missing(df, numeric_fill, category_fill, drop_rows)
    log.append(f"Handled {missing_handled} missing values (numeric={numeric_fill}, category={category_fill}, drop_rows={drop_rows})")

    df = try_convert_dates(df)
    log.append("Converted date columns to YYYY-MM-DD where possible")

    summary = {
        "original_rows": original_rows,
        "final_rows": len(df),
        "duplicates_removed": dup_removed,
        "missing_handled": missing_handled,
        "log": log
    }
    return df, summary
