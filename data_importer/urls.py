
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('leagues/', views.leagues, name='leagues'),
    path('leagues/<int:pk>', views.league, name='view_league'),
    path('leagues/<int:pk>/week/<int:week>', views.league_week, name='league_week'),
    
    # path('importleague', views.importFantasyLeague, name='import_league'),
    # path('importteams', views.importFantasyTeams, name='import_teams'),
    # path('importrosterweek', views.importRosterWeeks, name='import_roster_weeks'),
]
