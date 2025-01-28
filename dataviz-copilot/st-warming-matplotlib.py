# import libraries streamlit, pandas and matplotlib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np # Copilot forgot this

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
# add a column to df that is the difference between the average summer temperature over all 
# years and the actual summer temperature. Label it 'dSummer'.
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
col1, col2 = st.columns(2)

# In the first column, display the bar chart
with col1:
    fig, ax = plt.subplots()
    df['dSummer'].plot(kind='bar', ax=ax, color=df['dSummer'].apply(lambda x: 'red' if x > 0 else 'blue'))
    ax.set_title('Summer Temperature Anomaly')
    ax.set_ylabel('Temperature Anomaly (°C)')
    st.pyplot(fig)

    st.write(
        '''The bar chart above shows the temperature anomaly for the summer 
        months (June, July, August) at Heathrow Airport. The red bars indicate 
        years where the summer temperature was warmer than average, while the 
        blue bars indicate years where the summer temperature was cooler than 
        average.'''
    )

# In the second column, display the scatter chart
with col2:
    fig, ax = plt.subplots()
    ax.scatter(df.index, df['dSummer'], color='red')
    m, b = np.polyfit(df.index, df['dSummer'], 1)
    ax.plot(df.index, m*df.index + b, color='blue')
    ax.set_title('Summer Temperature Anomaly')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature Anomaly (°C)')
    st.pyplot(fig)

    st.write(
        '''The scatter chart above shows the temperature anomaly for the summer 
        months (June, July, August) at Heathrow Airport. The red dots represent 
        individual years, while the blue line represents the trendline of the data. 
        Years above the trendline experienced warmer than average summer temperatures, 
        while years below the trendline experienced cooler than average summer 
        temperatures.'''
    )
