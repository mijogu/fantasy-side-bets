from django.db import models

# from nfl_team import NFLTeam

class NFLPlayer(models.Model):
    #fields
    sleeper_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    espn_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    yahoo_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    nfl_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    fantasypros_id = models.CharField(max_length=30, blank=True, null=True)
    fantasy_data_id = models.CharField(max_length=30, blank=True, null=True)
    rotowire_id = models.CharField(max_length=30, blank=True, null=True)
    rotoworld_id = models.CharField(max_length=30, blank=True, null=True)
    swish_id = models.CharField(max_length=30, blank=True, null=True)
    number = models.CharField(max_length=30, blank=True, null=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=10, blank=True, null=True)

    #relationships
    team = models.ForeignKey(
        "NFLTeam", 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='players', 
    )
    # boxscores => many-to-one from NFLBoxscore

    def __str__(self):
        if self.team:
            return f"{self.full_name} {self.position} ({self.team.id})"
        else:
            return f"{self.full_name} {self.position}"
    
    class Meta: 
        verbose_name = 'NFL Player'
        verbose_name_plural = 'NFL Players'