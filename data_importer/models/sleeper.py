import requests
import json 
from datetime import date
from cleantext import clean
from pathlib import Path

from side_bets.models import \
    FantasyLeague, FantasyTeam, FantasyRosterWeek, \
    NFLPlayer, NFLTeam

class SleeperAPI:
    use_json_server = False
    to_csv = False

    username = 'mijogu'
    user_id = '455441209981136896'
    league_id = '986851253214863360'
    year = '2023'
    week = '1'
    
    def __init__(self):
        if self.use_json_server:
            self.host = "http://localhost:3000"
        else:
            self.host = 'https://api.sleeper.app/v1'
    
    def getUser(self, user_id = None):
        if user_id is None:
            user_id = self.user_id
        request = requests.get(f"{self.host}/user/{user_id}")
        return request.json()
    
    def getLeaguesForUser(self, user_id = None):
        if user_id is None:
            user_id = self.user_id
        year = self.year
        request = requests.get(f"{self.host}/user/{user_id}/leagues/nfl/{year}")
        return request.json()
    
    def getLeague(self, league_id = None):
        if league_id is None:
            league_id = self.league_id
        request = requests.get(f"{self.host}/league/{league_id}")
        return request.json()
    
    def getLeagueRosters(self, league_id = None):
        if league_id is None:
            league_id = self.league_id
        request = requests.get(f"{self.host}/league/{league_id}/rosters")
        return request.json()
    
    def getLeagueMatchups(self, league_id = None, week = None):
        if league_id is None: 
            league_id = self.league_id
        request = requests.get(f"{self.host}/league/{league_id}/matchups/{week}")
        return request.json()
    
    def getLeagueUsers(self, league_id = None):
        if league_id is None:
            league_id = self.league_id
        request = requests.get(f"{self.host}/league/{league_id}/users")
        return request.json()
    
    def getPlayers(self, sport = 'nfl'):
        if self.use_json_server:
            request = requests.get("http://localhost:3000/db")
        else: 
            request = requests.get(f"{self.host}/players/{sport}")
        return request.json()
    
    # def pullPlayerData(self):
    #     today = date.today()
    #     filename = f"nfl-players-{today.month}-{today.day}-{today.year}.json"

    #     data = self.getNflPlayers()
    #     json_object = json.dumps(data, indent=4)

    #     with open(filename, "w") as outfile:
    #         outfile.write(json_object)


class SleeperImporter:
    path = Path(__file__).parent.parent
    playerfiles = path / 'playerfiles'

    def __init__(self):
        pass

    @staticmethod
    def importLeague(league_id = None):
        if league_id is None:
            return False
        
        sleeper = SleeperAPI()
        sleeper_league = sleeper.getLeague(league_id)   

        new_league = FantasyLeague(
            league_id = sleeper_league['league_id'],
            name = sleeper_league['name'],
            season_id = sleeper_league['season']
        )
        new_league.save()
        print(f"Imported league id: {new_league.league_id}")
        return new_league

    @staticmethod
    def importLeagueTeams(league_id = None):
        if league_id is None:
            return False
        
        # get sleeper User and Rosters
        sleeper = SleeperAPI()
        sleeper_users = sleeper.getLeagueUsers(league_id)
        sleeper_rosters = sleeper.getLeagueRosters(league_id)
        
        # create dictionairy of {user_id: roster_id}
        roster_ids = {}
        for roster in sleeper_rosters:
            roster_ids[roster["owner_id"]] = roster["roster_id"]

        league = FantasyLeague.objects.get(league_id=league_id)        
        teams = []
        for user in sleeper_users:
            display = user.get("display_name", user["user_id"])
            team_name = user.get("metadata", {}).get("team_name", f"Team {display}")
            teams.append(FantasyTeam(
                sleeper_user_id = user.get("user_id"),
                display_name = display,
                # team_name = user.get("metadata", {}).get("team_name", f"Team {display}"),
                team_name = clean(team_name, no_emoji=True),
                roster_id = roster_ids[user["user_id"]],
                league = league
            ))
        teams_imported = FantasyTeam.objects.bulk_create(teams)    
        print(f"Imported {len(teams_imported)} teams")
        return teams_imported

    @staticmethod
    def importRostersForWeek(league_id = None, week = None):
        if league_id is None or week is None: 
            return False 
        
        sleeper = SleeperAPI()
        sleeper_matchups = sleeper.getLeagueMatchups(league_id, week)

        league = FantasyLeague.objects.get(league_id=league_id)
        rosters_for_week = FantasyRosterWeek.objects.filter(league_id=league.id, game_week=week).values_list("team_id", flat=True)
        new_rosters = []
        for roster in sleeper_matchups:
            roster_team = league.fantasy_teams.get(roster_id=roster["roster_id"])
            # opponent_team = FantasyTeam.objects.get(sleeper_user_id=roster["owner_id"])
            
            if (roster_team.id not in rosters_for_week):
                starters = ','.join(roster['starters'])
                bench_players = set(roster['players']).difference(set(roster['starters']))
                bench = ','.join(bench_players)

                new_rosters.append(FantasyRosterWeek(
                    starters = starters,
                    bench = bench,
                    roster_id = roster["roster_id"],
                    matchup_id = roster["matchup_id"],
                    game_week = week,
                    league = league,
                    team = roster_team,
                    # opponent = opponent_team,
                ))
            else: 
                print(f"Roster already found for {roster_team} in week {week}")
        rosters_imported = FantasyRosterWeek.objects.bulk_create(new_rosters)
        print(f"Imported {len(rosters_imported)} rosters")
        return rosters_imported
    
    @staticmethod
    def importLeagueMatchups(league_id = None, week = None):
        pass

    staticmethod
    def pullPlayerData():
        print('Pulling Sleeper player data')
        today = date.today()

        filename = f"sleeper-players-{today.month}-{today.day}-{today.year}.json"
        filepath = SleeperImporter.playerfiles / filename
        msg = None

        # check if file exists
        if filepath.exists:
            data = []
            msg = f"{filename} already exists - nothing done."
        else: 
            sleeper = SleeperAPI()
            data = sleeper.getPlayers()
            json_object = json.dumps(data, indent=4)
            with open(filepath, "w") as outfile:
                outfile.write(json_object)
            
        return {
            'data': data, 
            'filename': filename,
            'msg': msg
        }

    @staticmethod
    def importPlayers():
        # player_positions = ['QB', 'RB', 'WR', 'TE']
        ignore_positions = ['DEF']
        ignore_players = []
        teams = NFLTeam.objects.values_list('id', flat=True)

        sleeper = SleeperAPI()
        players = sleeper.getPlayers()
        new_players = []
        for key in players:
            player = players[key]

            if player["position"] in ignore_positions or \
                player["player_id"] in ignore_players or \
                player["full_name"] == "Duplicate Player" or \
                player["full_name"] == "Player Invalid":
                continue

            # if player["position"] in player_positions and \
            # if "search_full_name" in player and player["search_full_name"] != "duplicateplayer":
            try:
                new_players.append(NFLPlayer(
                    sleeper_id = player["player_id"], 
                    espn_id = player["espn_id"], 
                    # TODO store these values later, yahoo_id was a problem
                    # yahoo_id = player["yahoo_id"], 
                    # fantasy_data_id = player["fantasy_data_id"], 
                    # rotowire_id = player["rotowire_id"], 
                    # rotoworld_id = player["rotoworld_id"], 
                    # swish_id = player["swish_id"], 
                    number = player["number"], 
                    first_name = player["first_name"], 
                    last_name = player["last_name"], 
                    full_name = player["full_name"], 
                    position = player["position"], 
                    team_id = NFLTeam.cleanAbbreviation(player["team"]), 
                    # player["player_id"]         if "player_id" in player else "",
                    # player["position"]          if "position" in player else "",
                    # player["team"]              if "team" in player else "",
                    # player["first_name"]        if "first_name" in player else "",
                    # player["last_name"]         if "last_name" in player else "",
                    # player["full_name"]         if "full_name" in player else "",
                    # player["fantasy_data_id"]   if "fantasy_data_id" in player else "",
                    # player["espn_id"]           if "espn_id" in player else "",
                    # player["yahoo_id"]          if "yahoo_id" in player else ""
                ))  
            except Exception as exception:
                print(f"{exception}")
                print("...from the following data...")
                print(json.dumps(player))

        # return new_players
    
        print(f"Attempting to create {len(new_players)} NFL players")
        players_imported = NFLPlayer.objects.bulk_create(new_players, 400)
        print(f"Imported {len(players_imported)} NFL players")
        return players_imported
        
        