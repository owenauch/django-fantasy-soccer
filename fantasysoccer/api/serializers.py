from rest_framework import serializers
from api.models import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'team', 'name', 'country_code',
            'position', 'date_of_birth')


