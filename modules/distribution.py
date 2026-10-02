"""
Distribution Analysis Helper Module.
Combines frequency tables, statistics, and distribution metrics for a single variable.
"""
import pandas as pd
from modules.descriptive_stats import calculate_descriptive_stats
from modules.frequency_analysis import generate_frequency_table
from modules.skewness import analyze_skewness

def analyze_variable_distribution(series, num_bins=6):
    """
    Consolidates descriptive statistics, frequency table, and skewness for a target variable.
    """
    s = series.dropna()
    stats_dict = calculate_descriptive_stats(s)
    freq_df, ogive_data = generate_frequency_table(s, num_bins=num_bins)
    skew_dict = analyze_skewness(s)
    
    return {
        "variable_name": s.name if hasattr(s, "name") else "Variable",
        "stats": stats_dict,
        "freq_table": freq_df,
        "ogive_data": ogive_data,
        "skewness_info": skew_dict
    }
