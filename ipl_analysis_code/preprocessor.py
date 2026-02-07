import streamlit as st
import pandas as pd
import os

class IPLPreprocessor:
    def __init__(self):
        self.team_name_map = {
            'Delhi Daredevils': 'Delhi Capitals',
            'Rising Pune Supergiant': 'Rising Pune Supergiants',
            'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
            'Kings XI Punjab': 'Punjab Kings',
            'Deccan Chargers': 'Sunrisers Hyderabad',
            'Pune Warriors': 'Rising Pune Supergiants',
            'Gujarat Lions': 'Gujarat Titans'
        }
        self.base_dir = os.getcwd()

    @st.cache_data
    def load_data(_self):
        try:
            matches = pd.read_csv("matches.csv", low_memory=False)
            deliveries = pd.read_csv("deliveries.csv", low_memory=False)
        except FileNotFoundError:
            st.error("matches.csv or deliveries.csv not found")
            st.stop()
        return matches, deliveries

    def preprocess_all(self):
        matches, deliveries = self.load_data()

        # ✅ FIX: ID dtype mismatch (critical after appending 2025 data)
        matches["id"] = pd.to_numeric(matches["id"], errors="coerce")
        deliveries["match_id"] = pd.to_numeric(deliveries["match_id"], errors="coerce")

        # ✅ Standardize team names
        for col in ["team1", "team2", "winner", "toss_winner"]:
            if col in matches.columns:
                matches[col] = matches[col].replace(self.team_name_map)

        for col in ["batting_team", "bowling_team"]:
            if col in deliveries.columns:
                deliveries[col] = deliveries[col].replace(self.team_name_map)

        # ✅ Handle missing values safely
        matches["winner"] = matches["winner"].fillna("No Result")
        matches["date"] = pd.to_datetime(matches["date"], errors="coerce")

        for col in ["dismissal_kind", "player_dismissed", "fielder", "extras_type"]:
            if col in deliveries.columns:
                deliveries[col] = deliveries[col].fillna("None")

        # ✅ Force player columns to string (prevents mixed dtype crash)
        deliveries["batter"] = deliveries["batter"].astype(str)
        deliveries["bowler"] = deliveries["bowler"].astype(str)

        return matches, deliveries
