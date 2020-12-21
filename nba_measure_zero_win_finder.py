import json

def check_wire_to_wire(game):
    first_winning_team = ""
    for play in game:

        if play["away_score"] > play["home_score"]:
            first_winning_team = "away"
            break
        if play["away_score"] < play["home_score"]:
            first_winning_team = "home"
            break

    for play in game:
        # perfectly modeling measure zero wins was a bit tricky, so I am doing this
        # to get a set of possible measure zero wins that I verify manually.
        # This process also allows me to review some very cool games that weren't
        # quite measure 0
        if play["period"] == 4 and play["remaining_seconds_in_period"] < 5.0:
            break

        if play["away_score"] > play["home_score"]:
            if first_winning_team == "home":
                return None
        if play["away_score"] < play["home_score"]:
            if first_winning_team == "away":
                return None

    return first_winning_team


for year in range(1998, 2021):
    with open('play_by_plays/' + str(year) + '.json') as pbp_file:
        while True:
            game_line = pbp_file.readline()
            if not game_line:
                break

            game = json.loads(game_line)
            try:
                pbp = game["play_by_play"]
            except:
                continue
            res = check_wire_to_wire(pbp)
            if res is None:
                continue

            #if pbp[-1]["period"] != 4:
            #    continue

            if res == "away":
                if game["game_info"]["home_team_score"] > game["game_info"]["away_team_score"]:
                    print(game["game_info"])

            if res == "home":
                if game["game_info"]["home_team_score"] < game["game_info"]["away_team_score"]:
                    print(game["game_info"])
