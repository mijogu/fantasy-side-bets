from django.db import models 

class FantasyLeague(models.Model):
    # fields 
    sleeper_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    season = models.IntegerField()
    managers_imported = models.BooleanField()
    active = models.BooleanField()

    # relationships
    # fantasy_teams = many-to-one rel from FantasyTeam
    