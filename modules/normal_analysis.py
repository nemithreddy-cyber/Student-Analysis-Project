"""
Normal Datasets & Empirical Rule Analysis Module.
Evaluates distribution normality, empirical rule (68-95-99.7%), Shapiro-Wilk test, and Q-Q data.
"""
import numpy as np
import pandas as pd
from scipy import stats

def analyze_normality(series):
    """
    Evaluates whether a numeric series aligns with a Normal Distribution N(μ, σ²).
    Calculates Empirical Rule coverage, Shapiro-Wilk test, and Q-Q plot data.
    """
    s = series.dropna()
    n = len(s)
    
    if n < 3:
        return {
            "error": True,
            "message": "At least 3 non-null observations are required for normality analysis."
        }

    mean_val = float(s.mean())
    std_val = float(s.std(ddof=1)) if n > 1 else 0.0

    if std_val == 0:
        return {
            "error": True,
            "message": "Standard deviation is zero; variable is constant."
        }

    # Empirical Rule 1, 2, 3 Sigma Coverage
    pct_1s = float(((s >= mean_val - 1 * std_val) & (s <= mean_val + 1 * std_val)).mean() * 100)
    pct_2s = float(((s >= mean_val - 2 * std_val) & (s <= mean_val + 2 * std_val)).mean() * 100)
    pct_3s = float(((s >= mean_val - 3 * std_val) & (s <= mean_val + 3 * std_val)).mean() * 100)

    count_1s = int(((s >= mean_val - 1 * std_val) & (s <= mean_val + 1 * std_val)).sum())
    count_2s = int(((s >= mean_val - 2 * std_val) & (s <= mean_val + 2 * std_val)).sum())
    count_3s = int(((s >= mean_val - 3 * std_val) & (s <= mean_val + 3 * std_val)).sum())

    # Shapiro-Wilk Normality Test
    w_stat, p_val = stats.shapiro(s)
    
    is_normal = bool(p_val >= 0.05)
    
    if is_normal:
        normality_status = "Approximately Normally Distributed (p ≥ 0.05)"
        interpretation = (
            f"The Shapiro-Wilk test (W = {w_stat:.4f}, p = {p_val:.4f}) indicates that the dataset "
            f"does NOT significantly deviate from a normal distribution at α = 0.05 significance level."
        )
    else:
        normality_status = "Deviates from Normal Distribution (p < 0.05)"
        interpretation = (
            f"The Shapiro-Wilk test (W = {w_stat:.4f}, p = {p_val:.4f}) indicates significant deviation "
            f"from a normal distribution at α = 0.05 significance level."
        )

    # Q-Q Plot data (Theoretical quantiles vs Sample quantiles)
    sorted_s = np.sort(s.values)
    norm_quantiles = stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n, loc=mean_val, scale=std_val)

    return {
        "error": False,
        "n": n,
        "mean": mean_val,
        "std_dev": std_val,
        "empirical_rule": {
            "1_sigma": {"observed_pct": pct_1s, "theoretical_pct": 68.27, "count": count_1s, "range": (mean_val - std_val, mean_val + std_val)},
            "2_sigma": {"observed_pct": pct_2s, "theoretical_pct": 95.45, "count": count_2s, "range": (mean_val - 2*std_val, mean_val + 2*std_val)},
            "3_sigma": {"observed_pct": pct_3s, "theoretical_pct": 99.73, "count": count_3s, "range": (mean_val - 3*std_val, mean_val + 3*std_val)}
        },
        "shapiro_w": float(w_stat),
        "shapiro_p": float(p_val),
        "is_normal": is_normal,
        "normality_status": normality_status,
        "interpretation": interpretation,
        "qq_sample": sorted_s.tolist(),
        "qq_theoretical": norm_quantiles.tolist()
    }
