from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.forms.models import model_to_dict

from .models import SleeperImporter
from .models import TankStatsImporter
from .models.forms import ImportFantasyLeagueForm
from side_bets.models import \
    FantasyLeague, FantasyTeam, FantasyRosterWeek, \
    NFLSeason, NFLGame, NFLPlayer

default_league_id = '986851253214863360'
default_week = 1
errmsg = "Something didn't work"

def welcome(request):
    return render(request, 'welcome.html')

def league(request, pk):
    league = get_object_or_404(FantasyLeague, pk=pk)
    msg = None
    if request.method == 'POST':
        if request.POST['import_type'] == 'teams':
            teams = SleeperImporter.importLeagueTeams(league_id=league.league_id)
            league.are_teams_imported = True
            league.save()
            league.refresh_from_db()
            msg = 'Teams imported successfully!'
        elif request.POST['import_type'] == 'rosterweeks' and request.POST['week'] != '':
            roster_weeks = SleeperImporter.importRostersForWeek(league_id=league.league_id, week=request.POST['week'])
            msg = f'{len(roster_weeks)} Roster weeks imported!'
            pass    
        elif request.POST['import_type'] == 'delete':
            league.delete()
            return redirect('league_list')
        elif request.POST['import_type'] == 'deleteteams':
            teams = league.fantasy_teams.all()
            teams.delete()
            league.are_teams_imported = False
            league.save()
            league.refresh_from_db()
            msg = 'Deleted teams!'

    weeks = league.getLeagueWeeksList()
    return render(request, 'league.html', { 'league': league, 'msg': msg, 'weeks': weeks })

def league_list(request):
    new_league = False
    if request.method == 'POST':
        form = ImportFantasyLeagueForm(request.POST)
        if form.is_valid():
            new_league = form.save()
    else:
        # form = ImportFantasyLeagueForm(initial={ 'league_id': '986851253214863360'})
        form = ImportFantasyLeagueForm(initial={ 'league_id': '1005144379184582656'})

    leagues = FantasyLeague.objects.all()
    return render(request, 'league_list.html', { 'leagues': leagues, 'new_league': new_league, 'form': form })

def league_week(request, pk, week):
    league = get_object_or_404(FantasyLeague, pk=pk)
    rosters = FantasyRosterWeek.objects.filter(league=league, game_week=week)

    # split roster.starters for each team
    # get those NFL players: boxscore and player data
    #   boxscore -> 
    # join data 

    # get NFL players
    # get NFL player boxscores
    # link NFL players to rosters
    return render(request, 'league_week.html', { 'league': league, 'rosters': rosters, 'week': week })


def season_list(request):
    seasons = NFLSeason.objects.all()
    return render(request, 'season_list.html', { 'seasons': seasons })

def nfl_player_list(request):
    filter = None
    msg = ""
    if request.method == 'POST':
        if request.POST['form_type'] == 'importplayers':
            players = SleeperImporter.importPlayers() # TODO fix after refactoring import process
            msg = 'Players imported successfully!'
        elif request.POST['form_type'] == 'deleteplayers':
            players = NFLPlayer.objects.all()
            players.delete()
            msg = "Players deleted!"
        elif request.POST['form_type'] == 'fix_espn_id':
            msg = "DRY RUN: fixed espn IDs"
        elif request.POST['form_type'] == "sleeper_player_import":
            import_data = SleeperImporter.pullPlayerData()
            if import_data['msg'] != None:
                msg = import_data['msg']
            else:
                msg = f"{len(import_data['data'])} sleeper players imported into {import_data['filename']}"
        elif request.POST['form_type'] == "tankstats_player_import":
            msg = "DRY RUN: tankstats players imported"
    # elif request.method == 'GET' and "filter" in request.GET:
    #     filter = request.GET['filter']
    #     if filter == "missing_espn_id":
    #         players = NFLPlayer.objects.filter(espn_id__isnull=True)
        
    # get list of Sleeper Player files
    # get list of TankStats Player files

    players = NFLPlayer.objects.filter(espn_id__isnull=True)
    return render(request, 'nfl_player_list.html', { 'players': players, 'msg': msg, 'filter': filter })

def season(request, pk):
    msg = None
    if request.method == 'POST':
        if request.POST['import_type'] == 'nflgames':
            week = request.POST['week']
            season = request.POST['season']
            nflgames = TankStatsImporter.importNFLGames(week=week, season=season)
            msg = f"{len(nflgames)} NFL Games imported successfully!"
    season = get_object_or_404(NFLSeason, pk=pk)
    return render(request, 'season.html', { 'season': season, 'msg': msg })

def nfl_game(request, pk):
    game = get_object_or_404(NFLGame, pk=pk)
    msg = None
    if request.method == 'POST':
        if request.POST['import_type'] == 'boxscores':
            boxscores = TankStatsImporter.importBoxScores(game_id=pk)
            msg = f"{len(boxscores)} NFL Boxscores imported successfully!"

    game.refresh_from_db()
    return render(request, 'nflgame.html', { 'game': game, 'msg': msg })

    

# def importFantasyLeague(request):
#     errors = None
#     if request.method == 'POST':
#         form = ImportFantasyLeagueForm(request.POST)
#         if form.is_valid():
#             form.save()
#             redirect('leagues')
#     else:
#         form = ImportFantasyLeagueForm()
#     # import logic 
#     league = SleeperImporter.importLeague(league_id=default_league_id)
#     if league is False:
#         msg = errmsg
#     else:
#         msg = "League imported successfully!"
#     all = FantasyLeague.objects.all()
#     return render(request, 'import.html', { 'msg': msg, 'data' : league, 'all': all })

# def importFantasyTeams(request):
#     # import logic 
#     teams = SleeperImporter.importLeagueTeams(league_id=default_league_id)
#     if teams is False:
#         msg = errmsg
#     else:
#         msg = "FantasyTeams imported successfully!"
#     all = FantasyTeam.objects.all()
#     return render(request, 'import.html', { 'msg': msg, 'data' : teams, 'all': all })

# def importRosterWeeks(request):
#     rosterweeks = SleeperImporter.importRostersForWeek(league_id=default_league_id, week=default_week)
#     if rosterweeks is False:
#         msg = errmsg
#     else: 
#         msg = "FantasyRosterWeeks imported successfully!"
#     all = FantasyRosterWeek.objects.all()
#     return render(request, 'import.html', { 'msg': msg, 'data' : rosterweeks, 'all': all })