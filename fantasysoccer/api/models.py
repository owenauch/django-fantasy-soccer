from django.db import models

# Create your models here.
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