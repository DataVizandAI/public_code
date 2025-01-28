# add a slider to the user interface to select a beginnining and end year and plot the results for those years only

# import libraries streamlit, pandas and plotly express
import streamlit as st
import pandas as pd
import plotly.express as px

# Set display to wide
st.set_page_config(layout='wide')

# A function to read a csv file and return a dataframe
# The function takes a file path as an argument and the result is cached
# Only the columns 'Year', 'Month' and 'Tmean' are required
@st.cache_data
def read_csv(file_path):
    return pd.read_csv(file_path, usecols=['Year', 'Month', 'Tmean'])

# Read 'Heathrow.csv' as a dataframe
df = read_csv('Heathrow.csv')

# Create a new dataframe from df where the columns are months and the year are the rows
df = df.pivot(index='Year', columns='Month', values='Tmean')

# add a column to df that it the average temperature of month columns labelled 6, 7, and 8. 
# Label it 'Summer'.
df['Summer'] = df[[6, 7, 8]].mean(axis=1)
# add a column to df that is the dfference between the average summer temperature over all 
# years and the actual summer temparature. Label it 'dSummer'.
df['dSummer'] = df['Summer'] - df['Summer'].mean()

# Create a title for the app and two columns below it
st.header('Heathrow Summer Temperature Anomaly Analysis')
st.subheader('How is Global Warming affecting the local weather?')

st.write(
    '''This application attempts to demonstrate the local effect of global warming 
    by analyzing the summer temperature anomalies at Heathrow Airport. The data is 
    sourced from historical temperature records, focusing on the summer months 
    (June, July, August). The temperature anomaly is calculated as the difference 
    between the average summer temperature over all years and the actual summer 
    temperature for each year. The visualizations below help to understand the 
    trends and variations in summer temperatures over the years, providing insights 
    into the impact of global warming at a local level.'''
)

# Add a slider to select the beginning and end year
min_year = int(df.index.min())
max_year = int(df.index.max())
start_year, end_year = st.slider('Select the year range', min_year, max_year, (min_year, max_year))

# Filter the dataframe based on the selected year range
filtered_df = df.loc[start_year:end_year]

# plot a bar chart of the dSummer temperature over the selected years
summer_fig = px.bar(filtered_df, x=filtered_df.index, y='dSummer', title='Summer Temperature Anomaly')
summer_fig.update_layout(yaxis_title='Temperature Anomaly (°C)')
summer_fig.update_traces(marker_color=filtered_df['dSummer'].apply(lambda x: 'red' if x > 0 else 'blue'))

# plot a scatter chart with trendline of the dSummer temperature over the selected years.
scatter_fig = px.scatter(filtered_df, x=filtered_df.index, y='dSummer', trendline='ols', title='Summer Temperature Anomaly')
scatter_fig.update_layout(xaxis_title='Summer Temperature (°C)', yaxis_title='Temperature Anomaly (°C)')
scatter_fig.update_traces(marker_color='red')
scatter_fig.data[1].line.color = 'blue'  # Change the trendline color to blue

col1, col2 = st.columns(2)

# In the first column, display the bar chart
with col1:
    st.plotly_chart(summer_fig)

    st.write(
        '''The bar chart above shows the temperature anomaly for the summer 
        months (June, July, August) at Heathrow Airport. The red bars indicate 
        years where the summer temperature was warmer than average, while the 
        blue bars indicate years where the summer temperature was cooler than 
        average.'''
    )

# In the second column, display the scatter chart
with col2:
    st.plotly_chart(scatter_fig)

    st.write(
        '''The scatter chart above shows the temperature anomaly for the summer 
        months (June, July, August) at Heathrow Airport. The red dots represent 
        individual years, while the blue line represents the trendline of the data. 
        Years above the trendline experienced warmer than average summer temperatures, 
        while years below the trendline experienced cooler than average summer 
        temperatures.'''
    )
