"""
Frequency Analysis Module for Student Academic Performance and Statistical Analysis System.
Generates grouped frequency distributions and cumulative frequency data for Ogives.
"""
import numpy as np
import pandas as pd

def generate_frequency_table(series, num_bins=6):
    """
    Constructs a grouped frequency distribution table for a numerical variable.
    
    Returns:
      - freq_df: DataFrame with Class Interval, Midpoint, Frequency, Cumulative Frequency, Relative Frequency, Percentage
      - summary_row: DataFrame with total row
      - ogive_data: dict with upper_boundaries and cumulative_frequencies arrays for plotting less-than ogive
    """
    s = series.dropna()
    if len(s) == 0:
        return pd.DataFrame(), None
        
    min_val = float(s.min())
    max_val = float(s.max())
    
    # Determine class width and nice bin edges
    if min_val == max_val:
        bin_edges = np.array([min_val - 0.5, max_val + 0.5])
    else:
        # Create clear, rounded class intervals
        bin_edges = np.linspace(min_val, max_val, num_bins + 1)
        # Round bin edges nicely
        bin_edges = np.round(bin_edges, 1)

    # Compute bin edges and counts accurately
    counts, edges = np.histogram(s, bins=num_bins)
    
    rows = []
    cum_freq = 0
    total_n = len(s)
    
    upper_boundaries = []
    cum_frequencies = []
    
    # Starting Ogive point at lower bound of first class with 0 cumulative frequency
    upper_boundaries.append(float(round(edges[0], 2)))
    cum_frequencies.append(0)

    for i in range(len(counts)):
        lower = round(edges[i], 2)
        upper = round(edges[i+1], 2)
        freq = int(counts[i])
            
        cum_freq += freq
        rel_freq = freq / total_n
        pct = rel_freq * 100
        midpoint = round((lower + upper) / 2.0, 2)
        interval_label = f"{lower:.2f} - {upper:.2f}"
        
        rows.append({
            "Class Interval": interval_label,
            "Lower Boundary": lower,
            "Upper Boundary": upper,
            "Midpoint": midpoint,
            "Frequency (f)": freq,
            "Cumulative Frequency (CF)": cum_freq,
            "Relative Frequency": round(rel_freq, 4),
            "Percentage (%)": round(pct, 2)
        })
        
        upper_boundaries.append(float(upper))
        cum_frequencies.append(int(cum_freq))

    freq_df = pd.DataFrame(rows)

    
    # Verify cumulative frequency is monotonically non-decreasing
    assert (freq_df["Cumulative Frequency (CF)"].diff().dropna() >= 0).all(), "Cumulative frequency must be non-decreasing!"

    ogive_data = {
        "upper_boundaries": upper_boundaries,
        "cumulative_frequencies": cum_frequencies,
        "total_n": total_n
    }

    return freq_df, ogive_data
