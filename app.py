"""
Student Academic Performance Analytics System
Streamlit Dashboard Main Application (app.py)
Single Interactive Analytics Workspace
"""
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration - Compact Wide Layout
st.set_page_config(
    page_title="Student Academic Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import internal modules
from config.settings import DEFAULT_CHEBYSHEV_K, DEMO_DATASET_PATH
from modules.data_processing import load_demo_dataset, load_user_dataset, get_dataset_info, sanitize_numeric_data
from modules.validation import validate_dataset
from modules.descriptive_stats import calculate_descriptive_stats
from modules.frequency_analysis import generate_frequency_table
from modules.chebyshev import calculate_chebyshev_analysis
from modules.skewness import analyze_skewness
from modules.scatter_analysis import analyze_scatter_relationship
from modules.interpretations import generate_quick_insights

from visualization.histograms import create_histogram
from visualization.ogive import create_ogive_plot
from visualization.stem_leaf import generate_stem_and_leaf
from visualization.scatter import create_scatter_plot

# Ultra-Compact Dark Analytics Workspace CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
    }

    /* Header Styling */
    .dashboard-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
        padding: 0.9rem 1.4rem;
        border-radius: 10px;
        border: 1px solid #312E81;
        margin-bottom: 0.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .dashboard-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .dashboard-subtitle {
        font-size: 0.85rem;
        color: #94A3B8;
        margin: 0;
    }

    /* KPI Cards */
    .kpi-box {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.6rem 0.8rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .kpi-lbl {
        font-size: 0.72rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-val {
        font-size: 1.45rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0.1rem 0;
    }
    .kpi-sub {
        font-size: 0.7rem;
        color: #38BDF8;
    }

    /* Compact Workspace Cards */
    .card-panel {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Dynamic Result Display */
    .res-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #38BDF8;
        border-radius: 8px;
        padding: 0.9rem 1.2rem;
        margin-top: 0.6rem;
    }
    .res-hdr {
        font-size: 0.78rem;
        font-weight: 700;
        color: #38BDF8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .res-num {
        font-size: 2rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0.1rem 0;
    }
    .res-desc {
        font-size: 0.88rem;
        color: #CBD5E1;
        margin-top: 0.3rem;
    }

    /* Student Profile Badge */
    .badge-chip {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid #0284C7;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }

    /* Formula Box */
    .formula-tag {
        background: #0F172A;
        border-left: 3px solid #818CF8;
        padding: 0.4rem 0.8rem;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.82rem;
        color: #A5B4FC;
        margin: 0.4rem 0;
    }

    /* Remove Streamlit default vertical gaps */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1.5rem !important;
    }
    
    div[data-testid="stExpander"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "dataset" not in st.session_state:
    st.session_state.dataset = load_demo_dataset()
    st.session_state.source_type = "Demo Dataset"
    st.session_state.source_name = "data/students.csv"

# Function to update dataset
def set_dataset(df, source_type, source_name):
    st.session_state.dataset = sanitize_numeric_data(df)
    st.session_state.source_type = source_type
    st.session_state.source_name = source_name

df = st.session_state.dataset

# Default Control Keys Initialization in Session State
if "sel_student_filter" not in st.session_state:
    st.session_state.sel_student_filter = "All Students (100 Students)"
if "sel_metric" not in st.session_state:
    st.session_state.sel_metric = "Final_Marks"
if "sel_stat" not in st.session_state:
    st.session_state.sel_stat = "Mean"
if "sel_graph" not in st.session_state:
    st.session_state.sel_graph = "Histogram"
if "graph_metric" not in st.session_state:
    st.session_state.graph_metric = "Final_Marks"
if "scat_x" not in st.session_state:
    st.session_state.scat_x = "Study_Hours"
if "scat_y" not in st.session_state:
    st.session_state.scat_y = "Final_Marks"
if "p_cutoff" not in st.session_state:
    st.session_state.p_cutoff = 75.0

# Centralized Quick Preset Handler Function (Runs on_click before widget render)
def apply_preset(preset_key):
    st.session_state["sel_student_filter"] = "All Students (100 Students)"
    st.session_state["sel_metric"] = "Final_Marks"
    st.session_state["graph_metric"] = "Final_Marks"
    
    if preset_key == "avg_marks":
        st.session_state["sel_stat"] = "Mean"
        st.session_state["sel_graph"] = "Histogram"
    elif preset_key == "distribution":
        st.session_state["sel_stat"] = "Frequency Distribution"
        st.session_state["sel_graph"] = "Histogram"
    elif preset_key == "att_vs_marks":
        st.session_state["sel_stat"] = "Mean"
        st.session_state["sel_graph"] = "Scatter Plot"
        st.session_state["scat_x"] = "Attendance"
        st.session_state["scat_y"] = "Final_Marks"
    elif preset_key == "hours_vs_marks":
        st.session_state["sel_stat"] = "Mean"
        st.session_state["sel_graph"] = "Scatter Plot"
        st.session_state["scat_x"] = "Study_Hours"
        st.session_state["scat_y"] = "Final_Marks"
    elif preset_key == "trend_comparison":
        st.session_state["sel_stat"] = "Mean"
        st.session_state["sel_graph"] = "Performance Comparison"

# ---------------------------------------------------------
# DASHBOARD HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="dashboard-header">
    <div>
        <div class="dashboard-title">STUDENT ACADEMIC PERFORMANCE ANALYTICS</div>
        <div class="dashboard-subtitle">Interactive Student Performance & Statistical Analysis Workspace</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TOP KPI SUMMARY (CALCULATED FROM ALL STUDENTS)
# ---------------------------------------------------------
total_n = len(df)
overall_avg = df["Final_Marks"].mean() if "Final_Marks" in df.columns else 0.0
overall_med = df["Final_Marks"].median() if "Final_Marks" in df.columns else 0.0
overall_std = df["Final_Marks"].std(ddof=1) if "Final_Marks" in df.columns and total_n > 1 else 0.0
overall_att = df["Attendance"].mean() if "Attendance" in df.columns else 0.0
overall_pass = ((df["Final_Marks"] >= 40.0).sum() / total_n * 100) if "Final_Marks" in df.columns and total_n > 0 else 0.0

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-lbl">TOTAL STUDENTS</div>
        <div class="kpi-val">{total_n}</div>
        <div class="kpi-sub">Cohort Population</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-lbl">AVERAGE MARKS</div>
        <div class="kpi-val">{overall_avg:.1f}</div>
        <div class="kpi-sub">Final Exam Mean</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-lbl">MEDIAN MARKS</div>
        <div class="kpi-val">{overall_med:.1f}</div>
        <div class="kpi-sub">50th Percentile</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-lbl">STANDARD DEVIATION</div>
        <div class="kpi-val">{overall_std:.2f}</div>
        <div class="kpi-sub">Sample Dispersion</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-lbl">AVG ATTENDANCE</div>
        <div class="kpi-val">{overall_att:.1f}%</div>
        <div class="kpi-sub">Class Participation</div>
    </div>
    """, unsafe_allow_html=True)

with k6:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-lbl">PASS RATE</div>
        <div class="kpi-val">{overall_pass:.1f}%</div>
        <div class="kpi-sub">Final Marks ≥ 40</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# COMPACT DATA SOURCE & QUICK PRESETS BAR
# ---------------------------------------------------------
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
ctrl_col1, ctrl_col2 = st.columns([1.2, 2.8])

with ctrl_col1:
    with st.expander("📁 Data Source & Upload", expanded=False):
        d_mode = st.radio("Source Mode", ["Use Demo Data (100 Students)", "Upload CSV / Excel"], label_visibility="collapsed")
        if d_mode == "Use Demo Data (100 Students)":
            if st.button("Reset Demo Data", use_container_width=True):
                demo_df = load_demo_dataset()
                set_dataset(demo_df, "Demo Dataset", "data/students.csv")
                st.rerun()
        else:
            up_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx", "xls"], label_visibility="collapsed")
            if up_file is not None:
                user_df, err = load_user_dataset(up_file)
                if err:
                    st.error(err)
                else:
                    set_dataset(user_df, "User Upload", up_file.name)
                    st.success(f"Loaded {len(user_df)} rows.")
                    st.rerun()
                    
        st.markdown(f"**Active Data**: `{st.session_state.source_type}` ({len(df)} rows)")
        with st.expander("👁️ View Dataset Table", expanded=False):
            st.dataframe(df, use_container_width=True, height=200)

with ctrl_col2:
    st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#94A3B8; margin-bottom:0.2rem;'>⚡ QUICK ANALYTICS PRESETS</div>", unsafe_allow_html=True)
    p_c1, p_c2, p_c3, p_c4, p_c5 = st.columns(5)
    
    with p_c1:
        st.button("📊 Avg Marks", on_click=apply_preset, args=("avg_marks",), use_container_width=True)
    with p_c2:
        st.button("📈 Distribution", on_click=apply_preset, args=("distribution",), use_container_width=True)
    with p_c3:
        st.button("🤝 Att vs Marks", on_click=apply_preset, args=("att_vs_marks",), use_container_width=True)
    with p_c4:
        st.button("⏱️ Hours vs Marks", on_click=apply_preset, args=("hours_vs_marks",), use_container_width=True)
    with p_c5:
        st.button("📉 Trend Comparison", on_click=apply_preset, args=("trend_comparison",), use_container_width=True)

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN ANALYSIS WORKSPACE
# ---------------------------------------------------------
st.markdown('<div class="card-panel">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📌 ANALYZE STUDENT PERFORMANCE</div>', unsafe_allow_html=True)

numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c != "Student_ID"]
if not numeric_cols:
    numeric_cols = ["Final_Marks"]

student_options = ["All Students (100 Students)"]
if "Student_ID" in df.columns:
    student_options += list(df["Student_ID"].dropna().astype(str).unique())

c_stud, c_metric, c_stat = st.columns(3)

with c_stud:
    selected_student = st.selectbox("Student / Group", options=student_options, key="sel_student_filter")

with c_metric:
    selected_metric = st.selectbox("Academic Variable", options=numeric_cols, key="sel_metric")

stat_options = [
    "Mean",
    "Median",
    "Mode",
    "Minimum",
    "Maximum",
    "Range",
    "Sample Variance (s²)",
    "Sample Standard Deviation (s)",
    "Skewness Analysis",
    "Frequency Distribution",
    "Chebyshev Inequality Bounds",
    "Empirical Probability"
]
with c_stat:
    selected_stat = st.selectbox("Analysis Type", options=stat_options, key="sel_stat")

# Filter dataset based on selection
if selected_student.startswith("All Students"):
    sub_df = df.copy()
    student_label = f"all {len(sub_df)} selected students"
    is_group = True
else:
    sub_df = df[df["Student_ID"].astype(str) == selected_student].copy()
    student_label = f"Student {selected_student}"
    is_group = False

series = sub_df[selected_metric].dropna()

# Extra parameters for specific analysis types
chebyshev_k = DEFAULT_CHEBYSHEV_K
prob_cutoff = 75.0

if selected_stat == "Chebyshev Inequality Bounds":
    chebyshev_k = st.slider("Select Chebyshev Multiplier (k > 1)", min_value=1.1, max_value=4.0, value=2.0, step=0.1)

elif selected_stat == "Empirical Probability":
    prob_cutoff = st.number_input(f"Threshold Cutoff (c) for P({selected_metric} ≥ c)", value=float(np.round(df[selected_metric].median(), 1)) if selected_metric in df else 50.0)

# DYNAMIC RESULT CARD
if len(series) == 0:
    st.warning("No valid numeric observations available for the selected target.")
else:
    stats_summary = calculate_descriptive_stats(series)

    # Individual Student Profile & Performance Delta Display (Only if individual student selected)
    if not is_group and len(sub_df) == 1:
        s_row = sub_df.iloc[0]
        st.markdown(f"**Individual Student Profile**: <span class='badge-chip'>{selected_student}</span>", unsafe_allow_html=True)
        sp_cols = st.columns(min(len(numeric_cols), 6))
        for idx, col in enumerate(numeric_cols[:6]):
            with sp_cols[idx]:
                st.metric(col.replace("_", " "), f"{s_row[col]:.1f}" if pd.notnull(s_row[col]) else "N/A")

        if "Previous_Marks" in s_row and "Current_Marks" in s_row and pd.notnull(s_row["Previous_Marks"]) and pd.notnull(s_row["Current_Marks"]):
            prev_m = float(s_row["Previous_Marks"])
            curr_m = float(s_row["Current_Marks"])
            diff = curr_m - prev_m
            pct_chg = (diff / prev_m * 100) if prev_m > 0 else 0.0
            trend_str = "Improved 📈" if diff > 0 else ("Declined 📉" if diff < 0 else "No Change ➖")
            
            st.markdown(f"""
            <div class="res-card" style="border-color: #818CF8; margin-bottom: 0.6rem;">
                <div class="res-hdr">PERFORMANCE CHANGE (PREVIOUS VS CURRENT MARKS)</div>
                <div class="res-num" style="font-size:1.35rem;">Previous: {prev_m:.1f} ➔ Current: {curr_m:.1f} ({diff:+.1f} marks / {pct_chg:+.1f}%)</div>
                <div class="res-desc">Classification: <b>{trend_str}</b> (Descriptive delta across evaluation periods).</div>
            </div>
            """, unsafe_allow_html=True)

    # 1. MEAN
    if selected_stat == "Mean":
        val = stats_summary["mean"]
        st.markdown(f"""
        <div class="res-card">
            <div class="res-hdr">MEAN — {selected_metric.replace('_', ' ')}</div>
            <div class="res-num">{val:.2f}</div>
            <div class="res-desc">The average {selected_metric.replace('_', ' ')} for the {student_label} is <b>{val:.2f}</b>.</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. MEDIAN
    elif selected_stat == "Median":
        val = stats_summary["median"]
        st.markdown(f"""
        <div class="res-card">
            <div class="res-hdr">MEDIAN — {selected_metric.replace('_', ' ')}</div>
            <div class="res-num">{val:.2f}</div>
            <div class="res-desc">50% of observations in {selected_metric.replace('_', ' ')} fall below or equal to <b>{val:.2f}</b>.</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. MODE
    elif selected_stat == "Mode":
        val_str = stats_summary["mode"]
        st.markdown(f"""
        <div class="res-card">
            <div class="res-hdr">MODE — {selected_metric.replace('_', ' ')}</div>
            <div class="res-num" style="font-size:1.5rem;">{val_str}</div>
            <div class="res-desc">Most frequently occurring value(s) in {selected_metric.replace('_', ' ')}.</div>
        </div>
        """, unsafe_allow_html=True)

    # 4. MIN / MAX
    elif selected_stat in ["Minimum", "Maximum"]:
        val = stats_summary["min"] if selected_stat == "Minimum" else stats_summary["max"]
        st.markdown(f"""
        <div class="res-card">
            <div class="res-hdr">{selected_stat.upper()} — {selected_metric.replace('_', ' ')}</div>
            <div class="res-num">{val:.2f}</div>
            <div class="res-desc">The {selected_stat.lower()} value observed in {selected_metric.replace('_', ' ')} is <b>{val:.2f}</b>.</div>
        </div>
        """, unsafe_allow_html=True)

    # 5. RANGE
    elif selected_stat == "Range":
        val = stats_summary["range"]
        st.markdown(f"""
        <div class="res-card">
            <div class="res-hdr">RANGE (MAX - MIN) — {selected_metric.replace('_', ' ')}</div>
            <div class="res-num">{val:.2f}</div>
            <div class="res-desc">The total spread between highest ({stats_summary['max']:.1f}) and lowest ({stats_summary['min']:.1f}) values is <b>{val:.2f}</b>.</div>
        </div>
        """, unsafe_allow_html=True)

    # 6. SAMPLE VARIANCE
    elif selected_stat == "Sample Variance (s²)":
        if not is_group and len(series) < 2:
            st.info("ℹ️ Variance calculation requires multiple observations (n ≥ 2). Select 'All Students'.")
        else:
            val = stats_summary["variance"]
            st.markdown(f"""
            <div class="res-card">
                <div class="res-hdr">SAMPLE VARIANCE (s²) — {selected_metric.replace('_', ' ')}</div>
                <div class="res-num">{val:.2f}</div>
                <div class="formula-tag">s² = Σ(x - x̄)² / (n - 1) &nbsp;&nbsp;(unbiased sample variance, ddof=1)</div>
                <div class="res-desc">Measures average squared deviation of {selected_metric.replace('_', ' ')} from sample mean.</div>
            </div>
            """, unsafe_allow_html=True)

    # 7. SAMPLE STANDARD DEVIATION
    elif selected_stat == "Sample Standard Deviation (s)":
        if not is_group and len(series) < 2:
            st.info("ℹ️ Standard deviation requires multiple observations (n ≥ 2). Select 'All Students'.")
        else:
            val = stats_summary["std_dev"]
            st.markdown(f"""
            <div class="res-card">
                <div class="res-hdr">SAMPLE STANDARD DEVIATION (s) — {selected_metric.replace('_', ' ')}</div>
                <div class="res-num">{val:.2f}</div>
                <div class="formula-tag">s = √[ Σ(x - x̄)² / (n - 1) ]</div>
                <div class="res-desc">{selected_metric.replace('_', ' ')} typically varies by approximately <b>{val:.2f}</b> units around the mean.</div>
            </div>
            """, unsafe_allow_html=True)

    # 8. SKEWNESS
    elif selected_stat == "Skewness Analysis":
        if not is_group and len(series) < 3:
            st.info("ℹ️ Skewness analysis requires multiple observations (n ≥ 3). Select 'All Students'.")
        else:
            skew_res = analyze_skewness(series)
            val = skew_res["skewness"]
            cls = skew_res["classification"]
            st.markdown(f"""
            <div class="res-card">
                <div class="res-hdr">FISHER-PEARSON SKEWNESS (g₁) — {selected_metric.replace('_', ' ')}</div>
                <div class="res-num">{val:.3f}</div>
                <div class="res-desc">Classification: <b>{cls}</b>. {skew_res['interpretation']}<br><small style="color:#F59E0B;">⚠️ <i>Disclaimer: Skewness alone does not establish normality.</i></small></div>
            </div>
            """, unsafe_allow_html=True)

    # 9. CHEBYSHEV
    elif selected_stat == "Chebyshev Inequality Bounds":
        if not is_group and len(series) < 2:
            st.info("ℹ️ Chebyshev bounds require multiple observations (n ≥ 2). Select 'All Students'.")
        else:
            cheb_res = calculate_chebyshev_analysis(series, k=chebyshev_k)
            t_bound = cheb_res["theoretical_lower_bound"]
            o_pct = cheb_res["actual_percentage"]
            st.markdown(f"""
            <div class="res-card">
                <div class="res-hdr">CHEBYSHEV'S INEQUALITY (k = {chebyshev_k:.1f}) — {selected_metric.replace('_', ' ')}</div>
                <div class="res-num" style="font-size:1.4rem;">Theoretical Guarantee: ≥ {t_bound:.1f}% &nbsp;|&nbsp; Observed Data: {o_pct:.1f}%</div>
                <div class="res-desc">
                    • Mean (x̄) = {cheb_res['mean']:.2f}, Std Dev (s) = {cheb_res['std_dev']:.2f}<br>
                    • Interval [x̄ - {chebyshev_k}s, x̄ + {chebyshev_k}s]: <b>[{cheb_res['lower_bound']:.2f}, {cheb_res['upper_bound']:.2f}]</b><br>
                    • Actual records in range: <b>{cheb_res['count_in_range']} / {cheb_res['n']} students ({o_pct:.1f}%)</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 10. FREQUENCY DISTRIBUTION
    elif selected_stat == "Frequency Distribution":
        if not is_group and len(series) < 2:
            st.info("ℹ️ Frequency distribution requires multiple observations (n ≥ 2). Select 'All Students'.")
        else:
            freq_df, _ = generate_frequency_table(series)
            st.markdown(f"**Grouped Frequency Table**: `{selected_metric.replace('_', ' ')}`")
            st.dataframe(freq_df, use_container_width=True, height=180)

    # 11. EMPIRICAL PROBABILITY
    elif selected_stat == "Empirical Probability":
        count_sat = (series >= prob_cutoff).sum()
        emp_p = count_sat / len(series) if len(series) > 0 else 0.0
        st.markdown(f"""
        <div class="res-card">
            <div class="res-hdr">EMPIRICAL PROBABILITY — P({selected_metric.replace('_', ' ')} ≥ {prob_cutoff})</div>
            <div class="res-num">{emp_p:.4f} ({emp_p*100:.2f}%)</div>
            <div class="res-desc">
                Satisfying observations: <b>{count_sat} / {len(series)} selected observations</b>.<br>
                <i>Empirical probability based on the selected historical cohort dataset.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VISUALIZATION WORKSPACE
# ---------------------------------------------------------
st.markdown('<div class="card-panel">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📈 VISUALIZE PERFORMANCE</div>', unsafe_allow_html=True)

v_col1, v_col2, v_col3 = st.columns([1.2, 1.2, 1])

graph_options = [
    "Histogram",
    "Ogive",
    "Frequency Distribution",
    "Stem-and-Leaf",
    "Scatter Plot",
    "Performance Comparison"
]

with v_col1:
    selected_graph_type = st.selectbox("Graph Type", options=graph_options, key="sel_graph")

with v_col2:
    if selected_graph_type in ["Histogram", "Ogive", "Frequency Distribution", "Stem-and-Leaf"]:
        v_metric = st.selectbox("Graph Variable", options=numeric_cols, key="graph_metric")
    elif selected_graph_type == "Scatter Plot":
        v_x_metric = st.selectbox("X Variable (Horizontal)", options=numeric_cols, key="scat_x")
    elif selected_graph_type == "Performance Comparison":
        st.caption("Compares Previous_Marks vs Current_Marks.")

with v_col3:
    if selected_graph_type in ["Histogram", "Ogive"]:
        num_bins_val = st.slider("Bins / Intervals", min_value=5, max_value=25, value=10, key="bin_slider")
    elif selected_graph_type == "Scatter Plot":
        v_y_metric = st.selectbox("Y Variable (Vertical)", options=numeric_cols, key="scat_y")

# GRAPH RENDERER WITH DISTRIBUTION GUARD FOR SINGLE STUDENT
if selected_graph_type in ["Histogram", "Ogive", "Frequency Distribution", "Stem-and-Leaf"] and not is_group and len(sub_df) < 2:
    st.info(f"ℹ️ {selected_graph_type} requires a cohort group of observations (n ≥ 2). Please select 'All Students' in the Student / Group filter.")

elif selected_graph_type == "Scatter Plot" and not is_group and len(sub_df) < 2:
    st.info("ℹ️ Scatter plot requires paired observations from multiple students (n ≥ 2). Please select 'All Students'.")

else:
    if selected_graph_type == "Histogram":
        g_series = sub_df[v_metric].dropna()
        if len(g_series) >= 2:
            fig_hist = create_histogram(g_series, num_bins=num_bins_val, k_chebyshev=chebyshev_k if selected_stat == "Chebyshev Inequality Bounds" else None)
            st.plotly_chart(fig_hist, use_container_width=True)

    elif selected_graph_type == "Ogive":
        g_series = sub_df[v_metric].dropna()
        if len(g_series) >= 2:
            freq_df, freq_summary = generate_frequency_table(g_series, num_bins=num_bins_val)
            ogive_data = {
                "upper_boundaries": freq_summary["upper_boundaries"],
                "cumulative_frequencies": freq_summary["cumulative_frequencies"],
                "total_n": len(g_series)
            }
            fig_ogive = create_ogive_plot(ogive_data, var_name=v_metric)
            st.plotly_chart(fig_ogive, use_container_width=True)

    elif selected_graph_type == "Frequency Distribution":
        g_series = sub_df[v_metric].dropna()
        if len(g_series) >= 2:
            freq_df, _ = generate_frequency_table(g_series)
            st.dataframe(freq_df, use_container_width=True, height=200)

    elif selected_graph_type == "Stem-and-Leaf":
        g_series = sub_df[v_metric].dropna()
        if len(g_series) >= 2:
            stem_txt = generate_stem_and_leaf(g_series)
            st.code(stem_txt, language="text")

    elif selected_graph_type == "Scatter Plot":
        cur_x = st.session_state.get("scat_x", "Study_Hours")
        cur_y = st.session_state.get("scat_y", "Final_Marks")
        if cur_x in sub_df.columns and cur_y in sub_df.columns:
            paired_obs = sub_df[[cur_x, cur_y]].dropna()
            if len(paired_obs) < 2:
                st.info("ℹ️ At least two valid paired observations are required for scatter plot analysis. Select 'All Students'.")
            else:
                fig_scat = create_scatter_plot(sub_df, x_col=cur_x, y_col=cur_y, show_trendline=True)
                st.plotly_chart(fig_scat, use_container_width=True)
                
                scat_info = analyze_scatter_relationship(sub_df, cur_x, cur_y)
                if not scat_info.get("error"):
                    r_val = scat_info["r_value"]
                    assoc_dir = "positive" if r_val > 0.2 else ("negative" if r_val < -0.2 else "weak/none")
                    st.markdown(f"<div style='font-size:0.82rem; color:#94A3B8; margin-top:0.2rem;'>💡 <b>Scatter Insight</b>: <b>{cur_x.replace('_', ' ')}</b> and <b>{cur_y.replace('_', ' ')}</b> show a <b>{assoc_dir} visual association</b> (Correlation r = {r_val:.2f}). (<i>Academic Disclaimer: Association does not imply causation</i>).</div>", unsafe_allow_html=True)
                else:
                    st.warning(scat_info.get("message", "Unable to compute scatter correlation."))
        else:
            st.warning("Please select valid X and Y variables.")

    elif selected_graph_type == "Performance Comparison":
        if "Previous_Marks" in sub_df.columns and "Current_Marks" in sub_df.columns:
            if is_group:
                trend_df = sub_df[["Student_ID", "Previous_Marks", "Current_Marks"]].dropna().head(30)
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Bar(x=trend_df["Student_ID"], y=trend_df["Previous_Marks"], name="Previous Marks", marker_color="#818CF8"))
                fig_trend.add_trace(go.Bar(x=trend_df["Student_ID"], y=trend_df["Current_Marks"], name="Current Marks", marker_color="#38BDF8"))
                fig_trend.update_layout(
                    title="<b>Student Performance Comparison: Previous vs Current Evaluation</b>",
                    barmode="group",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(15,23,42,0.6)',
                    xaxis_title="Student ID",
                    yaxis_title="Marks (out of 100)",
                    height=380,
                    margin=dict(l=30, r=30, t=50, b=30)
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                s_row = sub_df.iloc[0]
                prev_m = float(s_row["Previous_Marks"])
                curr_m = float(s_row["Current_Marks"])
                diff = curr_m - prev_m
                pct_chg = (diff / prev_m * 100) if prev_m > 0 else 0.0
                st.markdown(f"#### Performance Comparison for `{selected_student}`")
                st.markdown(f"- **Previous Marks**: {prev_m:.1f}")
                st.markdown(f"- **Current Marks**: {curr_m:.1f}")
                st.markdown(f"- **Change**: {diff:+.1f} marks ({pct_chg:+.2f}%)")
                st.markdown(f"- **Classification**: **{'Improved' if diff > 0 else ('Declined' if diff < 0 else 'No Change')}**")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# COMPACT KEY INSIGHTS (ALWAYS INDEPENDENT & SAFE)
# ---------------------------------------------------------
st.markdown('<div class="card-panel">', unsafe_allow_html=True)
st.markdown('<div class="card-title">💡 KEY INSIGHTS</div>', unsafe_allow_html=True)

try:
    cur_scat_x = st.session_state.get("scat_x", "Study_Hours")
    cur_scat_y = st.session_state.get("scat_y", "Final_Marks")
    insights_list = generate_quick_insights(
        df,
        selected_graph=selected_graph_type,
        scat_x=cur_scat_x if selected_graph_type == "Scatter Plot" else None,
        scat_y=cur_scat_y if selected_graph_type == "Scatter Plot" else None
    )
    for insight in insights_list[:4]:
        st.markdown(f"• {insight}")
except Exception as e:
    st.markdown(f"• **Sample Size**: Analysis is based on a cohort of **{len(df)} student records**.")
    st.markdown(f"• **Final Marks Overview**: Mean final mark is **{df['Final_Marks'].mean():.2f}** with median **{df['Final_Marks'].median():.2f}**.")

st.markdown('</div>', unsafe_allow_html=True)

