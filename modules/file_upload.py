import pandas as pd


def load_file(uploaded_file):
    # reads csv or excel and returns a dataframe
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith(".xlsx") or name.endswith(".xls"):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Only CSV and Excel files are supported")

    if df.empty:
        raise ValueError("File is empty or has no readable data")

    return df


def check_file(uploaded_file):
    allowed = (".csv", ".xlsx", ".xls")
    return uploaded_file.name.lower().endswith(allowed)
