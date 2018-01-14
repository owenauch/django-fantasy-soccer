from api.models import *
from api.serializers import *
from rest_framework import generics


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

