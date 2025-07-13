import pandas as pd
import numpy as np

# Fantasy teams and their HR Derby players with betting odds
fantasy_teams = [
    ["Jonothina Janawitza", "Junior Caminero (+1000)", "Cal Raleigh (+250)", "Oneil Cruz (+300)"],
    ["Brad", "James Wood (+450)", "Cal Raleigh (+250)", "Byron Buxton (+850)"],
    ["Kevin \"GOAT\" Brown", "Byron Buxton (+850)", "James Wood (+450)", "Oneil Cruz (+300)"],
    ["Star Football Player Wes", "Cal Raleigh (+250)", "Matt \"GOATA\" Olson (+700)", "Brent Rooker (+850)"],
    ["Adam \"Pussy\" Sturisky", "Jazz Chisholm Jr. (+1200)", "Cal Raleigh (+250)", "Junior Caminero (+1000)"],
]

# Home run stats for 2025
home_run_stats = {
    "Cal Raleigh": 38,
    "Oneil Cruz": 18,
    "James Wood": 24,
    "Matt \"GOATA\" Olson": 17,
    "Brent Rooker": 19,
    "Byron Buxton": 21,
    "Junior Caminero": 23,
    "Jazz Chisholm Jr.": 18
}

# Convert American odds to implied probability
def american_to_probability(odds_str):
    odds = int(odds_str.strip('()+'))
    if '+' in odds_str:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)

# Extract player name and odds from formatted string
def extract_name_and_odds(player_field):
    name, odds = player_field.rsplit('(', 1)
    return name.strip(), odds.strip(')+')

# Process teams and build final table
processed_data = []

for team in fantasy_teams:
    manager, p1_raw, p2_raw, p3_raw = team
    players_raw = [p1_raw, p2_raw, p3_raw]
    players = []
    probs = []
    total_hrs = 0

    for raw in players_raw:
        name, odds = extract_name_and_odds(raw)
        full_label = f"{name} (+{odds}) | HR: {home_run_stats[name]}"
        players.append(full_label)
        probs.append(american_to_probability(f"+{odds}"))
        total_hrs += home_run_stats[name]

    avg_prob = round(np.mean(probs) * 100, 2)
    processed_data.append([manager, players[0], players[1], players[2], avg_prob, total_hrs])

# Create DataFrame
df_output = pd.DataFrame(processed_data, columns=[
    "Fantasy Player", "HR Player 1", "HR Player 2", "HR Player 3",
    "Team Implied Strength (%)", "Team Total HRs"
])

# Sort by team strength
df_output = df_output.sort_values(by="Team Implied Strength (%)", ascending=False).reset_index(drop=True)

import ace_tools as tools; tools.display_dataframe_to_user(name="Final Fantasy Teams with Stats", dataframe=df_output)
