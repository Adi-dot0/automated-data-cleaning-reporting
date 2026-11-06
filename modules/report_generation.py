import pandas as pd
import io


def make_quality_report_text(profile, validation, cleaning_summary):
    lines = []
    lines.append("DATA QUALITY REPORT")
    lines.append("=" * 40)
    lines.append(f"Total records: {profile['total_records']}")
    lines.append(f"Total columns: {profile['total_columns']}")
    lines.append(f"Duplicate records (before cleaning): {profile['duplicate_records']}")
    lines.append(f"Total missing values (before cleaning): {profile['total_missing']}")
    lines.append(f"Quality score (after cleaning): {validation['quality_score']} / 100")
    lines.append("")
    lines.append("CLEANING SUMMARY")
    lines.append("-" * 40)
    for item in cleaning_summary["log"]:
        lines.append(f"- {item}")
    lines.append(f"Rows: {cleaning_summary['original_rows']} -> {cleaning_summary['final_rows']}")
    lines.append("")
    lines.append("VALIDATION (after cleaning)")
    lines.append("-" * 40)
    lines.append(f"Missing values left: {validation['missing_total']}")
    lines.append(f"Duplicates left: {validation['duplicate_rows']}")
    if validation["email_check"]:
        lines.append(f"Invalid emails in '{validation['email_check']['column']}': {validation['email_check']['invalid_count']}")
    if validation["negative_values"]:
        lines.append(f"Negative values found: {validation['negative_values']}")
    if validation["high_missing_columns"]:
        lines.append(f"Columns with >50% missing: {validation['high_missing_columns']}")
    return "\n".join(lines)


def to_excel_bytes(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned Data")
    return buffer.getvalue()
