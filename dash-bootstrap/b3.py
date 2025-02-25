from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Initialize the Dash app with Bootstrap stylesheet
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define a default CSS class for styling
DEFAULT_CLASS = 'border border-primary rounded p-2 bg-light m-2'

# Load the CO2 emissions data from a CSV file
df = pd.read_csv("data/co2_total.csv") 

# Define the layout of the app
app.layout = dbc.Container(
    [
        # Title of the app
        html.H1('Dash App with Bootstrap components - CO2 Emissions', className=f"{DEFAULT_CLASS} text-center text-dark bg-dark-subtle"),
    
        # Row containing the dropdown and graph
        dbc.Row([
            # Subtitle
            html.Div('Total CO2 Emissions', className='h3 text-danger'),
            # Instruction text
            html.Div("Choose a country to display the CO2 emissions over time", className='text-secondary'),
            # Dropdown for selecting a country
            dcc.Dropdown(df.Entity.unique(), 'Canada', id='dropdown-selection'),
            # Graph to display the CO2 emissions
            dcc.Graph(id='graph-content'),
            dcc.Markdown("""The data used in this article is derived from Our World in Data. 
                            OWD publishes articles and data about the most pressing problems that the world faces. 
                            All its content is open source and its data is downloadable 
                            — see [Our World in Data](https://ourworldindata.org/) for details.
                        """, className='text-secondary')

            ],
            className='border border-primary rounded p-2 bg-light m-2'
        )
    ], className=f"{DEFAULT_CLASS} container-fluid"
)

# Callback to update the graph based on the selected country
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    # Filter the dataframe based on the selected country
    dff = df[df.Entity==value]
    # Create a bar chart of CO2 emissions over time
    return px.bar(dff, x='Year', y='Annual CO₂ emissions', template='plotly_white')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

