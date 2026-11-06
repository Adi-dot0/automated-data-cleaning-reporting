import streamlit as st
import pandas as pd
import plotly.express as px

from modules.file_upload import load_file, check_file
from modules.data_profiling import get_profile, numeric_summary, category_summary
from modules.data_cleaning import clean_data
from modules.data_validation import validate_data
from modules.report_generation import make_quality_report_text, to_excel_bytes
from database.db_connection import save_history

st.set_page_config(page_title="Automated Data Cleaning", layout="wide")
st.title("Automated Data Cleaning & Reporting System")
st.write("Upload a raw CSV or Excel file. The app profiles it, cleans it, checks quality and gives you a ready-to-use dataset.")

uploaded_files = st.file_uploader("Upload CSV / Excel files", type=["csv", "xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    for uploaded in uploaded_files:
        if not check_file(uploaded):
            st.error(f"{uploaded.name} - file type not supported")
            continue

        try:
            df = load_file(uploaded)
        except Exception as e:
            st.error(f"{uploaded.name} - could not read file: {e}")
            continue

        st.header(f"File: {uploaded.name}")
        st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
        st.dataframe(df.head(10))

        profile = get_profile(df)
        st.subheader("Data Profile (before cleaning)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records", profile["total_records"])
        col2.metric("Total Columns", profile["total_columns"])
        col3.metric("Duplicate Rows", profile["duplicate_records"])
        col4.metric("Missing Values", profile["total_missing"])

        st.dataframe(pd.DataFrame(profile["columns"]))

        if profile["missing_by_column"]:
            missing_df = pd.DataFrame(list(profile["missing_by_column"].items()), columns=["column", "missing"])
            fig = px.bar(missing_df, x="column", y="missing", title="Missing Values by Column")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Cleaning Options")
        numeric_fill = st.selectbox("Fill numeric missing values with", ["median", "mean"], key=f"num_{uploaded.name}")
        category_fill = st.selectbox("Fill text missing values with", ["mode", "Unknown"], key=f"cat_{uploaded.name}")
        drop_rows = st.checkbox("Drop rows with missing values instead of filling", key=f"drop_{uploaded.name}")

        if st.button("Clean Data", key=f"btn_{uploaded.name}"):
            cleaned_df, summary = clean_data(df, numeric_fill=numeric_fill, category_fill=category_fill, drop_rows=drop_rows)
            validation = validate_data(cleaned_df)

            save_history(uploaded.name, profile["total_records"], profile["duplicate_records"], profile["total_missing"])

            st.success("Cleaning done")
            st.write(f"Rows: {summary['original_rows']} -> {summary['final_rows']} | Duplicates removed: {summary['duplicates_removed']} | Missing handled: {summary['missing_handled']}")
            for line in summary["log"]:
                st.write(f"- {line}")

            st.metric("Data Quality Score (after cleaning)", f"{validation['quality_score']} / 100")

            if validation["email_check"]:
                st.write(f"Invalid emails: {validation['email_check']['invalid_count']}")
            if validation["negative_values"]:
                st.write(f"Negative values: {validation['negative_values']}")

            st.dataframe(cleaned_df.head(20))

            st.subheader("Charts (cleaned data)")
            num_cols = cleaned_df.select_dtypes(include="number").columns.tolist()
            if num_cols:
                chosen = st.selectbox("Pick a numeric column", num_cols, key=f"chart_{uploaded.name}")
                fig2 = px.histogram(cleaned_df, x=chosen, title=f"Distribution of {chosen}")
                st.plotly_chart(fig2, use_container_width=True)

            cat = category_summary(cleaned_df)
            for col_name, counts in list(cat.items())[:2]:
                fig3 = px.bar(x=counts.index.astype(str), y=counts.values, labels={"x": col_name, "y": "count"}, title=f"Top values in {col_name}")
                st.plotly_chart(fig3, use_container_width=True)

            st.subheader("Numerical Summary")
            st.dataframe(numeric_summary(cleaned_df))

            report_text = make_quality_report_text(profile, validation, summary)

            st.subheader("Download")
            st.download_button("Download Cleaned CSV", cleaned_df.to_csv(index=False), file_name="cleaned_data.csv", mime="text/csv")
            st.download_button("Download Cleaned Excel", to_excel_bytes(cleaned_df), file_name="cleaned_data.xlsx")
            st.download_button("Download Quality Report (.txt)", report_text, file_name="quality_report.txt", mime="text/plain")

            st.session_state[f"cleaned_{uploaded.name}"] = cleaned_df
else:
    st.info("No file uploaded yet. You can try the file in sample_data/sample_messy_data.csv")
