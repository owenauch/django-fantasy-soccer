from api.models import *
from api.serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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

class ScoredRostersList(APIView):
    def get(self, request, format=None):
        return null
