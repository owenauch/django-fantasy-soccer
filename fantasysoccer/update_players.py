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
import requests, re, time
from api.models import *

def update_players():
    print('Starting request for players...')

    url_front = 'https://api.sportradar.us/soccer-t3/eu/en/teams/sr:competitor:'
    url_back = '/profile.json?api_key=qq5z5t88838bu8kcwe4qvbjn'

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

if __name__ == "__main__":
    update_players()
