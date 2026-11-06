# What to do next - simple steps

## Step 1: Run it yourself (15 min)
1. Unzip the project
2. Open Terminal in that folder
3. Run:
   pip install -r requirements.txt
   streamlit run app.py
4. Browser will open (http://localhost:8501)
5. Upload: sample_data/sample_messy_data.csv
6. Click "Clean Data"
7. Download the cleaned CSV and quality report

You should see: 15 rows -> 13 rows, 2 duplicates removed, 6 missing handled, quality score 96.9/100

## Step 2: Take 2 screenshots for GitHub / LinkedIn
1. App home page with the sample file uploaded
2. Result page showing quality score + cleaned table + chart
Save them as screenshot1.png and screenshot2.png in the project folder.

## Step 3: Understand it before you show anyone (important)
Read these 5 files in this order - this is the whole project:
1. app.py - the screen you see, buttons and downloads
2. modules/data_profiling.py - counts rows, missing, duplicates
3. modules/data_cleaning.py - the main cleaning work
4. modules/data_validation.py - email check, negative check, quality score
5. modules/report_generation.py - makes the report you download

## Step 4: Put it on GitHub
Create a new repo named: automated-data-cleaning-reporting
Upload all files (except processing_history.db and __pycache__)
Add the 2 screenshots in the README.

## Step 5: Only after you run it, add it to resume / LinkedIn
Use only this honest wording:
"Built a Streamlit app in Python (Pandas, Plotly) that uploads CSV/Excel files, profiles data quality, removes duplicates, fills missing values, standardizes column names and dates, validates emails, and downloads a cleaned dataset with a quality report. Tested on a sample dataset."

Do NOT add numbers you did not test yourself.

## 5 questions an interviewer can ask - and your one-line answers
1. How do you handle missing values?
   Numeric columns with median/mean, text columns with mode - user chooses in the app.
2. How do you find duplicates?
   pandas duplicated() / drop_duplicates(), and I report how many were removed.
3. What is the quality score?
   Starts at 100, reduces for missing values, duplicates and invalid emails.
4. How are dates fixed?
   pd.to_datetime with mixed format, then saved as YYYY-MM-DD.
5. Why Streamlit?
   Fast to build a data app UI in pure Python, no HTML/CSS needed.

## Next project
Project 2 (BI ETL + Power BI) is next in your doc, but do Project 1 GitHub + run first. One finished, uploaded project is worth more than 3 half-done ones.
