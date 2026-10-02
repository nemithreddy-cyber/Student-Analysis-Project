"""
Histogram Visualization Module.
Generates interactive Plotly histograms with academic styling and Chebyshev interval bounds.
"""
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_histogram(series, num_bins=10, title=None, color_hex="#3B82F6", k_chebyshev=None):
    """
    Creates an interactive Plotly histogram figure for a pandas Series.
    Optionally highlights Chebyshev interval [x̄ - k*s, x̄ + k*s].
    """
    s = series.dropna()
    var_name = s.name if hasattr(s, 'name') and s.name else "Value"
    
    if title is None:
        title = f"Distribution Histogram: {var_name}"
        
    fig = px.histogram(
        s,
        x=var_name,
        nbins=num_bins,
        title=title,
        labels={var_name: var_name, "count": "Frequency (Number of Students)"},
        color_discrete_sequence=[color_hex],
        template="plotly_dark",
        opacity=0.85
    )
    
    fig.update_traces(
        marker_line_color="#60A5FA",
        marker_line_width=1.2,
        hovertemplate=f"<b>{var_name} Range</b>: %{{x}}<br><b>Frequency</b>: %{{y}} students<extra></extra>"
    )
    
    mean_val = float(s.mean())
    std_val = float(s.std(ddof=1)) if len(s) > 1 else 0.0

    # Add Mean vertical line reference
    fig.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color="#EF4444",
        annotation_text=f"Mean (x̄): {mean_val:.2f}",
        annotation_position="top right"
    )

    # Add Chebyshev Interval shading if k provided
    if k_chebyshev is not None and k_chebyshev > 1 and std_val > 0:
        lower_b = mean_val - k_chebyshev * std_val
        upper_b = mean_val + k_chebyshev * std_val

        fig.add_vrect(
            x0=lower_b,
            x1=upper_b,
            fillcolor="#F59E0B",
            opacity=0.2,
            layer="below",
            line_width=1.5,
            line_color="#F59E0B",
            line_dash="dot",
            annotation_text=f"Chebyshev k={k_chebyshev:.1f} Interval [{lower_b:.1f}, {upper_b:.1f}]",
            annotation_position="top left"
        )
    
    fig.update_layout(
        title={
            'text': f"<b>{title}</b>",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=18, color='#F8FAFC')
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.6)',
        xaxis_title=f"<b>{var_name}</b>",
        yaxis_title="<b>Frequency (Count)</b>",
        bargap=0.05,
        height=450,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig
