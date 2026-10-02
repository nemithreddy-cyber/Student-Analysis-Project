"""
Normal Datasets Visualization Module.
Generates Q-Q plots and Normal PDF overlay histograms.
"""
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats

def create_qq_plot(qq_theoretical, qq_sample, var_name="Value"):
    """
    Creates an interactive Q-Q plot comparing empirical quantiles against theoretical normal quantiles.
    """
    fig = go.Figure()

    # Scatter points for Q-Q plot
    fig.add_trace(go.Scatter(
        x=qq_theoretical,
        y=qq_sample,
        mode="markers",
        name="Data Quantiles",
        marker=dict(size=8, color="#6366F1", symbol="circle", line=dict(width=1, color="#312E81")),
        hovertemplate="Theoretical Quantile: %{x:.2f}<br>Sample Quantile: %{y:.2f}<extra></extra>"
    ))

    # Reference 45-degree / reference line y = x
    min_val = min(min(qq_theoretical), min(qq_sample))
    max_val = max(max(qq_theoretical), max(qq_sample))
    
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode="lines",
        name="Normal Ideal Line (y = x)",
        line=dict(color="#EF4444", width=2, dash="dash")
    ))

    fig.update_layout(
        title=f"<b>Q-Q Plot (Normal Probability Alignment): {var_name}</b>",
        xaxis_title="<b>Theoretical Normal Quantiles</b>",
        yaxis_title=f"<b>Sample Quantiles ({var_name})</b>",
        template="plotly_white",
        height=450,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    return fig

def create_histogram_with_normal_pdf(series, var_name="Value", num_bins=10):
    """
    Histogram overlaid with theoretical Gaussian Normal Curve N(μ, σ²).
    """
    s = series.dropna()
    mean_val = float(s.mean())
    std_val = float(s.std(ddof=1))

    fig = go.Figure()

    # Density Histogram
    fig.add_trace(go.Histogram(
        x=s,
        nbinsx=num_bins,
        histnorm="probability density",
        name="Sample Density",
        marker=dict(color="#3B82F6", line=dict(color="#1E3A8A", width=1.2)),
        opacity=0.65
    ))

    # Normal PDF Curve
    x_range = np.linspace(mean_val - 4 * std_val, mean_val + 4 * std_val, 200)
    pdf_y = stats.norm.pdf(x_range, loc=mean_val, scale=std_val)

    fig.add_trace(go.Scatter(
        x=x_range,
        y=pdf_y,
        mode="lines",
        name=f"Normal PDF N({mean_val:.1f}, {std_val:.1f}²)",
        line=dict(color="#DC2626", width=3)
    ))

    fig.update_layout(
        title=f"<b>Histogram with Fitted Normal PDF Curve: {var_name}</b>",
        xaxis_title=f"<b>{var_name}</b>",
        yaxis_title="<b>Probability Density</b>",
        template="plotly_white",
        bargap=0.05,
        height=450,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
