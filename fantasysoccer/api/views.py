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
        'id': roster.id
    }
  

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
