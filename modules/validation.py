"""
Validation Module for Student Academic Performance and Statistical Analysis System.
Performs data validation checks according to academic dataset rules.
"""
import pandas as pd
import numpy as np
from config.settings import REQUIRED_COLUMNS, VALIDATION_RULES

def validate_dataset(df):
    """
    Validates the dataset against required columns, data types, missing values,
    duplicates, and domain range constraints.
    
    Returns a dictionary containing:
      - overall_status: "Valid", "Warning", or "Error"
      - checks: list of check dictionaries {"name", "status", "icon", "message", "details"}
      - flagged_rows: DataFrame of rows containing any validation issues
      - summary_counts: summary count of issues
    """
    if df is None or df.empty:
        return {
            "overall_status": "Error",
            "checks": [{
                "name": "Dataset Existence",
                "status": "Error",
                "icon": "✕",
                "message": "Dataset is empty or not loaded.",
                "details": []
            }],
            "flagged_rows": pd.DataFrame(),
            "summary_counts": {"errors": 1, "warnings": 0, "passed": 0}
        }

    checks = []
    error_count = 0
    warning_count = 0
    passed_count = 0
    flagged_indices = set()

    # 1. Required Columns Check
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        error_count += 1
        checks.append({
            "name": "Required Columns",
            "status": "Error",
            "icon": "✕",
            "message": f"Missing required columns: {', '.join(missing_cols)}",
            "details": [f"Expected column '{c}' was not found in dataset." for c in missing_cols]
        })
    else:
        passed_count += 1
        checks.append({
            "name": "Required Columns",
            "status": "Valid",
            "icon": "✓",
            "message": "All required columns are present.",
            "details": [f"Columns verified: {', '.join(REQUIRED_COLUMNS)}"]
        })

    # 2. Numeric Columns Check
    non_numeric_cols = []
    for col in REQUIRED_COLUMNS:
        if col in df.columns and col != "Student_ID":
            # Check if values can be numeric
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.isnull().sum() > df[col].isnull().sum():
                non_numeric_cols.append(col)
                
    if non_numeric_cols:
        error_count += 1
        checks.append({
            "name": "Numeric Columns",
            "status": "Error",
            "icon": "✕",
            "message": f"Non-numeric values found in column(s): {', '.join(non_numeric_cols)}",
            "details": [f"Column '{c}' contains text or invalid numerical data." for c in non_numeric_cols]
        })
    else:
        passed_count += 1
        checks.append({
            "name": "Numeric Columns",
            "status": "Valid",
            "icon": "✓",
            "message": "All performance variables contain valid numeric data types.",
            "details": []
        })

    # 3. Missing Values Check
    missing_mask = df.isnull()
    total_missing = missing_mask.sum().sum()
    if total_missing > 0:
        warning_count += 1
        missing_rows = df[missing_mask.any(axis=1)].index
        flagged_indices.update(missing_rows)
        col_missing_summary = [f"{col}: {df[col].isnull().sum()} missing" for col in df.columns if df[col].isnull().sum() > 0]
        checks.append({
            "name": "Missing Values",
            "status": "Warning",
            "icon": "⚠",
            "message": f"Found {total_missing} missing value(s) across {len(missing_rows)} record(s).",
            "details": col_missing_summary
        })
    else:
        passed_count += 1
        checks.append({
            "name": "Missing Values",
            "status": "Valid",
            "icon": "✓",
            "message": "No missing values found in the dataset.",
            "details": []
        })

    # 4. Duplicate Rows Check
    dup_rows = df[df.duplicated(keep=False)]
    if len(dup_rows) > 0:
        warning_count += 1
        flagged_indices.update(dup_rows.index)
        checks.append({
            "name": "Duplicate Rows",
            "status": "Warning",
            "icon": "⚠",
            "message": f"Found {len(dup_rows)} duplicate row(s) in the dataset.",
            "details": [f"Row indices {list(dup_rows.index)} are identical duplicates."]
        })
    else:
        passed_count += 1
        checks.append({
            "name": "Duplicate Rows",
            "status": "Valid",
            "icon": "✓",
            "message": "No duplicate rows found.",
            "details": []
        })

    # 5. Duplicate Student_ID Check
    if "Student_ID" in df.columns:
        dup_ids = df[df.duplicated(subset=["Student_ID"], keep=False)]
        if len(dup_ids) > 0:
            warning_count += 1
            flagged_indices.update(dup_ids.index)
            dup_id_list = dup_ids["Student_ID"].unique().tolist()
            checks.append({
                "name": "Student ID Uniqueness",
                "status": "Warning",
                "icon": "⚠",
                "message": f"Found {len(dup_ids)} record(s) with duplicate Student_ID.",
                "details": [f"Duplicate Student_ID values: {', '.join(map(str, dup_id_list))}"]
            })
        else:
            passed_count += 1
            checks.append({
                "name": "Student ID Uniqueness",
                "status": "Valid",
                "icon": "✓",
                "message": "All Student_ID values are unique.",
                "details": []
            })

    # 6-10. Academic Value Range Checks
    range_issues = []
    for col, rule in VALIDATION_RULES.items():
        if col in df.columns:
            series = pd.to_numeric(df[col], errors="coerce")
            min_val = rule["min"]
            max_val = rule["max"]
            
            invalid_mask = (series < min_val) | (series > max_val)
            invalid_rows = df[invalid_mask]
            
            if len(invalid_rows) > 0:
                warning_count += 1
                flagged_indices.update(invalid_rows.index)
                range_issues.append({
                    "col": col,
                    "count": len(invalid_rows),
                    "rule": f"{min_val} <= {col} <= {max_val}",
                    "indices": list(invalid_rows.index)
                })

    if range_issues:
        details_list = [f"'{item['col']}': {item['count']} value(s) outside expected range ({item['rule']}). Rows: {item['indices']}" for item in range_issues]
        checks.append({
            "name": "Academic Value Ranges",
            "status": "Warning",
            "icon": "⚠",
            "message": f"Value range issues detected in {len(range_issues)} variable(s).",
            "details": details_list
        })
    else:
        passed_count += 1
        checks.append({
            "name": "Academic Value Ranges",
            "status": "Valid",
            "icon": "✓",
            "message": "All academic variables fall within expected valid boundaries.",
            "details": [
                "Attendance: 0 - 100%",
                "Study Hours: >= 0",
                "Assignment Marks: 0 - 20",
                "Internal Marks: 0 - 20",
                "Final Marks: 0 - 100"
            ]
        })

    # Determine overall status
    if error_count > 0:
        overall_status = "Error"
    elif warning_count > 0:
        overall_status = "Warning"
    else:
        overall_status = "Valid"

    flagged_df = df.loc[sorted(list(flagged_indices))] if flagged_indices else pd.DataFrame()

    return {
        "overall_status": overall_status,
        "checks": checks,
        "flagged_rows": flagged_df,
        "summary_counts": {
            "errors": error_count,
            "warnings": warning_count,
            "passed": passed_count
        }
    }
