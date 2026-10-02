"""
Report Generator Module for Student Academic Performance and Statistical Analysis System.
Consolidates active dataset statistics, validation status, and insights into exportable reports.
"""
from datetime import datetime
import pandas as pd
import numpy as np
from modules.descriptive_stats import get_summary_table_for_all_numeric
from modules.validation import validate_dataset
from modules.chebyshev import calculate_chebyshev_analysis
from modules.skewness import analyze_skewness
from modules.scatter_analysis import analyze_scatter_relationship

def generate_text_report(df, dataset_name="Active Dataset", is_demo=True):
    """
    Generates a full structured statistical report in Markdown/Text format.
    Calculates all numbers dynamically from the active DataFrame.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    val_res = validate_dataset(df)
    stats_df = get_summary_table_for_all_numeric(df)
    
    source_type = "Demonstration Dataset" if is_demo else "User Uploaded Approved Dataset"
    
    report_lines = [
        "=" * 70,
        "STUDENT ACADEMIC PERFORMANCE & STATISTICAL ANALYSIS SYSTEM",
        "FINAL STATISTICAL REPORT (MODULE I - DESCRIPTIVE STATISTICS)",
        "=" * 70,
        f"Report Generation Time: {timestamp}",
        f"Data Source: {dataset_name} ({source_type})",
        f"Total Records Analyzed: {len(df)}",
        f"Total Variables: {len(df.columns)}",
        f"Validation Status: {val_res['overall_status']}",
        "=" * 70,
        "",
        "1. DATASET OVERVIEW & SCHEMA",
        "-" * 40,
        f"- Number of Students (n): {len(df)}",
        f"- Columns: {', '.join(df.columns)}",
        f"- Missing Values: {val_res['summary_counts']['errors'] + val_res['summary_counts']['warnings']} issues noted.",
        "",
        "2. DESCRIPTIVE STATISTICS SUMMARY",
        "-" * 40,
        stats_df.to_string(index=False),
        "",
        "3. CHEBYSHEV'S INEQUALITY ANALYSIS (k = 2.0)",
        "-" * 40
    ]

    if "Final_Marks" in df.columns:
        cheb = calculate_chebyshev_analysis(df["Final_Marks"], k=2.0)
        if not cheb.get("error"):
            report_lines.extend([
                f"Variable Analyzed: Final_Marks",
                f"- Mean (x̄): {cheb['mean']:.2f}, Std Dev (s): {cheb['std_dev']:.2f}",
                f"- Selected k: {cheb['k']:.2f}",
                f"- Theoretical Minimum Lower Bound (1 - 1/k²): {cheb['theoretical_bound_pct']:.2f}%",
                f"- Chebyshev Interval [x̄ - k*s, x̄ + k*s]: [{cheb['lower_interval']:.2f}, {cheb['upper_interval']:.2f}]",
                f"- Actual Observed Percentage in Interval: {cheb['observed_pct']:.2f}% ({cheb['observed_count']}/{cheb['n']} students)",
                f"- Compliance Note: Observed percentage ({cheb['observed_pct']:.2f}%) exceeds theoretical lower bound guarantee ({cheb['theoretical_bound_pct']:.2f}%)."
            ])
            
    report_lines.extend([
        "",
        "4. SKEWNESS & DISTRIBUTION SYMMETRY",
        "-" * 40
    ])

    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        sk = analyze_skewness(df[col])
        report_lines.append(f"- {col}: Skewness = {sk['skewness']:.3f} -> {sk['classification']}")

    report_lines.extend([
        "",
        "5. PAIRED SCATTER PLOT ASSOCIATIONS",
        "-" * 40
    ])

    pairs = [("Study_Hours", "Final_Marks"), ("Attendance", "Final_Marks")]
    for x_col, y_col in pairs:
        if x_col in df.columns and y_col in df.columns:
            sc = analyze_scatter_relationship(df, x_col, y_col)
            if not sc.get("error"):
                report_lines.append(f"- {x_col} vs {y_col}: Pearson r = {sc['correlation']:.3f} ({sc['association_type']})")

    report_lines.extend([
        "",
        "6. KEY ACADEMIC OBSERVATIONS & FINDINGS",
        "-" * 40,
        "1. Central tendency metrics provide benchmark averages for student cohort performance.",
        "2. Dispersion measures (variance and standard deviation) highlight variation among individual students.",
        "3. Chebyshev's inequality guarantees minimum proportion bounds regardless of underlying distribution shape.",
        "4. Visual scatter plots illustrate association tendencies but do NOT imply direct causal relationship.",
        "",
        "7. PROJECT LIMITATIONS",
        "-" * 40,
        "1. Analysis quality depends directly on accuracy and representativeness of input dataset.",
        "2. Self-reported metrics (e.g. daily study hours) may contain measurement error or reporting bias.",
        "3. A single sample cohort may not generalize to wider academic populations.",
        "4. Current scope is strictly descriptive (Module I) and excludes formal hypothesis testing or inferential regression.",
        "",
        "8. FUTURE SCOPE & EXTENSIONS",
        "-" * 40,
        "- Extension to Probability Theory, Random Variables, Binomial/Poisson distributions.",
        "- Normal, Uniform, Gamma, Exponential, and Beta distribution fitting.",
        "- Sampling distributions, confidence intervals, and hypothesis testing (t-tests, ANOVA).",
        "- Inferential Pearson/Spearman correlation and simple/multiple regression modeling.",
        "",
        "=" * 70,
        "END OF STATISTICAL REPORT",
        "=" * 70
    ])

    return "\n".join(report_lines)
