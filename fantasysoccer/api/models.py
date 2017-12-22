from django.db import models
from django.contrib.auth.models import User

# teams in real life
class Team(models.Model):
    COUNTRY_CODES = (
        ('ENG', 'England'),
        ('ESP', 'Spain'),
        ('ITA', 'Italy'),
        ('FRA', 'France'),
        ('DEU', 'Germany') 
    )

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    country_code = models.CharField(max_length=3, choices=COUNTRY_CODES)
    abbreviation = models.CharField(max_length=10, blank=False)

class Player(models.Model):
    POSITIONS = (
        ('goalkeeper', 'GK'),
        ('defender', 'D'),
        ('midfielder', 'M'),
        ('forward', 'F')
    )

    id = models.IntegerField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False)
    country_code = models.CharField(max_length=3, blank=False)
    position = models.CharField(max_length=15, choices=POSITIONS)
    date_of_birth = models.DateField(blank=False)

class MatchStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    substituted_in = models.IntegerField(default=0)
    substituted_out = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    yellow_red_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    interceptions = models.IntegerField(default=0)
    chances_created = models.IntegerField(default=0)
    successful_crosses = models.IntegerField(default=0)
    crosses = models.IntegerField(default=0)
    successful_tackles = models.IntegerField(default=0)
    tackles = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    shots_saved = models.IntegerField(default=0)
    shots_faced = models.IntegerField(default=0)
    penalties_faced = models.IntegerField(default=0)
    penalties_saved = models.IntegerField(default=0)
    fouls_committed = models.IntegerField(default=0)
    shots_on_goal = models.IntegerField(default=0)
    shots_off_goal = models.IntegerField(default=0)
    shots_blocked = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    penalty_goals = models.IntegerField(default=0)
    match_date = models.DateField(blank=False)

class League(models.Model):
    name = models.CharField(max_length=200)

# user clubs within the game
class Club(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    transfer_balance = models.IntegerField(default=200000000)
    players = models.ManyToManyField(Player)

class Matchweek(models.Model):
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)

class Roster(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    week = models.ForeignKey(Matchweek, on_delete=models.CASCADE)
    gk = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='gk')
    gk_sub = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='gk_sub')
    d_one = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='d_one')
    d_two = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='d_two')
    d_three = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='d_three')
    d_four = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='d_four')
    d_sub = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='d_sub')
    m_one = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='m_one')
    m_two = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='m_two')
    m_three = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='m_three')
    m_four = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='m_four')
    m_sub = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='m_sub')
    f_one = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='f_one')
    f_two = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='f_two')
    f_three = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='f_three')
    f_sub = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='f_sub')
