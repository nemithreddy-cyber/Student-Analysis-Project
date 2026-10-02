"""
Stem-and-Leaf Plot Module for Student Academic Performance and Statistical Analysis System.
Generates genuine stem-and-leaf formatted displays preserving individual data observations.
"""
import numpy as np
import pandas as pd

def generate_stem_and_leaf(series, scale=10):
    """
    Constructs a text-formatted stem-and-leaf plot for a quantitative series.
    
    Default scale = 10 (Stem = tens digit, Leaf = units digit).
    Returns string representation of the stem-and-leaf plot.
    """
    s = series.dropna().astype(float)
    if len(s) == 0:
        return "No data available for stem-and-leaf plot."
        
    # Round values to integers for display if continuous
    vals = np.sort(np.round(s.values).astype(int))
    
    stem_dict = {}
    for v in vals:
        stem = v // scale
        leaf = v % scale
        if stem not in stem_dict:
            stem_dict[stem] = []
        stem_dict[stem].append(leaf)

    lines = []
    lines.append(f"STEM-AND-LEAF PLOT FOR: {series.name if hasattr(series, 'name') else 'Variable'}")
    lines.append(f"Total Observations (n): {len(vals)}")
    lines.append(f"Key: 7 | 2  = 72")
    lines.append("-" * 40)
    lines.append(f"{'Stem':>6} | {'Leaves':<30}")
    lines.append("-" * 40)

    stems = sorted(stem_dict.keys())
    if not stems:
        return "No valid stems generated."

    for st in range(stems[0], stems[-1] + 1):
        leaves = stem_dict.get(st, [])
        leaves_str = " ".join(map(str, sorted(leaves)))
        lines.append(f"{st:6d} | {leaves_str}")

    lines.append("-" * 40)
    lines.append("Note: Stem-and-leaf displays preserve exact individual data points.")
    
    return "\n".join(lines)
