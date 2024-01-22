from django.db import models
from .nfl_game import NFLGame


class NFLSeason(models.Model):
    reg_season_weeks = 18
    year = models.CharField(max_length=4, blank=True, null=True)
    are_games_imported = models.BooleanField(default=False)

    # games = many-to-one from NFLGame
    # fantasy_leagues = many-to-one from FantasyLeague

    @property
    def number_of_games(self):
        return NFLGame.objects.filter(season=self).count()

    def __str__(self):
        return f"{self.year} NFL Season"
    
    def getGameIDs(self):
        pass
        # get the list of NFLGame IDs only
    
    def getNumberOfGames(self):
        pass
        # return int num of total games
        # each season should have 272 reg season games
    
    class Meta: 
        verbose_name = 'NFL Season'
        verbose_name_plural = 'NFL Seasons'
    
    # def save(self):
    #     # initial save
    #     super(NFLSeason, self).save()
        
    #     # import games for the season

    #     # update season
    #     self.are_games_imported = True
    #     super(NFLSeason, self).save()



# NFLSeasondef save(self, *args, **kwargs):
#         self.slug = slugify(self.title)
#         super(GeeksModel, self).save(*args, **kwargs)