import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go

# Set Page Config
st.set_page_config(page_title="IPL Predictor | Analytics Pro", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Load the saved assets
pipe = pickle.load(open('pipe.pkl', 'rb'))
teams = pickle.load(open('teams.pkl', 'rb'))
cities = pickle.load(open('cities.pkl', 'rb'))

st.title('🎯 IPL Win Probability Predictor')
st.markdown("---")

# Layout: Team Selection
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select Batting Team (Chasing)', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(teams), index=1)

selected_city = st.selectbox('Select Host City', sorted(cities))
target = st.number_input('Target Score', min_value=1, max_value=300, value=180)

# Layout: Game Progress
col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Current Score', min_value=0, max_value=target+10, value=100)
with col4:
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=20.0, step=0.1, value=10.0)
with col5:
    wickets = st.number_input('Wickets Out', min_value=0, max_value=10, value=3)

if st.button('Predict Win Probability', use_container_width=True):
    # Feature Engineering
    runs_left = target - score
    balls_left = 120 - int(overs * 6)
    wickets_remaining = 10 - wickets
    
    # 1. Logic Checks
    if score >= target:
        st.success(f"🏆 Match Over! {batting_team} won the match.")
    elif wickets >= 10 or (balls_left <= 0 and score < target):
        st.error(f"❌ Match Over! {bowling_team} won the match.")
    else:
        # Calculate Rates
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        # Stats Row
        st.markdown("### Match Live Analytics")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Runs Required", runs_left)
        m_col2.metric("Balls Left", balls_left)
        m_col3.metric("Current RR (CRR)", round(crr, 2))
        m_col4.metric("Required RR (RRR)", round(rrr, 2), delta=round(rrr-crr, 2), delta_color="inverse")

        # Create input dataframe
        input_df = pd.DataFrame({
            'batting_team': [batting_team], 'bowling_team': [bowling_team],
            'city': [selected_city], 'runs_left': [runs_left],
            'balls_left': [balls_left], 'wickets': [wickets_remaining],
            'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]
        })

        # Model Prediction
        pipe.named_steps[list(pipe.named_steps.keys())[-1]].multi_class = 'auto'
        result = pipe.predict_proba(input_df)
        win = result[0][1]
        loss = result[0][0]

        # Visualization
        st.markdown("---")
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.subheader("Win Probability Chart")
            # Create a simple Donut Chart
            fig = go.Figure(data=[go.Pie(labels=[batting_team, bowling_team], 
                             values=[win, loss], hole=.6,
                             marker_colors=['#38bdf8', '#ef4444'])])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300, 
                             showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig.add_annotation(text=f"{round(win*100)}%", x=0.5, y=0.5, font_size=40, showarrow=False, font_color="white")
            st.plotly_chart(fig, use_container_width=True)

        with res_col2:
            st.subheader("Probability Details")
            st.write(f"**{batting_team}**: {round(win * 100, 1)}%")
            st.progress(win)
            st.write(f"**{bowling_team}**: {round(loss * 100, 1)}%")
            st.progress(loss)

            st.info(f"The model predicts a high chance of victory for **{batting_team if win > loss else bowling_team}** based on current momentum.")

            