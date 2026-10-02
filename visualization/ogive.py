"""
Ogive Visualization Module.
Generates interactive Less-Than Ogive and Greater-Than Ogive cumulative frequency curves using Plotly.
"""
import plotly.graph_objects as go
import numpy as np

def create_ogive_plot(ogive_data, var_name="Value", color_hex="#10B981", target_percentile=None):
    """
    Constructs a Less-Than Ogive (Cumulative Frequency Curve).
    Includes percentile markers (Q1=25%, Median=50%, Q3=75% or custom target).
    """
    boundaries = ogive_data["upper_boundaries"]
    cum_freqs = ogive_data["cumulative_frequencies"]
    total_n = ogive_data["total_n"]
    
    pcts = [(cf / total_n) * 100 if total_n > 0 else 0 for cf in cum_freqs]
    
    fig = go.Figure()
    
    # Cumulative frequency line trace
    fig.add_trace(go.Scatter(
        x=boundaries,
        y=cum_freqs,
        mode="lines+markers",
        name="Less-Than Ogive (CF)",
        line=dict(color=color_hex, width=3, shape="linear"),
        marker=dict(size=8, color="#047857", symbol="circle"),
        customdata=pcts,
        hovertemplate=(
            f"<b>Upper Class Boundary</b>: %{{x}}<br>"
            f"<b>Cumulative Frequency</b>: %{{y}} students<br>"
            f"<b>Cumulative Percentage</b>: %{{customdata:.1f}}%<extra></extra>"
        )
    ))

    # Add 50% median cumulative line indicator
    half_n = total_n / 2.0
    fig.add_hline(
        y=half_n,
        line_dash="dot",
        line_color="#6B7280",
        annotation_text=f"Median Cutoff (50% CF = {half_n:.1f})",
        annotation_position="bottom right"
    )

    if target_percentile is not None and 0 < target_percentile < 100:
        target_n = (target_percentile / 100.0) * total_n
        fig.add_hline(
            y=target_n,
            line_dash="dash",
            line_color="#8B5CF6",
            annotation_text=f"Target P{target_percentile:.0f} (CF = {target_n:.1f})",
            annotation_position="top left"
        )

    fig.update_layout(
        title={
            'text': f"<b>Less-Than Ogive (Cumulative Frequency Curve): {var_name}</b>",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=18, color='#F8FAFC')
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.6)',
        xaxis_title=f"<b>Upper Class Boundaries ({var_name})</b>",
        yaxis_title="<b>Cumulative Frequency (Students ≤ Upper Boundary)</b>",
        template="plotly_dark",
        height=450,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig
