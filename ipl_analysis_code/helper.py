import pandas as pd
import numpy as np

# ================= MATCH LIST =================
def get_match_list_formatted(matches):
    matches = matches.dropna(subset=["date"]).sort_values("date", ascending=False)

    output = []
    for _, row in matches.iterrows():
        label = f"{row['date'].strftime('%Y-%m-%d')}: {row['team1']} vs {row['team2']} (Winner: {row['winner']})"
        output.append((row["id"], label))

    return output

# ================= DISMISSAL TEXT =================
def get_dismissal_text(row):
    kind = row.get("dismissal_kind", "None")
    bowler = row.get("bowler", "Unknown")
    fielder = row.get("fielder", "Unknown")

    if kind == "caught":
        return f"c {fielder} b {bowler}"
    if kind == "bowled":
        return f"b {bowler}"
    if kind == "lbw":
        return f"lbw b {bowler}"
    if kind in ["run out", "stumped"]:
        return f"{kind} ({fielder})"
    if kind == "caught and bowled":
        return f"c&b {bowler}"
    return kind

def safe_sum(df, col):
    return df[col].sum() if col in df.columns else 0

# ================= BATTING CARD =================
def generate_batting_card(match_id, inning, deliveries):
    df = deliveries[(deliveries["match_id"] == match_id) & (deliveries["inning"] == inning)]

    if df.empty:
        return pd.DataFrame(), 0, 0, 0, {}, []

    bat = df.groupby("batter").agg(
        R=("batsman_runs", "sum"),
        B=("ball", "count")
    ).reset_index()

    bat["4s"] = df[df["batsman_runs"] == 4].groupby("batter").size()
    bat["6s"] = df[df["batsman_runs"] == 6].groupby("batter").size()
    bat = bat.fillna(0)
    bat["S/R"] = (bat["R"] / bat["B"] * 100).round(2)

    wk = df[df["player_dismissed"] != "None"]
    if not wk.empty:
        wk["Dismissal"] = wk.apply(get_dismissal_text, axis=1)
        bat = bat.merge(
            wk[["player_dismissed", "Dismissal"]],
            left_on="batter",
            right_on="player_dismissed",
            how="left"
        )

    bat["Dismissal"] = bat["Dismissal"].fillna("not out")
    bat = bat[["batter", "Dismissal", "R", "B", "4s", "6s", "S/R"]]
    bat.columns = ["Batter", "Dismissal", "R", "B", "4s", "6s", "S/R"]

    extras = {
        "Wides": safe_sum(df, "wide_runs"),
        "No Balls": safe_sum(df, "noball_runs"),
        "Byes": safe_sum(df, "bye_runs"),
        "Leg Byes": safe_sum(df, "legbye_runs"),
        "Penalty": safe_sum(df, "penalty_runs"),
    }

    fow, score, w = [], 0, 0
    for _, r in df.iterrows():
        score += r["total_runs"]
        if r["player_dismissed"] != "None":
            w += 1
            fow.append(f"{score}-{w} ({r['player_dismissed']})")

    return bat, score, w, sum(extras.values()), extras, fow

# ================= BOWLING CARD =================
def generate_bowling_card(match_id, inning, deliveries):
    df = deliveries[(deliveries["match_id"] == match_id) & (deliveries["inning"] == inning)]

    if df.empty:
        return pd.DataFrame()

    bowl = df.groupby("bowler").agg(
        R=("total_runs", "sum"),
        Balls=("ball", "count"),
        W=("is_wicket", "sum")
    ).reset_index()

    bowl["Overs"] = (bowl["Balls"] // 6) + (bowl["Balls"] % 6) / 10
    bowl["Econ"] = (bowl["R"] / bowl["Overs"]).replace([np.inf, -np.inf], 0).round(2)

    bowl = bowl[["bowler", "Overs", "R", "W", "Econ"]]
    bowl.columns = ["Bowler", "O", "R", "W", "Econ"]

    return bowl

# ================= PHASE STATS =================
def calculate_phase_stats(player, deliveries):
    df = deliveries[deliveries["batter"] == player].copy()

    def phase(over):
        if over < 6:
            return "Powerplay (1-6)"
        elif over < 16:
            return "Middle (7-15)"
        return "Death (16-20)"

    df["phase"] = df["over"].apply(phase)

    out = df.groupby("phase").agg(
        batsman_runs=("batsman_runs", "sum"),
        balls=("ball", "count")
    ).reset_index()

    out["Strike Rate"] = (out["batsman_runs"] / out["balls"] * 100).round(2)
    return out

def get_total_centuries(deliveries_df):
    """
    Returns a Series with total centuries (100+ runs in a match)
    for each batter.
    """

    # 1️⃣ Calculate runs per batter per match
    runs_per_match = (
        deliveries_df
        .groupby(['match_id', 'batter'])['batsman_runs']
        .sum()
        .reset_index()
    )

    # 2️⃣ Filter centuries (100+ runs in a match)
    centuries = runs_per_match[runs_per_match['batsman_runs'] >= 100]

    # 3️⃣ Count centuries per batter
    century_count = (
        centuries
        .groupby('batter')
        .size()
        .sort_values(ascending=False)
    )

    return century_count
