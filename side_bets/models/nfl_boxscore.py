from django.db import models

from nfl_game import NFLGame
from nfl_player import NFLPlayer
from fantasy_team import FantasyTeam

class NFLBoxscore(models.Model):
    # rushing fields
    rushing_tds = models.IntegerField()
    rushing_yards = models.IntegerField()
    carries = models.IntegerField()
    
    # passing fields
    passing_tds = models.IntegerField()
    passing_yards = models.IntegerField()
    passing_completions = models.IntegerField()
    passing_ints = models.IntegerField()
    
    # receiving fields
    receiving_tds = models.IntegerField()
    receiving_yards = models.IntegerField()
    receptions = models.IntegerField()
    targets = models.IntegerField()
    
    # other fields
    fumbles = models.IntegerField()
    fumbles_lost = models.IntegerField()

    # relationships
    player = models.ForeignKey(NFLPlayer, related_name='boxscores')
    game = models.ForeignKey(NFLGame, related_name='boxscores')
    fantasy_team = models.ForeignKey(FantasyTeam, related_name='boxscores')

    def __str__(self): 
        return self.player.full_name + ' in game ' + self.game.game_id

    class Meta:
        unique_together = ('player', 'game')