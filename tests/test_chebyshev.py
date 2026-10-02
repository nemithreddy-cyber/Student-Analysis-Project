"""
Unit tests for Chebyshev's Inequality analysis module.
"""
import pytest
import pandas as pd
import numpy as np
from modules.chebyshev import calculate_chebyshev_analysis

def test_chebyshev_k2():
    # TC09: Run Chebyshev for k=2. Expected theoretical lower bound = 75%
    s = pd.Series(np.random.normal(70, 10, 100), name="Final_Marks")
    res = calculate_chebyshev_analysis(s, k=2.0)
    
    assert res["error"] is False
    assert abs(res["theoretical_bound_pct"] - 75.0) < 1e-6
    assert res["observed_pct"] >= res["theoretical_bound_pct"]  # Chebyshev guarantee must hold

def test_chebyshev_k3():
    s = pd.Series(np.random.normal(70, 10, 100), name="Final_Marks")
    res = calculate_chebyshev_analysis(s, k=3.0)
    
    assert res["error"] is False
    assert abs(res["theoretical_bound_pct"] - (1 - 1/9)*100) < 1e-4

def test_chebyshev_invalid_k():
    s = pd.Series([10, 20, 30], name="Final_Marks")
    res = calculate_chebyshev_analysis(s, k=0.5)
    assert res["error"] is True
    assert "k > 1.0" in res["message"]
