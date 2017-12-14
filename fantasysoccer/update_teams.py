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
import requests, time, re
from api.models import *

url_front = 'https://api.sportradar.us/soccer-t3/eu/en/tournaments/sr:tournament:'
url_back = '/info.json?api_key=qq5z5t88838bu8kcwe4qvbjn'
league_ids = ['8','17','23','34','35']

# get teams for every league
for league_id in league_ids: 
    # can't request more than once a second
    time.sleep(1)

    # get data
    url = url_front + league_id + url_back
    response = requests.get(url)
    data = response.json()
    teams = data['groups'][0]['teams']
    # get each team and save
    for team in teams:
        # get team id from id string
        id_string = team['id']
        id_match = re.search(r'(\d+)$', id_string)
        id = int(id_string[id_match.start():id_match.end()])

        name = team['name']
        country_code = team['country_code']
        abbreviation = team['abbreviation']

        t = Team(id=id, name=name, country_code=country_code, abbreviation=abbreviation)
        t.save()

print('Teams successfully saved to DB!')