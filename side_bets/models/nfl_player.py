from django.db import models

# from nfl_team import NFLTeam

class NFLPlayer(models.Model):
    #fields
    sleeper_id = models.CharField(max_length=30, unique=True)
    espn_id = models.CharField(max_length=30, unique=True)
    yahoo_id = models.CharField(max_length=30, unique=True)
    nfl_id = models.CharField(max_length=30, unique=True)
    fantasypros_id = models.CharField(max_length=30)
    fantasy_data_id = models.CharField(max_length=30)
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=10)

    #relationships
    team = models.ForeignKey(
        "NFLTeam", 
        on_delete=models.SET_NULL, 
        related_name='players', 
        null=True
    )
    # boxscores => many-to-one from NFLBoxscore

    def __str__(self):
        return self.full_name + ": " + self.team