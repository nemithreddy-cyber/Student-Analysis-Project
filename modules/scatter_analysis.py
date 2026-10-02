"""
Scatter Plot Analysis Module for Student Academic Performance and Statistical Analysis System.
Analyzes paired observations, regression trends, and visual associations without causal claims.
"""
import numpy as np
import pandas as pd
from scipy import stats

def analyze_scatter_relationship(df, x_col, y_col):
    """
    Analyzes the paired quantitative relationship between x_col and y_col.
    
    Returns metrics, trend line parameters, correlation coefficient, and academic interpretation.
    """
    if x_col not in df.columns or y_col not in df.columns:
        return {
            "error": True,
            "message": f"Variables '{x_col}' or '{y_col}' not found in dataset.",
            "r_value": 0.0,
            "rvalue": 0.0,
            "correlation": 0.0,
            "r": 0.0,
            "p_value": 1.0,
            "slope": 0.0,
            "intercept": 0.0
        }
        
    paired_df = df[[x_col, y_col]].dropna()
    n = len(paired_df)
    
    if n < 2:
        return {
            "error": True,
            "message": "At least 2 complete paired observations are required for scatter plot analysis.",
            "r_value": 0.0,
            "rvalue": 0.0,
            "correlation": 0.0,
            "r": 0.0,
            "p_value": 1.0,
            "slope": 0.0,
            "intercept": 0.0
        }
        
    x = paired_df[x_col].values
    y = paired_df[y_col].values
    
    # Pearson Correlation Coefficient (r)
    if np.std(x) == 0 or np.std(y) == 0:
        r_val, p_val = 0.0, 1.0
        slope, intercept = 0.0, float(np.mean(y)) if len(y) > 0 else 0.0
        association_type = "No Variation in Variable"
        desc = "Correlation/regression cannot be calculated because one variable has no variation across the selected dataset."
    else:
        r_val, p_val = stats.pearsonr(x, y)
        slope, intercept = np.polyfit(x, y, 1)

        r_val = float(r_val)
        p_val = float(p_val)
        slope = float(slope)
        intercept = float(intercept)

        # Directional association interpretation
        if r_val > 0.5:
            association_type = "Strong Positive Visual Association"
            desc = f"Higher values of '{x_col}' are strongly associated with higher values of '{y_col}'."
        elif r_val > 0.2:
            association_type = "Moderate Positive Visual Association"
            desc = f"Higher values of '{x_col}' tend to be associated with higher values of '{y_col}'."
        elif r_val < -0.5:
            association_type = "Strong Negative Visual Association"
            desc = f"Higher values of '{x_col}' are strongly associated with lower values of '{y_col}'."
        elif r_val < -0.2:
            association_type = "Moderate Negative Visual Association"
            desc = f"Higher values of '{x_col}' tend to be associated with lower values of '{y_col}'."
        else:
            association_type = "No Clear Visual Association"
            desc = f"There is no discernible linear relationship between '{x_col}' and '{y_col}'."

    interpretation = (
        f"Scatter analysis of {n} paired records indicates a {association_type.lower()} "
        f"with a Pearson correlation coefficient of r = {r_val:.3f}. {desc}"
    )

    causation_warning = (
        "Academic Disclaimer: Association does not imply causation. Observed scatter patterns "
        "and correlation coefficients describe co-occurrence in this dataset, not a causal mechanism."
    )

    return {
        "error": False,
        "x_col": x_col,
        "y_col": y_col,
        "n": n,
        "correlation": r_val,
        "r_value": r_val,
        "rvalue": r_val,
        "r": r_val,
        "p_value": p_val,
        "slope": slope,
        "intercept": intercept,
        "association_type": association_type,
        "interpretation": interpretation,
        "causation_warning": causation_warning,
        "paired_data": paired_df
    }
