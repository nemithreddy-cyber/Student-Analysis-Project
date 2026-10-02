"""
Scatter Plot Visualization Module.
Generates interactive Plotly scatter plots with OLS regression lines and marginal plots.
"""
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def create_scatter_plot(df, x_col, y_col, show_trendline=True, marginal_type="box"):
    """
    Creates an interactive scatter plot figure comparing x_col and y_col.
    Supports marginal plots ('box', 'histogram', or None).
    """
    paired_df = df[[x_col, y_col] + (["Student_ID"] if "Student_ID" in df.columns else [])].dropna()
    
    if paired_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No paired data available", showarrow=False)
        return fig
        
    hover_data = ["Student_ID"] if "Student_ID" in paired_df.columns else None
    
    fig = px.scatter(
        paired_df,
        x=x_col,
        y=y_col,
        hover_data=hover_data,
        marginal_x=marginal_type if marginal_type != "none" else None,
        marginal_y=marginal_type if marginal_type != "none" else None,
        title=f"Scatter Analysis: {x_col} vs {y_col}",
        labels={x_col: x_col, y_col: y_col},
        template="plotly_dark",
        opacity=0.85
    )

    fig.update_traces(
        marker=dict(size=10, color="#38BDF8", line=dict(width=1, color="#0284C7")),
        selector=dict(type='scatter', mode='markers')
    )

    if show_trendline and len(paired_df) > 1:
        x_vals = paired_df[x_col].values
        y_vals = paired_df[y_col].values
        if np.std(x_vals) > 0:
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
            y_line = slope * x_line + intercept
            
            fig.add_trace(go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name=f"OLS Trendline (y = {slope:.2f}x + {intercept:.2f})",
                line=dict(color="#F43F5E", width=2.5, dash="dash")
            ))

    fig.update_layout(
        title={
            'text': f"<b>Quantitative Association: {x_col} vs {y_col}</b>",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=18, color='#F8FAFC')
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.6)',
        xaxis_title=f"<b>{x_col}</b>",
        yaxis_title=f"<b>{y_col}</b>",
        height=520,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    return fig
