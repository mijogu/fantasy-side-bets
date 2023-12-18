from django.contrib import admin
from django.db import models

from .models.fantasy_manager import FantasyManager
from .models.fantasy_team import FantasyTeam
from .models.fantasy_league import FantasyLeague

from .models.nfl_boxscore import NFLBoxscore
from .models.nfl_player import NFLPlayer
from .models.nfl_team import NFLTeam
from .models.nfl_game import NFLGame

admin.site.register(FantasyManager)
admin.site.register(FantasyTeam)
admin.site.register(FantasyLeague)

admin.site.register(NFLBoxscore)
admin.site.register(NFLPlayer)
admin.site.register(NFLTeam)
admin.site.register(NFLGame)
