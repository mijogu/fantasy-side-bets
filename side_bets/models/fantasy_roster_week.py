from django.db import models 
from .nfl_boxscore import NFLBoxscore

class FantasyRosterWeek(models.Model):
    # fields
    starters = models.CharField(max_length=1000, blank=True, null=True)
    bench = models.CharField(max_length=1000, blank=True, null=True)
    roster_id = models.IntegerField(blank=True, null=True)
    matchup_id = models.IntegerField(blank=True, null=True)
    game_week = models.IntegerField(blank=True, null=True)

    # relationships
    league = models.ForeignKey(
        "FantasyLeague",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="roster_weeks"
    )
    team = models.ForeignKey(
        "FantasyTeam",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="roster_weeks",
    )

    @property
    def boxscores(self):
        starters = self.starters.split(',') 
        
        boxscores = NFLBoxscore.objects.filter()

        return starters

    def __str__(self):
        return f"{self.team.team_name}: week {self.game_week}"

    class Meta:
        unique_together = ('league', 'game_week', 'team')
        verbose_name = 'Fantasy Roster Week'
        verbose_name_plural = 'Fantasy Roster Weeks'
