"""
Descriptive Statistics Module for Student Academic Performance and Statistical Analysis System.
Provides core statistical functions for central tendency, variability, and step-by-step calculations.
"""
import numpy as np
import pandas as pd
from scipy import stats

def calculate_descriptive_stats(series):
    """
    Computes summary descriptive statistics for a numerical Series.
    Uses sample statistics (ddof=1 for variance and standard deviation).
    
    Returns a dictionary of key-value statistical metrics.
    """
    s = series.dropna()
    n = len(s)
    
    if n == 0:
        return {
            "n": 0,
            "mean": np.nan,
            "median": np.nan,
            "mode": "N/A",
            "min": np.nan,
            "max": np.nan,
            "range": np.nan,
            "q1": np.nan,
            "q3": np.nan,
            "iqr": np.nan,
            "variance": np.nan,
            "std_dev": np.nan,
            "cv": np.nan,
            "mad": np.nan,
            "trimmed_mean_5": np.nan,
            "skewness": np.nan
        }

    # Central Tendency
    mean_val = float(s.mean())
    median_val = float(s.median())
    trimmed_5 = float(stats.trim_mean(s, 0.05)) if n >= 10 else mean_val
    
    # Mode calculation
    counts = s.value_counts()
    if len(counts) == 0:
        mode_str = "No values"
    else:
        max_freq = counts.iloc[0]
        if max_freq == 1 and n > 1:
            mode_str = "No unique mode exists for this dataset."
        else:
            modal_vals = counts[counts == max_freq].index.tolist()
            if len(modal_vals) == 1:
                mode_str = f"{modal_vals[0]:.2f}".rstrip('0').rstrip('.')
            elif len(modal_vals) > 5:
                mode_str = f"Multiple modes ({len(modal_vals)} values with frequency {max_freq})"
            else:
                mode_str = ", ".join([f"{v:.2f}".rstrip('0').rstrip('.') for v in modal_vals])

    # Dispersion & Quartiles
    min_val = float(s.min())
    max_val = float(s.max())
    range_val = float(max_val - min_val)
    
    q1 = float(s.quantile(0.25))
    q3 = float(s.quantile(0.75))
    iqr = float(q3 - q1)
    
    mad_val = float(np.mean(np.abs(s - mean_val)))

    if n > 1:
        variance_val = float(s.var(ddof=1))
        std_dev_val = float(s.std(ddof=1))
        cv_val = float((std_dev_val / mean_val) * 100) if mean_val != 0 else np.nan
        skewness_val = float(stats.skew(s, bias=False)) if n >= 3 else float(stats.skew(s))
    else:
        variance_val = 0.0
        std_dev_val = 0.0
        cv_val = 0.0
        skewness_val = 0.0

    return {
        "n": n,
        "mean": mean_val,
        "median": median_val,
        "mode": mode_str,
        "trimmed_mean_5": trimmed_5,
        "min": min_val,
        "max": max_val,
        "range": range_val,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "variance": variance_val,
        "std_dev": std_dev_val,
        "cv": cv_val,
        "mad": mad_val,
        "skewness": skewness_val
    }

def get_calculation_details(series, max_rows=100):
    """
    Generates step-by-step mathematical breakdown of Mean and Sample Variance calculations.
    Returns details dict including a step-by-step tabular DataFrame.
    """
    s = series.dropna()
    n = len(s)
    if n == 0:
        return None
        
    sum_x = float(s.sum())
    mean_val = sum_x / n if n > 0 else 0.0
    
    deviations = s - mean_val
    sq_deviations = deviations ** 2
    sum_sq_diff = float(sq_deviations.sum())
    
    sample_var = sum_sq_diff / (n - 1) if n > 1 else 0.0
    sample_std = np.sqrt(sample_var)
    
    table_df = pd.DataFrame({
        "Observation (x)": s.values,
        "Deviation (x - x̄)": np.round(deviations.values, 4),
        "Squared Deviation (x - x̄)²": np.round(sq_deviations.values, 4)
    })
    
    if len(table_df) > max_rows:
        preview_table = table_df.head(max_rows)
    else:
        preview_table = table_df

    return {
        "n": n,
        "sum_x": sum_x,
        "mean": mean_val,
        "sum_sq_diff": sum_sq_diff,
        "sample_variance": sample_var,
        "sample_std_dev": sample_std,
        "table_df": preview_table,
        "total_observations": len(table_df)
    }

def get_summary_table_for_all_numeric(df):
    """
    Returns a consolidated DataFrame of descriptive statistics for all numeric columns.
    """
    num_cols = df.select_dtypes(include=[np.number]).columns
    results = []
    
    for col in num_cols:
        st = calculate_descriptive_stats(df[col])
        results.append({
            "Variable": col,
            "Count (n)": st["n"],
            "Mean (x̄)": round(st["mean"], 2) if not np.isnan(st["mean"]) else np.nan,
            "Median": round(st["median"], 2) if not np.isnan(st["median"]) else np.nan,
            "Mode": st["mode"],
            "Min": round(st["min"], 2) if not np.isnan(st["min"]) else np.nan,
            "Max": round(st["max"], 2) if not np.isnan(st["max"]) else np.nan,
            "Range": round(st["range"], 2) if not np.isnan(st["range"]) else np.nan,
            "IQR": round(st["iqr"], 2) if not np.isnan(st["iqr"]) else np.nan,
            "Variance (s²)": round(st["variance"], 2) if not np.isnan(st["variance"]) else np.nan,
            "Std Dev (s)": round(st["std_dev"], 2) if not np.isnan(st["std_dev"]) else np.nan,
            "CV (%)": round(st["cv"], 2) if not np.isnan(st["cv"]) else np.nan,
            "Skewness": round(st["skewness"], 3) if not np.isnan(st["skewness"]) else np.nan
        })
        
    return pd.DataFrame(results)
