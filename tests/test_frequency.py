"""
Unit tests for frequency analysis and ogive data generation.
"""
import pytest
import pandas as pd
import numpy as np
from modules.frequency_analysis import generate_frequency_table

def test_frequency_table_and_ogive_monotonicity():
    # Generate random series
    np.random.seed(42)
    data = np.random.uniform(40, 100, size=100)
    s = pd.Series(data, name="Final_Marks")
    
    freq_df, ogive_data = generate_frequency_table(s, num_bins=6)
    
    assert not freq_df.empty
    assert freq_df["Frequency (f)"].sum() == 100
    
    # TC07: Cumulative frequency MUST be monotonic (non-decreasing)
    cf_diff = freq_df["Cumulative Frequency (CF)"].diff().dropna()
    assert (cf_diff >= 0).all(), "Cumulative frequency is not monotonic!"
    
    # Verify ogive data matches
    assert ogive_data["cumulative_frequencies"][-1] == 100
    assert len(ogive_data["upper_boundaries"]) == len(ogive_data["cumulative_frequencies"])
