import requests

response = requests.get('https://api.sportradar.us/soccer-t3/eu/en/tournaments/sr:tournament:17/info.json?api_key=qq5z5t88838bu8kcwe4qvbjn')
data = response.json()
teams = data['groups'][0]['teams']
print(teams)