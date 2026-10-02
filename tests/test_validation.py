"""
Unit tests for data validation module.
"""
import pytest
import pandas as pd
import numpy as np
from modules.validation import validate_dataset

def test_valid_csv_validation():
    # TC01: Upload valid CSV
    df = pd.DataFrame({
        "Student_ID": ["ST001", "ST002", "ST003"],
        "Attendance": [86.0, 92.0, 74.0],
        "Study_Hours": [3.5, 5.0, 2.5],
        "Assignment_Marks": [17.0, 19.0, 14.0],
        "Internal_Marks": [18.0, 20.0, 15.0],
        "Final_Marks": [78.0, 88.0, 65.0]
    })
    res = validate_dataset(df)
    assert res["overall_status"] == "Valid"
    assert res["summary_counts"]["errors"] == 0

def test_missing_column_validation():
    # TC02: Upload invalid file / missing required columns
    df = pd.DataFrame({
        "Student_ID": ["ST001"],
        "Attendance": [86.0]
    })
    res = validate_dataset(df)
    assert res["overall_status"] == "Error"
    assert res["summary_counts"]["errors"] > 0

def test_attendance_out_of_range():
    # TC03: Attendance outside 0-100
    df = pd.DataFrame({
        "Student_ID": ["ST001", "ST002"],
        "Attendance": [150.0, -10.0],  # Invalid
        "Study_Hours": [3.5, 5.0],
        "Assignment_Marks": [17.0, 19.0],
        "Internal_Marks": [18.0, 20.0],
        "Final_Marks": [78.0, 88.0]
    })
    res = validate_dataset(df)
    assert res["overall_status"] in ["Warning", "Error"]
    assert len(res["flagged_rows"]) == 2

def test_missing_final_marks():
    # TC04: Missing Final_Marks
    df = pd.DataFrame({
        "Student_ID": ["ST001", "ST002"],
        "Attendance": [86.0, 92.0],
        "Study_Hours": [3.5, 5.0],
        "Assignment_Marks": [17.0, 19.0],
        "Internal_Marks": [18.0, 20.0],
        "Final_Marks": [78.0, np.nan]  # Missing
    })
    res = validate_dataset(df)
    assert res["overall_status"] == "Warning"
    assert len(res["flagged_rows"]) == 1
