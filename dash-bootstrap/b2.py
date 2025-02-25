
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("data/co2_total.csv") 
marks={ int(i): str(i) for i in df.Year.unique() if i%50==0}

min_year = df.Year.min()
max_year = df.Year.max()
mid_year = (max_year+min_year)//2

DEFAULT_CLASS = 'border border-primary rounded p-2 bg-light m-2'

app.layout = dbc.Container(
    [
        html.H1('Dash App with Bootstrap components - CO2 emissions', className=f"{DEFAULT_CLASS} text-center text-dark bg-dark-subtle"),
        
            dbc.Row([
                html.Div('Global CO2 Emissions', className='h3 text-danger'),
                html.Div("Move the slider to display the CO2 emissions by country for a specific year", className='text-secondary'),
                dcc.Slider(min=min_year, max=max_year, value=mid_year, step=1, marks=marks, id='slider-value'),
                dcc.Graph(id='graph2-content'),
                dcc.Markdown("""The data used in this article is derived from Our World in Data. 
                                OWD publishes articles and data about the most pressing problems that the world faces. 
                                All its content is open source and its data is downloadable 
                                — see [Our World in Data](https://ourworldindata.org/) for details.
                            """, className='text-secondary')
                ],
                className='border border-primary rounded p-2 bg-light m-2'
            ),
    ], className=f"{DEFAULT_CLASS} container-fluid"
)

@callback(
    Output('graph2-content', 'figure'),
    Input('slider-value', 'value')
)
def update_graph(value):
    col = 'Annual CO₂ emissions'# the column that contains the emissions data
    max = df[col].max()         # maximum emissions value for color range
    min = df[col].min() 
        
    fig = px.choropleth(df[df['Year']==value], 
        locations="Code",       # The ISO code for the Entity (country)
        color=col,              # color is set by this column
        hover_name="Entity",    # hover name is the name of the Entity (country)
        range_color=(min,max),  # the range of values as set above
        scope= 'world',         # a world map - the default
        projection='equirectangular', 
        title=f"CO2 Emissions by country in {value}",
        color_continuous_scale=px.colors.sequential.Reds
        )
    fig.update_layout(
        margin=dict(l=0, r=0, t=60, b=0),
        coloraxis_colorbar=dict(
        title="Tonnes",),
        )
    return fig

if __name__ == '__main__':
    app.run(debug=True, jupyter_mode='jupyterlab')
