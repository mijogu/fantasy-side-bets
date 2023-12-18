from django.db import models

# from nfl_team import NFLTeam

class NFLGame(models.Model):
    # fields
    game_id = models.CharField(max_length=50, unique=True)
    away_team = models.CharField()
    away_score = models.IntegerField()
    away_result = models.CharField(max_length=5)
    home_team = models.CharField()
    home_score = models.IntegerField()
    home_result = models.CharField(max_length=5)
    game_date = models.DateField()
    game_time = models.TimeField()
    game_week = models.IntegerField()
    scores_imported = models.BooleanField()
    season = models.IntegerField()

    #relationships
    home_team = models.ForeignKey(
        "NFLTeam", 
        on_delete=models.SET_NULL,
        null=True, 
        related_name='home_games'
    )
    away_team = models.ForeignKey(
        "NFLTeam", 
        on_delete=models.SET_NULL,
        null=True, 
        related_name='away_games'
    )
    # boxscores -> many-to-one relationship from Boxscore

    def __str__(self):
        return self.game_id