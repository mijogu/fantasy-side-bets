from django.db import models

class NFLTeam(models.Model): 
    id = models.CharField(max_length=10, primary_key=True)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True)
    conference = models.CharField(max_length=3, null=True)
    division = models.CharField(max_length=5, null=True)

    # relationships
    # players = many-to-one rel from NFLPlayer
    # home_games => many-to-one from NFLGame 
    # away_games => many-to-one from NFLGame 

    def __str__(self):
        return f"{self.city} {self.name}"
    
    @staticmethod
    def cleanAbbreviation(abbr):
        match abbr:
            case 'ARZ':
                return 'ARI'
            case 'BLT':
                return 'BAL'
            case 'CLV':
                return 'CLE'
            case 'HST':
                return 'HOU'
            case 'LA':
                return 'LAR'
            case 'OAK':
                return 'LV'
            case 'WSH':
                return 'WAS' 
            case None:
                return 'NONE'
            case _:
                return abbr

    class Meta: 
        verbose_name = 'NFL Team'
        verbose_name_plural = 'NFL Teams'
