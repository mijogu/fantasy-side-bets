import requests
import json 
from datetime import date

from side_bets.models import FantasyLeague, FantasyTeam, FantasyRosterWeek, NFLPlayer

class SleeperAPI:
    json_server = False
    to_csv = False

    host = 'https://api.sleeper.app/v1'
    username = 'mijogu'
    user_id = '455441209981136896'
    league_id = '986851253214863360'
    year = '2023'
    week = '1'
    
    def __init__(self):
        pass 
    
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
        if self.json_server:
            request = requests.get("http://localhost:3000/db")
        else: 
            request = requests.get(f"{self.host}/players/{sport}")
        return request.json()
    
    def generateNflPlayerFile(self):
        today = date.today()
        filename = f"nfl-players-{today.month}-{today.day}-{today.year}.json"

        data = self.getNflPlayers()
        json_object = json.dumps(data, indent=4)

        with open(filename, "w") as outfile:
            outfile.write(json_object)


class SleeperImporter:
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
            season = sleeper_league['season']
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
            teams.append(FantasyTeam(
                sleeper_user_id = user.get("user_id"),
                display_name = display,
                team_name = user.get("metadata", {}).get("team_name", f"Team {display}"),
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
        new_rosters = []
        for roster in sleeper_matchups:
            roster_team = league.fantasy_teams.get(roster_id=roster["roster_id"])
            # opponent_team = FantasyTeam.objects.get(sleeper_user_id=roster["owner_id"])
            
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
        rosters_imported = FantasyRosterWeek.objects.bulk_create(new_rosters)
        print(f"Imported {len(rosters_imported)} rosters")
        return rosters_imported
    
    @staticmethod
    def importLeagueMatchups(league_id = None, week = None):
        pass

    @staticmethod
    def importPlayers():
        player_positions = ['QB', 'RB', 'WR', 'TE']
        sleeper = SleeperAPI()
        players = sleeper.getPlayers()
        args = []
        for key in players:
            player = players[key]
            if player["position"] in player_positions and player["team"] is not None:
                args.append((
                    player["player_id"]         if "player_id" in player else "",
                    player["position"]          if "position" in player else "",
                    player["team"]              if "team" in player else "",
                    player["first_name"]        if "first_name" in player else "",
                    player["last_name"]         if "last_name" in player else "",
                    player["full_name"]         if "full_name" in player else "",
                    player["fantasy_data_id"]   if "fantasy_data_id" in player else "",
                    player["espn_id"]           if "espn_id" in player else "",
                    player["yahoo_id"]          if "yahoo_id" in player else ""
                ))
            # sleeper_id VARCHAR(10),
            # espn_id VARCHAR(10),
            # yahoo_id VARCHAR(10),
            # nfl_id VARCHAR(10),
            # fantasypros_id VARCHAR(10),
            # position VARCHAR(10),
            # team VARCHAR(5),
            # first_name VARCHAR(20),
            # last_name VARCHAR(30),
            # full_name VARCHAR(50)                

        # # NFL Players INSERT
        sql = """INSERT INTO players
            (id, sleeper_id, position, team, first_name, last_name, full_name, fantasy_data_id, espn_id, yahoo_id)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ;"""
        db = Database()
        imported = db.insertmany(sql, args)
        print(f"Imported {imported} rosters")
        