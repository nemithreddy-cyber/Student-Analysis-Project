"""
Chebyshev Analysis Module for Student Academic Performance and Statistical Analysis System.
Calculates theoretical Chebyshev lower bounds and compares them with actual observed percentages.
"""
import numpy as np
import pandas as pd

def calculate_chebyshev_analysis(series, k=2.0):
    """
    Computes Chebyshev's Inequality theoretical bound and compares it against
    the actual empirical proportion of data within [Mean - k*SD, Mean + k*SD].
    
    Requirements:
      - k > 1.0
    """
    if k <= 1.0:
        return {
            "error": True,
            "message": "Chebyshev's Inequality requires k > 1.0."
        }
        
    s = series.dropna()
    n = len(s)
    if n == 0:
        return {
            "error": True,
            "message": "Selected variable contains no valid observations."
        }
        
    mean_val = float(s.mean())
    std_val = float(s.std(ddof=1)) if n > 1 else 0.0
    
    if std_val == 0.0:
        return {
            "error": True,
            "message": "Standard deviation is zero (all observations are identical). Chebyshev interval is singular."
        }

    # Theoretical lower bound calculation: 1 - 1/k^2
    theoretical_bound_frac = 1.0 - (1.0 / (k ** 2))
    theoretical_bound_pct = theoretical_bound_frac * 100.0
    
    # Interval bounds: [Mean - k*s, Mean + k*s]
    lower_interval = mean_val - (k * std_val)
    upper_interval = mean_val + (k * std_val)
    
    # Actual observed count and percentage
    within_mask = (s >= lower_interval) & (s <= upper_interval)
    observed_count = int(within_mask.sum())
    observed_pct = (observed_count / n) * 100.0
    
    out_of_bounds_count = n - observed_count
    
    explanation = (
        f"Chebyshev's Inequality guarantees that for k = {k:.2f}, at least {theoretical_bound_pct:.2f}% "
        f"of all observations lie within {k:.2f} standard deviations of the mean "
        f"({lower_interval:.2f} to {upper_interval:.2f}). "
        f"In this dataset, exactly {observed_count} out of {n} observations ({observed_pct:.2f}%) "
        f"fall within this range, satisfying the theoretical minimum bound of {theoretical_bound_pct:.2f}%."
    )

    return {
        "error": False,
        "variable_name": series.name if hasattr(series, 'name') else "Variable",
        "n": n,
        "mean": mean_val,
        "std_dev": std_val,
        "k": k,
        "theoretical_bound_frac": theoretical_bound_frac,
        "theoretical_bound_pct": theoretical_bound_pct,
        "lower_interval": lower_interval,
        "upper_interval": upper_interval,
        "observed_count": observed_count,
        "observed_pct": observed_pct,
        "out_of_bounds_count": out_of_bounds_count,
        "explanation": explanation
    }
