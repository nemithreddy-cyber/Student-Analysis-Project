"""
Unit tests for descriptive statistics calculations.
"""
import pytest
import pandas as pd
import numpy as np
from modules.descriptive_stats import calculate_descriptive_stats, get_calculation_details

def test_descriptive_stats_known_values():
    # Sample numbers: 10, 20, 30, 40, 50
    # n = 5
    # sum = 150 -> mean = 30
    # median = 30
    # range = 40
    # dev^2 = 400 + 100 + 0 + 100 + 400 = 1000
    # sample var = 1000 / 4 = 250
    # sample std = sqrt(250) ~ 15.8113883
    s = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0], name="TestVar")
    res = calculate_descriptive_stats(s)
    
    assert res["n"] == 5
    assert abs(res["mean"] - 30.0) < 1e-6
    assert abs(res["median"] - 30.0) < 1e-6
    assert abs(res["range"] - 40.0) < 1e-6
    assert abs(res["variance"] - 250.0) < 1e-6
    assert abs(res["std_dev"] - np.sqrt(250.0)) < 1e-6

def test_no_unique_mode():
    s = pd.Series([10.0, 20.0, 30.0, 40.0], name="TestVar")
    res = calculate_descriptive_stats(s)
    assert "No unique mode" in res["mode"]

def test_multiple_modes():
    s = pd.Series([10.0, 10.0, 20.0, 20.0, 30.0], name="TestVar")
    res = calculate_descriptive_stats(s)
    assert "10" in res["mode"] and "20" in res["mode"]

def test_calculation_details():
    s = pd.Series([2.0, 4.0, 6.0], name="TestVar")
    # mean = 4, sum = 12
    # devs: -2, 0, 2 -> sq_devs: 4, 0, 4 -> sum_sq = 8
    # var = 8 / 2 = 4.0, std = 2.0
    details = get_calculation_details(s)
    assert details["n"] == 3
    assert abs(details["sum_x"] - 12.0) < 1e-6
    assert abs(details["mean"] - 4.0) < 1e-6
    assert abs(details["sum_sq_diff"] - 8.0) < 1e-6
    assert abs(details["sample_variance"] - 4.0) < 1e-6
    assert abs(details["sample_std_dev"] - 2.0) < 1e-6
