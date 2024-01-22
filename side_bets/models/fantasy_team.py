from typing import Any
from django.db import models

class FantasyTeam(models.Model):
    sleeper_user_id = models.CharField(max_length=50)
    display_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    team_name = models.CharField(max_length=200)
    roster_id = models.IntegerField(blank=True, null=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True)

    # relationships
    # fantasy_teams = many-to-one rel from FantasyTeam
    league = models.ForeignKey(
        "FantasyLeague",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="fantasy_teams"
    )

    def __str__(self):
        return self.league.name + ': ' + self.team_name

    class Meta:
        unique_together = ('sleeper_user_id', 'league')
        verbose_name = 'Fantasy Team'
        verbose_name_plural = 'Fantasy Teams'