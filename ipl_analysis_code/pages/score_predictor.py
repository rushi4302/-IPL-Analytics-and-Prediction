import streamlit as st
import pickle
import pandas as pd

# Load the saved model
pipe = pickle.load(open('pipe_score.pkl', 'rb'))

st.title('IPL Final Score Predictor 🏏')

# Data for dropdowns
teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Punjab Kings', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
]

cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Dubai', 'Navi Mumbai', 'Lucknow', 'Guwahati'
]

# Layout
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

selected_city = st.selectbox('Select Host City', sorted(cities))

col3, col4, col5 = st.columns(3)
with col3:
    current_score = st.number_input('Current Score', min_value=0)
with col4:
    overs = st.number_input('Overs Completed', min_value=5.0, max_value=19.9, step=0.1)
with col5:
    wickets = st.number_input('Wickets Out', min_value=0, max_value=9)

if st.button('Predict Final Score'):
    balls_left = 120 - int(overs * 6)

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'current_score': [current_score],
        'balls_left': [balls_left],
        'wickets_fallen': [wickets]
    })

    result = pipe.predict(input_df)
    st.success(f"Predicted Final Score: {int(result[0])}")
