import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def highlight_chart(df,
                    x_value,
                    y_value,
                    trace_name,
                    highlight_traces,
                    xaxis_title="", yaxis_title="", chart_name="",
                    width=1600, height=800, template='plotly_white'):
    """
    Generates a Plotly figure with highlighted traces.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        x_value (str): The name of the column to use for the x-axis.
        y_value (str): The name of the column to use for the y-axis.
        trace_name (str): The name of the column that identifies different traces (e.g., countries).
        highlight_traces (list): A list of trace names to highlight with different colors.
        xaxis_title (str, optional): Title for the x-axis. Defaults to "".
        yaxis_title (str, optional): Title for the y-axis. Defaults to "".
        chart_name (str, optional): Title for the chart. Defaults to "".
        width (int, optional): Width of the chart in pixels. Defaults to 1600.
        height (int, optional): Height of the chart in pixels. Defaults to 800.
        template (str, optional): Plotly template to use. Defaults to 'plotly_white'.

    Returns:
        plotly.graph_objects.Figure: The generated Plotly figure.
    """
    # Create the base figure
    fig = go.Figure()

    # Plot all traces in grey
    for t_name in df[trace_name].unique():
        t_df = df[df[trace_name] == t_name]
        fig.add_trace(go.Scatter(
            x=t_df[x_value],
            y=t_df[y_value],
            mode='lines',
            line=dict(color='#E8E8E8', width=1),
            showlegend=False  # Hide legend for grey lines
        ))


    # Overlay selected countries in color
    colors = px.colors.qualitative.Plotly
    for t_name, color in zip(highlight_traces, colors):
        t_df = df[df[trace_name] == t_name]
        fig.add_trace(go.Scatter(
            x=t_df[x_value],
            y=t_df[y_value],
            mode='lines',
            name=t_name,
            line=dict(color=color, width=4)
        ))

    # Update layout
    fig.update_layout(
        title=chart_name,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        height = height,
        width = width,
        template=template
    )
    return fig

# Load the data
df = pd.read_csv('rate.csv', sep=';')

chart_name='Fertility Rate by Country'
xaxis_title='Year'
yaxis_title='Fertiity Rate' # Typo: Should be 'Fertility Rate'
template='simple_white'

# column names
y_value = 'Fertility Rate'
x_value = 'Year'
trace_name = 'Region'


# Get unique regions for the selector
all_regions = sorted(df[trace_name].unique())

# Default list of countries to highlight
default_highlight_traces = ['World','Spain','India','Brazil','United States of America']

# Streamlit multiselect widget for highlighting traces
st.sidebar.header("Chart Options") # Optional: Add a header in the sidebar
highlight_traces = st.sidebar.multiselect(
    "Select regions to highlight:",
    options=all_regions,
    default=[region for region in default_highlight_traces if region in all_regions] # Ensure defaults are valid
)

# Corrected yaxis_title
yaxis_title='Fertility Rate'


if highlight_traces: # Only generate chart if at least one region is selected
    fig = highlight_chart(df,x_value=x_value, y_value=y_value,
                          trace_name=trace_name,
                          highlight_traces=highlight_traces,
                          xaxis_title=xaxis_title,
                          yaxis_title=yaxis_title,
                          chart_name=chart_name,
                          template=template) # Pass the template

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please select at least one region to highlight from the sidebar.")
