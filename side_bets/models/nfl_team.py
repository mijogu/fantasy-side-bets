from django.db import models

class NFLTeam(models.Model):
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)

    # relationships
    # players = many-to-one rel from NFLPlayer
    # home_games => many-to-one from NFLGame 
    # away_games => many-to-one from NFLGame 

    def __str__(self):
        return f"{self.city} {self.name}"