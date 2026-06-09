import pandas as pd
import re

def get_match_list(bkfc_file):
    """Scans the BKFC file and returns a list of all match row pairs found."""
    bkfc_df = pd.read_excel(bkfc_file, header=None, engine="openpyxl")
    matches = []
    
    # Iterate through match pairs starting at row index 3, skipping by pairs (2)
    for i in range(3, len(bkfc_df), 2):
        if i + 1 >= len(bkfc_df):
            break
        row = bkfc_df.iloc[i]
        # Skip empty placeholder rows
        if pd.isna(row[0]) or pd.isna(row[1]):
            continue
            
        match_date = str(row[0]).split(" ")[0]  # Keep date string clean
        match_title = str(row[1])
        
        matches.append({
            "index": i,
            "label": f"{match_date} | {match_title}"
        })
    return matches

def load_match_data(bkfc_file, opponent_file, match_row_idx=None):
    bkfc_df = pd.read_excel(bkfc_file, header=None, engine="openpyxl")
    opp_df = pd.read_excel(opponent_file, header=None, engine="openpyxl")

    bkfc_season_avg = bkfc_df.iloc[1]
    all_opp_avg = bkfc_df.iloc[2]

    # Auto-detect: If no index is explicitly selected, fall back to the newest row pair
    if match_row_idx is None:
        valid_indices = []
        for i in range(3, len(bkfc_df), 2):
            if i + 1 < len(bkfc_df) and pd.notna(bkfc_df.iloc[i][0]) and pd.notna(bkfc_df.iloc[i][1]):
                valid_indices.append(i)
        match_row_idx = valid_indices[-1] if valid_indices else 3

    # Dynamically extract the specific pair of rows for the targeted match
    match_bkfc = bkfc_df.iloc[match_row_idx]
    match_opp = bkfc_df.iloc[match_row_idx + 1]

    opp_season_avg = opp_df.iloc[1]

    match_title = str(match_bkfc[1])
    competition = str(match_bkfc[2])
    match_date = str(match_bkfc[0])

    score = ""
    m = re.search(r"\d+:\d+", match_title)
    if m:
        score = m.group()

    opponent_name = (
        match_title.split("-")[-1]
        .replace(score, "")
        .strip()
    )

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
