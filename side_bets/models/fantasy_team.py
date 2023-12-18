from django.db import models

# from .fantasy_manager import FantasyManager
# from .fantasy_league import FantasyLeague

class FantasyTeam(models.Model):
    # fields
    sleeper_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    # relationships
    manager = models.ForeignKey(
        "FantasyManager", 
        on_delete=models.SET_NULL,
        null=True,  
        related_name='fantasy_teams'
    )
    league = models.ForeignKey(
        "FantasyLeague", 
        on_delete=models.SET_NULL,
        null=True, 
        related_name='fantasy_teams'
    )
    # boxscores = many-to-one rel from Boxscore