from django.db import models 
from .fantasy_roster_week import FantasyRosterWeek


class FantasyLeague(models.Model):
    # fields 
    league_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    season = models.IntegerField()
    platform = models.CharField(max_length=100, default='sleeper')
    
    are_teams_imported = models.BooleanField(default=False)
    are_users_imported = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # relationships
    # fantasy_teams = many-to-one rel from FantasyTeam
    # games = many-to-one rel from FantasyRosterWeek
    
    def __str__(self):
        return f"{self.name} {self.season}"
    
    def getLeagueWeeksList(self):
        weeks = FantasyRosterWeek.objects \
            .filter(league_id=self.id) \
            .values('game_week') \
            .distinct()
        return weeks

    def getLeagueGames(self, week = 'all'):
        pass 
        if week == 'all':
            games = self.games.all().orderby('game_week')
        else:
            games = self.games.filter(game_week=week)
        
        return games