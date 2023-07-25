import streamlit as st
import plotly.express as px
from backend import get_data
import json

# Add title, text input, slider, selectbox, and subheader
st.title('Weather Forecast for the Next Days')
place = st.text_input('Place: ')
days = st.slider('Forecast Days', min_value=1, max_value=5, help='Select the numbers of forecasted days')
option = st.selectbox('Select data to view',
                      ('Temperature', 'Sky'))
st.subheader(f'{option} for the next {days} days in {place}')

# Get the temperature/sky data
if place:
    try:
        filtered_data = get_data(place, days)

        if option == 'Temperature':
            temperatures = [round(data['main']['temp'] / 10, 1) for data in filtered_data]
            dates = [data['dt_txt'] for data in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={'x': 'Date',
                                                              'y': 'Temperature (C)'})

            st.plotly_chart(figure)

        if option == 'Sky':
            images = {'Clear': 'images/clear.png', 'Clouds': 'images/cloud.png',
                      'Rain': 'images/rain.png', 'Snow': 'images/snow.png'}
            sky_conditions = [data['weather'][0]['main'] for data in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115)

    except KeyError:
        st.error('This city does not exist! Try again!')

