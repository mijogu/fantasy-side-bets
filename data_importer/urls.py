
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),

    path('leagues/', views.league_list, name='league_list'),
    path('leagues/<int:pk>', views.league, name='view_league'),
    path('leagues/<int:pk>/week/<int:week>', views.league_week, name='league_week'),

    path('seasons/', views.season_list, name='season_list'),
    path('seasons/<int:pk>', views.season, name='view_season'),

    path('games/<str:pk>', views.nfl_game, name='view_nflgame'),
    
    path('players', views.nfl_player_list, name='nfl_player_list')

    # path('importleague', views.importFantasyLeague, name='import_league'),
    # path('importteams', views.importFantasyTeams, name='import_teams'),
    # path('importrosterweek', views.importRosterWeeks, name='import_roster_weeks'),
]
