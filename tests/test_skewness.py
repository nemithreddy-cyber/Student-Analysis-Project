"""
Unit tests for skewness analysis module.
"""
import pytest
import pandas as pd
import numpy as np
from modules.skewness import analyze_skewness

def test_positive_skewness():
    # Right-skewed distribution
    data = [10, 12, 13, 14, 15, 16, 17, 45, 60, 80]
    s = pd.Series(data, name="PosSkew")
    res = analyze_skewness(s)
    
    assert res["skewness"] > 0.2
    assert "Positively Skewed" in res["classification"]

def test_negative_skewness():
    # Left-skewed distribution
    data = [20, 40, 70, 80, 85, 88, 90, 92, 95, 98]
    s = pd.Series(data, name="NegSkew")
    res = analyze_skewness(s)
    
    assert res["skewness"] < -0.2
    assert "Negatively Skewed" in res["classification"]

def test_symmetric():
    # Symmetric distribution
    data = [10, 20, 30, 40, 50, 60, 70]
    s = pd.Series(data, name="Symm")
    res = analyze_skewness(s)
    
    assert abs(res["skewness"]) <= 0.2
    assert "Symmetric" in res["classification"]
