"""
Unit tests for modules/normal_analysis.py
"""
import pytest
import numpy as np
import pandas as pd
from modules.normal_analysis import analyze_normality

def test_analyze_normality_basic():
    # Generate normal random numbers
    np.random.seed(42)
    s = pd.Series(np.random.normal(loc=75, scale=10, size=100))
    res = analyze_normality(s)
    
    assert res["error"] is False
    assert res["n"] == 100
    assert "empirical_rule" in res
    assert res["empirical_rule"]["1_sigma"]["observed_pct"] > 50.0
    assert "shapiro_w" in res
    assert "shapiro_p" in res
    assert len(res["qq_sample"]) == 100
    assert len(res["qq_theoretical"]) == 100

def test_analyze_normality_small_data():
    s = pd.Series([10.0, 12.0])
    res = analyze_normality(s)
    assert res["error"] is True
