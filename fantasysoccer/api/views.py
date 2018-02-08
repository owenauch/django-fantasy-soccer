from api.models import *
from api.serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime

# takes in a roster and a matchweek, and returns a scored roster
# with stats for each player in the roster
def generate_scored_roster(roster, matchweek):
    positions = ['gk', 'gk_sub',
    'd_one', 'd_two', 'd_three', 'd_four', 'd_sub',
    'm_one', 'm_two', 'm_three', 'm_sub',
    'f_one', 'f_two', 'f_three', 'f_sub']
    stats = ['minutes_played', 'goals', 'assists', 'penalty_goals',
    'shots_on_goal', 'shots_off_goal', 'crosses', 'successful_tackles',
    'yellow_cards', 'yellow_red_cards', 'red_cards',
    'shots_saved', 'goals_conceded']
    scored_players = []

    # loop through D players, resolve mutiples and score them
    for i, position in enumerate(positions):
        match_stats = MatchStat.objects.filter(player_id=getattr(roster, position),
        match_date__range=(matchweek.start_date, matchweek.end_date))
        player_stats = {
            'minutes_played': 0,
            'goals': 0,
            'assists': 0,
            'penalty_goals': 0,
            'shots_on_goal': 0,
            'shots_off_goal': 0,
            'crosses': 0,
            'successful_tackles': 0,
            'yellow_cards': 0,
            'yellow_red_cards': 0,
            'red_cards': 0,
            'shots_saved': 0,
            'goals_conceded': 0
        }

        # add to stats if there's only one
        if (len(match_stats) == 1):
            for stat in stats:
                new_stat = getattr(match_stats[0], stat)
                player_stats[stat] = new_stat
        # if there are multiple, loop through and add them together
        else:
            for idx, match_stat in enumerate(match_stats):
                for stat in stats:
                    if (idx == 0):
                        new_stat = getattr(match_stats[0], stat)
                        player_stats[stat] = new_stat
                    else:
                        new_value = getattr(match_stats[idx], stat) + player_stats[stat]
                        player_stats[stat] = new_value

        # get player name and team
        player = getattr(roster, position)
        player_stats['name'] = player.name
        team = Team.objects.get(pk=player.team_id)
        player_stats['team'] = team.name

        # append to list
        scored_players.append(player_stats)

    # calculate points for each player
    # first goalies and defenders
    for idx, position in enumerate(positions[:7]):
        player = scored_players[idx]
        points = player['goals'] * 8
        points += player['penalty_goals'] * -4
        points += player['assists'] * 4
        points += player['shots_off_goal'] * .8
        points += player['shots_on_goal']
        points += player['successful_tackles'] * 2
        points += player['shots_saved'] * 2
        points -= player['yellow_cards']
        points -= player['yellow_red_cards']
        points -= player['red_cards'] * 3
        if (player['minutes_played'] != 0 and player['goals_conceded'] == 0):
            points += 4
        if (player['minutes_played'] > 60):
            points += 1
        if (player['minutes_played'] >= 90):
            points += 1
        scored_players[idx]['points'] = points

    # then, attacking players
    for idx, position in enumerate(positions[-8:]):
        idx = idx + 7
        player = scored_players[idx]
        points = player['goals'] * 6
        points += player['penalty_goals'] * -2
        points += player['assists'] * 3
        points += player['shots_off_goal'] * .8
        points += player['shots_on_goal']
        points += player['successful_tackles'] * 1
        points -= player['yellow_cards']
        points -= player['yellow_red_cards']
        points -= player['red_cards'] * 3
        if (player['minutes_played'] > 60):
            points += 1
        if (player['minutes_played'] >= 90):
            points += 1
        scored_players[idx]['points'] = points

    # deal with subs and get total score
    total_points = 0
    total_points += scored_players[0]['points']
    # check if goalie sub is necessary
    if (scored_players[0]['minutes_played'] == 0):
        total_points += scored_players[1]['points']

    total_points += scored_players[2]['points']
    total_points += scored_players[3]['points']
    total_points += scored_players[4]['points']
    total_points += scored_players[5]['points']
    # check if defense sub is necessary
    if (scored_players[2]['minutes_played'] == 0
    or scored_players[3]['minutes_played'] == 0
    or scored_players[4]['minutes_played'] == 0
    or scored_players[5]['minutes_played'] == 0):
        total_points += scored_players[6]['points']

    total_points += scored_players[7]['points']
    total_points += scored_players[8]['points']
    total_points += scored_players[9]['points']
    # check if midfield sub is necessary
    if (scored_players[7]['minutes_played'] == 0
    or scored_players[8]['minutes_played'] == 0
    or scored_players[9]['minutes_played'] == 0):
        total_points += scored_players[10]['points']

    total_points += scored_players[11]['points']
    total_points += scored_players[12]['points']
    total_points += scored_players[13]['points']
    # check if forward sub is necessary
    if (scored_players[11]['minutes_played'] == 0
    or scored_players[12]['minutes_played'] == 0
    or scored_players[13]['minutes_played'] == 0):
        total_points += scored_players[14]['points']

    return {
        'total_points': round(total_points, 1),
        'player_info': scored_players,
        'manager_name': roster.manager_name,
        'id': roster.id,
        "matchweek": roster.week.id
    }

import requests, re, time

# this is gross but I don't care
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

# still don't care
def update_players():
    print('Starting request for players...')

    url_front = 'https://api.sportradar.us/soccer-t3/eu/en/teams/sr:competitor:'
    url_back = '/profile.json?api_key=wen4p2gkyru39s2cxx3c5wae'

    # go through each team
    teams = Team.objects.all()
    for team in teams:
        time.sleep(1)

        print('Getting players on ' + team.name)
        url = url_front + str(team.id) + url_back
        response = requests.get(url)
        data = response.json()
        players = data['players']

        # save each player
        for player in players:
            # get player id from id string
            id_string = player['id']
            id_match = re.search(r'(\d+)$', id_string)
            id = int(id_string[id_match.start():id_match.end()])

            # get rest of attributes
            name = player['name']
            country_code = 'UNK'
            if 'country_code' in player:
                country_code = player['country_code']
            position = 'unknown'
            if 'type' in player:
                position = player['type']
            date_of_birth = '1900-1-1'
            if 'date_of_birth' in player:
                date_of_birth = player['date_of_birth']

            p = Player(id=id, team=team, name=name,
                country_code=country_code, position=position,
                date_of_birth=date_of_birth)
            p.save()
  

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class RosterList(generics.ListCreateAPIView):
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer

class RosterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer

class MatchweekList(generics.ListCreateAPIView):
    queryset = Matchweek.objects.all()
    serializer_class = MatchweekSerializer

class MatchweekDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Matchweek.objects.all()
    serializer_class = MatchweekSerializer

class ScoredRostersDetail(APIView):
    def get(self, request, matchweek_pk, roster_pk, format=None):
        roster = Roster.objects.get(pk=roster_pk)
        matchweek = Matchweek.objects.get(pk=matchweek_pk)
        scored_roster = generate_scored_roster(roster, matchweek)
        return Response(scored_roster)

class ScoredRostersList(APIView):
    def get(self, request, matchweek_pk, format=None):
        rosters = Roster.objects.filter(week=matchweek_pk)
        matchweek = Matchweek.objects.get(pk=matchweek_pk)
        # apply function to get scored roster to all of them and return
        scored_rosters = []
        for roster in rosters:
            scored_rosters.append(generate_scored_roster(roster, matchweek))
        return Response(scored_rosters)

class ScoredRostersAll(APIView):
    def get(self, request, format=None):
        rosters = Roster.objects.all()
        # apply function to get scored roster to all of them and return
        scored_rosters = []
        for roster in rosters:
            matchweek = roster.week
            scored_rosters.append(generate_scored_roster(roster, matchweek))
        return Response(scored_rosters)

class UpdateMatchStats(APIView):
    def get(self, request, date, format=None):
        get_match_stats(date)
        return Response({'message': 'Updated stats successfully'})

class UpdatePlayerStats(APIView):
    def get(self, request, format=None):
        update_players()
        return Response({'message': 'Updated players successfully'})
