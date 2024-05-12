from django.db import models

from .nfl_player import NFLPlayer

class NFLBoxscore(models.Model):
    # rushing fields
    rushing_tds = models.IntegerField(default=0)
    rushing_yards = models.IntegerField(default=0)
    carries = models.IntegerField(default=0)
    
    # passing fields
    passing_tds = models.IntegerField(default=0)
    passing_yards = models.IntegerField(default=0)
    passing_completions = models.IntegerField(default=0)
    passing_ints = models.IntegerField(default=0)
    
    # receiving fields
    receiving_tds = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    receptions = models.IntegerField(default=0)
    targets = models.IntegerField(default=0)
    
    # other fields
    fumbles = models.IntegerField(default=0)
    fumbles_lost = models.IntegerField(default=0)

    player_id = models.CharField(max_length=30, blank=True, null=True)

    # relationships
    game = models.ForeignKey(
        "NFLGame", 
        on_delete=models.CASCADE, 
        null=True,
        related_name='boxscores',
        db_index=False,
        db_constraint=False
    )

    @property
    def player(self):
        try:
            player = NFLPlayer.objects.get(espn_id=self.player_id)
        except Exception as e:
            print(e)
            player = NFLPlayer(full_name=f"(player id {self.player_id})")
        return player

    def __str__(self): 
        return self.player.full_name + ' in game ' + self.game.id

    class Meta:
        verbose_name = 'NFL Boxscore'
        verbose_name_plural = 'NFL Boxscores'