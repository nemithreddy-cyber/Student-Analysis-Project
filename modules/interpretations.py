"""
Automatic Interpretations Module for Student Academic Performance and Statistical Analysis System.
Generates dynamically calculated, academically rigorous statistical interpretations.
"""

def generate_quick_insights(df, selected_graph=None, scat_x=None, scat_y=None):
    """
    Generates high-level statistical bullet insights for the dashboard home page.
    Guaranteed to run safely without breaking the dashboard rendering.
    """
    insights = []
    if df is None or df.empty:
        return ["No active dataset available for insights."]

    num_students = len(df)
    insights.append(f"**Sample Size**: Analysis is based on a cohort of **{num_students} student records**.")

    if "Final_Marks" in df.columns and len(df) > 0:
        mean_fm = df["Final_Marks"].mean()
        med_fm = df["Final_Marks"].median()
        std_fm = df["Final_Marks"].std(ddof=1) if len(df) > 1 else 0.0
        insights.append(
            f"**Final Marks Overview**: Mean final mark is **{mean_fm:.2f}** with median **{med_fm:.2f}** and standard deviation **{std_fm:.2f}**."
        )

    if "Attendance" in df.columns and len(df) > 0:
        mean_att = df["Attendance"].mean()
        insights.append(f"**Attendance Level**: Average student attendance rate across the dataset is **{mean_att:.1f}%**.")

    if "Study_Hours" in df.columns and len(df) > 0:
        mean_sh = df["Study_Hours"].mean()
        insights.append(f"**Study Habit**: Average reported daily study time is **{mean_sh:.1f} hours** per day.")

    # Contextual Relationship / Trend Insight based on active graph / preset
    if selected_graph == "Scatter Plot" and scat_x and scat_y and scat_x in df.columns and scat_y in df.columns and len(df) > 2:
        try:
            from modules.scatter_analysis import analyze_scatter_relationship
            sc_info = analyze_scatter_relationship(df, scat_x, scat_y)
            if not sc_info.get("error"):
                r_val = sc_info.get("r_value", 0.0)
                assoc_type = sc_info.get("association_type", "Visual Association")
                insights.append(f"**Relationship Insight**: **{scat_x.replace('_', ' ')}** and **{scat_y.replace('_', ' ')}** show a **{assoc_type.lower()}** (r = {r_val:.2f}). (<i>Academic Disclaimer: Association does not imply causation</i>).")
        except Exception:
            pass

    elif selected_graph == "Performance Comparison" and "Previous_Marks" in df.columns and "Current_Marks" in df.columns and len(df) > 0:
        avg_prev = df["Previous_Marks"].mean()
        avg_curr = df["Current_Marks"].mean()
        avg_diff = avg_curr - avg_prev
        pct_diff = (avg_diff / avg_prev * 100) if avg_prev > 0 else 0.0
        improved_count = (df["Current_Marks"] > df["Previous_Marks"]).sum()
        pct_improved = (improved_count / len(df)) * 100
        insights.append(f"**Performance Trend**: Average Previous: **{avg_prev:.1f}** ➔ Average Current: **{avg_curr:.1f}** (Change: **{avg_diff:+.1f}** / **{pct_diff:+.1f}%**). **{pct_improved:.1f}%** of students ({improved_count}/{len(df)}) demonstrated academic improvement.")

    else:
        # Fallback relationship insight between Study_Hours and Final_Marks if present
        if "Study_Hours" in df.columns and "Final_Marks" in df.columns and len(df) > 2:
            try:
                corr = df["Study_Hours"].corr(df["Final_Marks"])
                if pd.notnull(corr):
                    insights.append(f"**Observed Pattern**: Study Hours and Final Marks show a positive visual association (r = {corr:.2f}).")
            except Exception:
                pass

        if "Previous_Marks" in df.columns and "Current_Marks" in df.columns and len(df) > 0:
            improved_count = (df["Current_Marks"] > df["Previous_Marks"]).sum()
            pct_improved = (improved_count / len(df)) * 100
            insights.append(f"**Performance Trend**: **{pct_improved:.1f}%** of students ({improved_count}/{len(df)}) demonstrated academic improvement compared to their previous assessment.")

    return insights

def format_stat_interpretation(col_name, stats_dict):
    """
    Generates a formal paragraph summarizing central tendency and dispersion for a specific variable.
    """
    mean = stats_dict["mean"]
    median = stats_dict["median"]
    std_dev = stats_dict["std_dev"]
    variance = stats_dict["variance"]
    rng = stats_dict["range"]
    n = stats_dict["n"]
    
    text = (
        f"For the variable **'{col_name}'** (n = {n}):\n\n"
        f"- **Central Tendency**: The sample mean is **{mean:.2f}**, while the median is **{median:.2f}**. "
        f"The mode is reported as **{stats_dict['mode']}**.\n"
        f"- **Variability**: The sample standard deviation is **{std_dev:.2f}** units around the mean, "
        f"with a sample variance of **{variance:.2f}** and an overall range of **{rng:.2f}** "
        f"(Minimum: {stats_dict['min']:.2f}, Maximum: {stats_dict['max']:.2f}).\n"
    )
    return text
