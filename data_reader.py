import pandas as pd
import re

# Comprehensive metrics mapping transferred from advanced telemetry definitions
STATS = [
    {"label": "Goals", "col": 6},
    {"label": "xG (Expected Goals)", "col": 7},
    {"label": "Shots", "col": 8},
    {"label": "Shots on Target", "col": 9},
    {"label": "Shot Accuracy %", "col": 10},
    {"label": "Possession %", "col": 14},
    {"label": "Passes", "col": 11},
    {"label": "Pass Accuracy %", "col": 13},
    {"label": "Positional Attacks", "col": 29},
    {"label": "Positional Attacks w/ Shots", "col": 30},
    {"label": "Counterattacks", "col": 32},
    {"label": "Corners", "col": 38},
    {"label": "Set Pieces w/ Shots", "col": 36},
    {"label": "Duels Won %", "col": 25},
    {"label": "Crosses", "col": 47},
    {"label": "Cross Accuracy %", "col": 49},
    {"label": "Touches in Penalty Area", "col": 55},
    {"label": "Offensive Duels Won %", "col": 58},
    {"label": "Defensive Duels Won %", "col": 66},
    {"label": "Aerial Duels Won %", "col": 69},
    {"label": "Interceptions", "col": 73},
    {"label": "Clearances", "col": 74},
    {"label": "Fouls", "col": 75},
    {"label": "Yellow Cards", "col": 76},
    {"label": "Shots Against", "col": 61},
    {"label": "PPDA", "col": 108},
]

def load_match_data(bkfc_file, opponent_file):
    bkfc_df = pd.read_excel(bkfc_file, header=None, engine="openpyxl")
    opp_df = pd.read_excel(opponent_file, header=None, engine="openpyxl")

    bkfc_season_avg = bkfc_df.iloc[1]
    all_opp_avg = bkfc_df.iloc[2]
    match_bkfc = bkfc_df.iloc[3]
    match_opp = bkfc_df.iloc[4]
    opp_season_avg = opp_df.iloc[1]

    match_title = str(match_bkfc[1])
    competition = str(match_bkfc[2])
    match_date = str(match_bkfc[0])

    score = ""
    m = re.search(r"\d+:\d+", match_title)
    if m:
        score = m.group()

    opponent_name = match_title.split("-")[-1].replace(score, "").strip()

    return {
        "match_title": match_title,
        "match_date": match_date,
        "competition": competition,
        "score": score,
        "opponent_name": opponent_name,
        "bkfc_season_avg": bkfc_season_avg,
        "all_opp_avg": all_opp_avg,
        "match_bkfc": match_bkfc,
        "match_opp": match_opp,
        "opp_season_avg": opp_season_avg
    }