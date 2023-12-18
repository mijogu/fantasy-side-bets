from django.db import models

class FantasyManager(models.Model):
    sleeper_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    display_name = models.CharField(max_length=200)

    # relationships
    # fantasy_teams = many-to-one rel from FantasyTeam

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
