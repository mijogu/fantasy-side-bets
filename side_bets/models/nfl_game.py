from django.db import models

class NFLGame(models.Model):
    # fields
    id = models.CharField(max_length=50, primary_key=True)
    away_score = models.IntegerField(blank=True, null=True)
    away_result = models.CharField(max_length=5, blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True)
    home_result = models.CharField(max_length=5, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=10, blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    are_scores_imported = models.BooleanField(default=False)

    #relationships
    home_team = models.ForeignKey(
        "NFLTeam", 
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        related_name='home_games'
    )
    away_team = models.ForeignKey(
        "NFLTeam", 
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        related_name='away_games'
    )
    season = models.ForeignKey(
        "NFLSeason",
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True,
        related_name='games'
    )

    # boxscores -> many-to-one relationship from Boxscore

    def __str__(self):
        return self.id
    
    class Meta: 
        verbose_name = 'NFL Game'
        verbose_name_plural = 'NFL Games'