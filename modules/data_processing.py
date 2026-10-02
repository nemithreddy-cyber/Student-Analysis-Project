"""
Data Processing Module for Student Academic Performance and Statistical Analysis System.
Handles data loading from CSV/Excel, dataset summaries, and basic cleanup.
"""
import os
import pandas as pd
from config.settings import REQUIRED_COLUMNS, NUMERIC_COLUMNS, DEMO_DATASET_PATH

def load_demo_dataset(filepath=None):
    """
    Loads the default demonstration dataset from CSV.
    """
    path = filepath if filepath else DEMO_DATASET_PATH
    if not os.path.exists(path):
        # Fallback inline generation if file not found
        from scripts.generate_demo_data import generate_demo_dataset
        return generate_demo_dataset(path)
    
    df = pd.read_csv(path)
    return df

def load_user_dataset(uploaded_file):
    """
    Loads a dataset from an uploaded CSV or Excel file buffer.
    """
    if uploaded_file is None:
        return None, "No file uploaded."
    
    filename = uploaded_file.name
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file format. Please upload a CSV or Excel file."
        return df, None
    except Exception as e:
        return None, f"Error reading file '{filename}': {str(e)}"

def get_dataset_info(df, source_type="Demo Dataset", source_name="students.csv"):
    """
    Returns a dictionary summarizing basic properties of the dataset.
    """
    if df is None or df.empty:
        return {
            "source_type": source_type,
            "source_name": source_name,
            "total_rows": 0,
            "total_columns": 0,
            "column_names": [],
            "numeric_columns": [],
            "missing_cells": 0,
            "duplicate_rows": 0,
            "is_demo": source_type == "Demo Dataset"
        }
        
    num_rows, num_cols = df.shape
    cols = list(df.columns)
    num_cols_present = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    missing_total = int(df.isnull().sum().sum())
    duplicate_count = int(df.duplicated().sum())
    
    return {
        "source_type": source_type,
        "source_name": source_name,
        "total_rows": num_rows,
        "total_columns": num_cols,
        "column_names": cols,
        "numeric_columns": num_cols_present,
        "missing_cells": missing_total,
        "duplicate_rows": duplicate_count,
        "is_demo": (source_type == "Demo Dataset")
    }

def sanitize_numeric_data(df):
    """
    Ensures numerical columns are converted to proper float/int types where possible.
    Does not drop rows silently, only coerces types.
    """
    df_clean = df.copy()
    for col in df_clean.columns:
        if col in NUMERIC_COLUMNS or col != "Student_ID":
            # Attempt numeric conversion
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
    return df_clean
