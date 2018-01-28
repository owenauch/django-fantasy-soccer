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
            "minutes_played": 0,
            "goals": 0,
            "assists": 0
        }

        if (len(match_stats) == 1):
            for stat in stats:
                new_stat = getattr(match_stats[0], stat)
                setattr(player_stats, stat, new_stat)
        # if there are multiple, loop through and add them together
        else:
            for idx, match_stat in enumerate(match_stats):
                for stat in stats:
                    if (idx == 0):
                        setattr(player_stats, stat, getattr(match_stats[0], stat))
                    else:
                        new_value = getattr(match_stats[idx], stat) + getattr(player_stats, stat)
                        setattr(player_stats, stat, getattr(match_stats[idx], new_value))

        scored_players.append(player_stats)

    return scored_players

  

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
        return Response({})
