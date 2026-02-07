import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import base64

# Set Page Config

from preprocessor import IPLPreprocessor
from helper import get_match_list_formatted, generate_batting_card, generate_bowling_card, calculate_phase_stats , get_total_centuries

# ==========================================
# 0. HELPER FUNCTIONS
# ==========================================

@st.cache_data
def get_base64_of_bin_file(bin_file):
    """
    Reads a binary file and returns the base64 string.
    Cached to prevent reloading on every interaction.
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def add_video_background(video_path):
    """
    Injects a video background into the Streamlit app.
    """
    try:
        video_base64 = get_base64_of_bin_file(video_path)
        
        video_html = f"""
        <style>
        .stApp {{
            background: transparent !important;
        }}
        #video-background {{
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            z-index: -1;
            opacity: 0.8; /* Adjust opacity as needed */
            object-fit: cover;
        }}
        /* Optional: Dark overlay to make text readable */
        #video-overlay {{
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: -1;
        }}
        </style>
        <video id="video-background" autoplay loop muted playsinline>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        <div id="video-overlay"></div>
        """
        st.markdown(video_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading video: {e}")

# ==========================================
# 1. UI DASHBOARD SETUP
# ==========================================

# Custom CSS for Tables
st.markdown("""
<style>
    [data-testid="stDataFrame"] { font-family: sans-serif; }
    .stDataFrame table { background-color: rgba(30, 30, 30, 0.9) !important; color: #E0E0E0 !important; }
    .stDataFrame th { background-color: rgba(45, 45, 45, 0.9) !important; color: #AAAAAA !important; font-weight: normal !important; border-bottom: 1px solid #444 !important; }
    .stDataFrame td { border-bottom: 1px solid #333 !important; }
    .stDataFrame td:nth-child(2) { font-weight: 500; color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

st.title("🏏 IPL Analytics Hub")

prep = IPLPreprocessor()
matches, deliveries = prep.preprocess_all()

if matches is not None and deliveries is not None:

    # --- Sidebar Logic ---
    if os.path.exists("tataipl.jpg"):
        st.sidebar.image("tataipl.jpg", use_container_width=True)
    elif os.path.exists(os.path.join("images", "tataipl.jpg")):
        st.sidebar.image(os.path.join("images", "tataipl.jpg"), use_container_width=True)

    st.sidebar.title("Navigation")
    OPTIONS = ["Match Scorecard", "Player Analysis", "Team Analysis"]
    
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = OPTIONS[0]
        
    st.session_state.selected_option = st.sidebar.radio(
        "Go to", 
        OPTIONS, 
        index=OPTIONS.index(st.session_state.selected_option)
    )
    option = st.session_state.selected_option

    # ==========================================
    # OPTION 1: MATCH SCORECARD
    # ==========================================
    if option == "Match Scorecard":
        st.header("IPL Match Center")
        match_options = get_match_list_formatted(matches)
        
        if not match_options:
            st.warning("No match data available.")
        else:
            match_labels = [m[1] for m in match_options]
            selected_match_label = st.selectbox("Select Match:", match_labels)

            if selected_match_label:
                match_id = next(m[0] for m in match_options if m[1] == selected_match_label)
                match_df = matches[matches['id'] == match_id]

                if match_df.empty:
                    st.error("Match data not found for selected match.")
                    st.stop()

                match_data = match_df.iloc[0]

                t1 = match_data.get('team1', 'Team 1')
                t2 = match_data.get('team2', 'Team 2')
                winner = match_data.get('winner', 'No Result')
                venue = match_data.get('city', match_data.get('venue', 'Unknown Venue'))
                
                win_runs = match_data.get('win_by_runs', 0)
                win_wickets = match_data.get('win_by_wickets', 0)
                margin = f"{win_runs} runs" if win_runs > 0 else f"{win_wickets} wickets"

                st.markdown(f"### {t1} vs {t2}")
                st.caption(f"📍 Played at {venue} | 🏆 Winner: **{winner}** (Margin: {margin})")
                st.divider()

                toss_winner = match_data.get('toss_winner', t1)
                toss_decision = match_data.get('toss_decision', 'bat')
                
                if toss_decision == 'bat':
                    bat1_team = toss_winner
                    bat2_team = t2 if toss_winner == t1 else t1
                else:
                    bat2_team = toss_winner
                    bat1_team = t2 if toss_winner == t1 else t1

                tab1, tab2 = st.tabs([f"{bat1_team} Innings", f"{bat2_team} Innings"])

                with tab1:
                    bat_card, t_runs, t_wkts, t_extras, extras_dict, fow = generate_batting_card(match_id, 1, deliveries)
                    bowl_card = generate_bowling_card(match_id, 1, deliveries)
                    st.dataframe(bat_card, use_container_width=True, hide_index=True)
                    st.markdown(f"**Total:** {t_runs}/{t_wkts} (Extras: {t_extras})")
                    st.dataframe(bowl_card, use_container_width=True, hide_index=True)

                with tab2:
                    bat_card_2, t_runs_2, t_wkts_2, t_extras_2, extras_dict_2, fow_2 = generate_batting_card(match_id, 2, deliveries)
                    bowl_card_2 = generate_bowling_card(match_id, 2, deliveries)
                    st.dataframe(bat_card_2, use_container_width=True, hide_index=True)
                    st.markdown(f"**Total:** {t_runs_2}/{t_wkts_2} (Extras: {t_extras_2})")
                    st.dataframe(bowl_card_2, use_container_width=True, hide_index=True)

    # ==========================================
    # OPTION 2: PLAYER ANALYSIS
    # ==========================================
    elif option == "Player Analysis":
        st.header("Player Intelligence Center")
        all_players = sorted(list(set(deliveries['batter'].unique()) | set(deliveries['bowler'].unique())))
        selected_player = st.sidebar.selectbox("Search Player Name", all_players)
        centuries_df = get_total_centuries(deliveries)
        player_centuries = centuries_df.get(selected_player, 0)
        if selected_player:
            st.divider()
            col_img, col_stats = st.columns([1, 3])
            
            with col_img:
                png_path = os.path.join(prep.base_dir, "images", f"{selected_player}.png")
                jpg_path = os.path.join(prep.base_dir, "images", f"{selected_player}.jpg")
                default_path = os.path.join(prep.base_dir, "images", "default.png")
                
                if os.path.exists(png_path): 
                    st.image(png_path, caption=selected_player, use_container_width=True)
                elif os.path.exists(jpg_path): 
                    st.image(jpg_path, caption=selected_player, use_container_width=True)
                elif os.path.exists(default_path): 
                    st.image(default_path, caption=selected_player, use_container_width=True)
                else: 
                    st.image("https://cdn-icons-png.flaticon.com/512/166/166344.png", caption=selected_player, width=150)

            with col_stats:
                player_bat = deliveries[deliveries['batter'] == selected_player]
                runs = player_bat['batsman_runs'].sum()
                balls = len(player_bat)
                sr = round(runs/balls*100, 2) if balls > 0 else 0
                
                player_bowl = deliveries[deliveries['bowler'] == selected_player]
                wickets = len(player_bowl[player_bowl['is_wicket']==1])
                runs_conceded = player_bowl['total_runs'].sum()
                eco = round(runs_conceded / (len(player_bowl)/6), 2) if len(player_bowl) > 0 else 0

                c1, c2, c3, c4 ,c5= st.columns(5)
                c1.metric("Runs", runs)
                c2.metric("Strike Rate", sr)
                c3.metric("Centuries", player_centuries)  
                c4.metric("Wickets", wickets)
                c5.metric("Economy", eco)

            st.divider()
            tab1, tab2, tab3  = st.tabs(["📊 Performance Phases", "☠️ Weakness Analysis", "🆚 Opponent Analysis"])
            
            with tab1:
                st.subheader("Batting Impact by Phase")
                phase_data = calculate_phase_stats(selected_player, deliveries)
                if not phase_data.empty:
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        fig_runs = px.bar(phase_data, x='phase', y='batsman_runs', title="Runs Scored by Phase", color='batsman_runs', color_continuous_scale='Viridis')
                        st.plotly_chart(fig_runs, use_container_width=True)
                    with col_p2:
                        fig_sr = px.bar(phase_data, x='phase', y='Strike Rate', title="Strike Rate Aggression", text='Strike Rate', color='Strike Rate', color_continuous_scale='Magma')
                        st.plotly_chart(fig_sr, use_container_width=True)
                else: 
                    st.info("No detailed phase data available.")

            with tab2:
                st.subheader("How do they get out?")
                if not player_bat.empty:
                    dismissals = player_bat[player_bat['player_dismissed'] == selected_player]
                    dismissal_counts = dismissals['dismissal_kind'].value_counts().reset_index()
                    dismissal_counts.columns = ['Type', 'Count']
                    if not dismissal_counts.empty:
                        fig_d = px.pie(dismissal_counts, values='Count', names='Type', title="Dismissal Distribution", hole=0.4)
                        st.plotly_chart(fig_d, use_container_width=True)
                    else: 
                        st.info("Player has never been dismissed!")
                else: 
                    st.info("No batting data.")


            with tab3:
                st.subheader("Favorite Opponents")
                if not player_bat.empty:
                    runs_vs_team = player_bat.groupby('bowling_team')['batsman_runs'].sum().reset_index()
                    runs_vs_team = runs_vs_team.sort_values('batsman_runs', ascending=False).head(10)
                    fig_opp = px.bar(runs_vs_team, x='batsman_runs', y='bowling_team', orientation='h', title="Most Runs Against...", color='batsman_runs')
                    st.plotly_chart(fig_opp, use_container_width=True)

           


    # ==========================================
    # OPTION 3: TEAM ANALYSIS
    # ==========================================
    elif option == "Team Analysis":
        st.header("Team Analytics Hub")
        
        tab_main, tab_profile = st.tabs(["🏆 League Overview", "📊 Team Profile"])
        
        with tab_main:
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.subheader("Trophy Cabinet")
                if 'season' in matches.columns:
                    matches_sorted = matches.sort_values(['season', 'date'])
                    season_winners = matches_sorted.drop_duplicates(subset=['season'], keep='last')[['season', 'winner']]
                    winners_count = season_winners['winner'].value_counts().reset_index()
                    winners_count.columns = ['Team', 'Trophies']
                    fig = px.bar(winners_count, x='Team', y='Trophies', color='Trophies', color_continuous_scale='oranges')
                    st.plotly_chart(fig, use_container_width=True)
            with col_t2:
                st.subheader("Total Match Wins")
                total_wins = matches['winner'].value_counts().reset_index()
                total_wins.columns = ['Team', 'Wins']
                total_wins = total_wins[total_wins['Team'] != 'No Result']
                fig2 = px.bar(total_wins, x='Wins', y='Team', orientation='h', color='Wins')
                st.plotly_chart(fig2, use_container_width=True)

        with tab_profile:
            all_teams = sorted(matches['team1'].unique())
            selected_team = st.selectbox("Select Team:", all_teams)
            
            # --- VIDEO BACKGROUND LOGIC ---
            # Using partial matching ("Royal Challengers") to catch variations like "RCB" or "Royal Challengers Bangalore"
            if selected_team and "Royal Challengers" in selected_team:
                video_file = "rcb.mp4"
                video_full_path = os.path.join("videos", "rcb.mp4")
                
                if os.path.exists(video_file):
                    add_video_background(video_file)
                elif os.path.exists(video_full_path):
                    add_video_background(video_full_path)
            
            if selected_team:
                st.divider()
                st.subheader(f"Stats for {selected_team}")
                
                titles = 0
                if 'season' in matches.columns:
                    season_winners = matches.sort_values(['season', 'date']).drop_duplicates(subset=['season'], keep='last')
                    titles = len(season_winners[season_winners['winner'] == selected_team])
                
                matches_played = len(matches[(matches['team1'] == selected_team) | (matches['team2'] == selected_team)])
                matches_won = len(matches[matches['winner'] == selected_team])
                win_percentage = round((matches_won / matches_played * 100), 2) if matches_played > 0 else 0
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Titles Won", titles, "🏆")
                m2.metric("Matches Played", matches_played)
                m3.metric("Matches Won", matches_won)
                m4.metric("Win Percentage", f"{win_percentage}%")

else:
    st.error("Data not loaded. Please check your CSV path.")




    