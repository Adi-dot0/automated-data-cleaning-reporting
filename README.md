# Automated Data Cleaning & Reporting System

A Streamlit app that cleans raw CSV / Excel files automatically — no manual work in Excel needed each time.

## Business Problem
Data analysts spend a lot of time on the same steps for every file: removing duplicates, filling missing values, fixing column names and formats, checking wrong values, and making a summary report. This project automates that whole workflow.

## What it does
1. Upload CSV or Excel (multiple files supported)
2. Data profiling — total rows/columns, duplicates, missing values, unique values, data types
3. Automated cleaning — standardize column names, trim spaces, remove duplicates, fill numeric missing values with mean/median, fill text with mode, convert dates to YYYY-MM-DD
4. Data quality check — email format, negative values, date issues, columns with >50% missing, and a quality score out of 100
5. Charts — missing values chart, numeric distribution, top category values (Plotly)
6. Download — cleaned CSV, cleaned Excel, and a quality report (.txt)
7. Every run is logged in a local SQLite table `processing_history`

## Tech Stack
Python, Pandas, NumPy, Streamlit, Plotly, OpenPyXL, SQLite (PostgreSQL table design is in the project doc — SQLite is used here so it runs anywhere with no setup)

## Folder Structure
```
automated-data-cleaning-reporting/
  app.py
  requirements.txt
  README.md
  modules/
    file_upload.py
    data_profiling.py
    data_cleaning.py
    data_validation.py
    report_generation.py
  database/
    db_connection.py
  sample_data/
    sample_messy_data.csv
  tests/
    test_cleaning.py
    test_validation.py
```

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open the local URL Streamlit shows (usually http://localhost:8501).

Try it first with `sample_data/sample_messy_data.csv` — it has duplicates, missing values, bad emails, a negative amount, and mixed date formats on purpose.

## Tests
```bash
pip install pytest
pytest tests/ -v
```
Tested result on the sample file: 15 rows -> 13 rows, duplicates removed 2, missing values handled 6, quality score after cleaning 96.9/100, invalid emails flagged 2, negative amount flagged 1. All 6 unit tests pass. Run the app / tests yourself to record your own numbers.

## Limitations
- Date conversion only applies to columns with "date" in the name
- Email check only applies to columns with "email" in the name
- Very large files will be slow in Streamlit — this is made for normal analyst-size files

## Results on Sample Data
Tested with `sample_data/sample_messy_data.csv`:
- Rows: 15 -> 13 (2 duplicates removed)
- Missing values handled: 6
- Quality score after cleaning: 96.9 / 100
- Invalid emails flagged: 2
- Negative values flagged: 1 (purchase_amount)
- All 6 unit tests pass (`pytest tests/ -v`)

## Screenshots
Add screenshots of the app here after running it:
1. Upload page with a file selected
2. Results page showing quality score, cleaned table and charts
