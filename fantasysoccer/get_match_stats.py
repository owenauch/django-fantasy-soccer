# Random stuff to make standalone script work
import os, sys

proj_path = "fantasysoccer"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantasysoccer.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

###############################################

# the script
import requests, re, datetime, time
from api.models import *

def get_match_stats (date_string):
    print('Starting request for match stats...')

    schedule_url_front = 'https://api.sportradar.us/soccer-xt3/eu/en/schedules/'
    schedule_url_back = '/schedule.json?api_key=wen4p2gkyru39s2cxx3c5wae'
    league_ids = ['ENG','ESP','ITA','FRA','DEU']

    match_url_front = 'https://api.sportradar.us/soccer-xt3/eu/en/matches/'
    match_url_back = '/timeline.json?api_key=wen4p2gkyru39s2cxx3c5wae'

    # get match ids
    schedule_url = schedule_url_front + date_string + schedule_url_back
    schedule_response = requests.get(schedule_url)
    schedule_data = schedule_response.json()
    events = schedule_data['sport_events']
    match_ids = []
    for event in events:
        country_code = event['tournament']['category']['country_code']
        if country_code in league_ids:
            match_ids.append(event['id'])

    # get match stats for each player with match ids
    for id in match_ids:
        time.sleep(1)
        match_url = match_url_front + str(id) + match_url_back
        match_response = requests.get(match_url)
        match_data = match_response.json()
        if 'statistics' in match_data:
            teams = match_data['statistics']['teams']
            print('Stats for ' + match_data['sport_event']['competitors'][0]['name'] + " vs " + match_data['sport_event']['competitors'][1]['name'] + ':')
            for team in teams:
                players = team['players']
                for player in players:
                    # get id as int
                    id_string = player['id']
                    id_match = re.search(r'(\d+)$', id_string)
                    id = int(id_string[id_match.start():id_match.end()])

                    # find player record
                    p = Player.objects.get(pk=id)
                    print(p.name)

                    # if there's already a stat from this game, delete it
                    MatchStat.objects.filter(match_date=date_string, player_id=id).delete()

                    # if they're a goalie
                    shots_saved, shots_faced, penalties_saved, penalties_faced = 0, 0, 0, 0
                    if 'shots_faced_saved' in player:
                        shots_saved = player['shots_faced_saved']
                        shots_faced = player['shots_faced_total']
                        penalties_saved = player['penalties_saved']
                        penalties_faced = player['penalties_faced']

                    # check if they have full stats
                    if 'interceptions' in player:
                        stat = MatchStat(player=p, substituted_in=player['substituted_in'], substituted_out=player['substituted_out'],
                            goals=player['goals_scored'], assists=player['assists'], yellow_cards=player['yellow_cards'],
                            yellow_red_cards=player['yellow_red_cards'], red_cards=player['red_cards'],
                            interceptions=player['interceptions'], chances_created=player['chances_created'],
                            successful_crosses=player['crosses_successful'], crosses=player['crosses_total'],
                            successful_tackles=player['duels_tackle_successful'], tackles=player['duels_tackle_total'],
                            goals_conceded=player['goals_conceded'], shots_saved=shots_saved, shots_faced=shots_faced,
                            penalties_faced=penalties_faced, penalties_saved=penalties_saved,
                            fouls_committed=player['fouls_committed'], shots_on_goal=player['shots_on_goal'],
                            shots_off_goal=player['shots_off_goal'], shots_blocked=player['shots_blocked'],
                            minutes_played=player['minutes_played'], penalty_goals=player['goals_by_penalty'],
                            match_date=date_string)
                        stat.save()
                    else:
                        stat = MatchStat(player=p, substituted_in=player['substituted_in'], substituted_out=player['substituted_out'],
                            goals=player['goals_scored'], assists=player['assists'], yellow_cards=player['yellow_cards'],
                            yellow_red_cards=player['yellow_red_cards'], red_cards=player['red_cards'],
                            match_date=date_string)
                        stat.save()
            print('----------------------------------------------')

    print('Today\'s match stats successfully added to DB!')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        date_string = datetime.datetime.today().strftime('%Y-%m-%d')
    else:
        date_string = sys.argv[1]
    get_match_stats(date_string)
