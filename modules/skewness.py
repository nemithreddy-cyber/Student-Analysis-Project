"""
Skewness Analysis Module for Student Academic Performance and Statistical Analysis System.
Calculates numerical skewness and provides academic interpretations of distribution symmetry.
"""
import numpy as np
import pandas as pd
from scipy import stats

def analyze_skewness(series):
    """
    Computes skewness coefficient and provides formal statistical classification.
    """
    s = series.dropna()
    n = len(s)
    if n < 3:
        return {
            "skewness": 0.0,
            "classification": "Insufficient Data",
            "interpretation": "At least 3 valid observations are required to calculate meaningful skewness.",
            "mean": float(s.mean()) if n > 0 else 0.0,
            "median": float(s.median()) if n > 0 else 0.0
        }
        
    mean_val = float(s.mean())
    median_val = float(s.median())
    skew_val = float(stats.skew(s, bias=False))

    if skew_val > 0.2:
        classification = "Positively Skewed (Right-skewed)"
        interpretation = (
            f"The distribution of '{s.name if hasattr(s, 'name') else 'Variable'}' has a positive skewness of {skew_val:.3f}. "
            f"This indicates that the right tail is longer or fatter, with more observations concentrated on the lower side of the scale "
            f"(Mean = {mean_val:.2f} > Median = {median_val:.2f})."
        )
    elif skew_val < -0.2:
        classification = "Negatively Skewed (Left-skewed)"
        interpretation = (
            f"The distribution of '{s.name if hasattr(s, 'name') else 'Variable'}' has a negative skewness of {skew_val:.3f}. "
            f"This indicates that the left tail is longer or fatter, with more observations concentrated on the higher side of the scale "
            f"(Mean = {mean_val:.2f} < Median = {median_val:.2f})."
        )
    else:
        classification = "Approximately Symmetric"
        interpretation = (
            f"The distribution of '{s.name if hasattr(s, 'name') else 'Variable'}' has a skewness value of {skew_val:.3f}, "
            f"which is near zero. The observations are distributed relatively symmetrically around the mean "
            f"(Mean = {mean_val:.2f}, Median = {median_val:.2f})."
        )

    disclaimer = "Note: Skewness alone does not establish normality. Additional distribution plots and normality tests are required to confirm a normal distribution."

    return {
        "skewness": skew_val,
        "classification": classification,
        "interpretation": interpretation,
        "disclaimer": disclaimer,
        "mean": mean_val,
        "median": median_val,
        "n": n
    }
