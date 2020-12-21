from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

from datetime import datetime, timezone
import json
import time

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def make_output_str(game):
    local_start = utc_to_local(game["start_time"])
    pbp = client.play_by_play(home_team=game["home_team"],
                              year=local_start.year,
                              month=local_start.month,
                              day=local_start.day)
    # attach the game info so we can easily look up the winner while parsing
    full_game = {"game_info": game, "play_by_play": pbp}
    return json.dumps(full_game, default=str)

for year in range(1998, 2021):
    try:
        schedule = client.season_schedule(season_end_year=year)
    except:
        continue
    with open('play_by_plays/' + str(year) + '.json', 'w') as pbp_file:
        for game in schedule:
            time.sleep(3) # respect the crawl rate in bball reference's robots.txt page
            try:
                pbp_file.write(make_output_str(game) + '\n')
            except:
                print("error:")
                print(game)
                print()
