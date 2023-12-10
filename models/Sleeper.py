import requests
import json 
from datetime import date

from Database import *

class SleeperAPI():
    json_server = True
    to_csv = False

    host = 'https://api.sleeper.app/v1'
    username = 'mijogu'
    user_id = '455441209981136896'
    league_id = '986851253214863360'
    year = '2023'
    
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
    
    def getLeagueManagers(self, league_id = None):
        if league_id is None:
            league_id = self.league_id
        request = requests.get(f"{self.host}/league/{league_id}/users")
        return request.json()
    
    def getPlayers(self, sport = 'nfl'):
        if self.json_server:
            request = requests.get("http://localhost:3000/db")
            return request.json()
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
    player_positions = ['QB', 'RB', 'WR', 'TE']

    def __init__(self):
        pass

    def setupTables(self):
        db = Database()
        args = []

        # league table
        sql = """CREATE TABLE IF NOT EXISTS leagues(
            league_id VARCHAR(50) PRIMARY KEY,
            season YEAR(4),
            name VARCHAR(100),
            sport VARCHAR(50) DEFAULT 'nfl',
            platform VARCHAR(50) DEFAULT 'sleeper'
        );"""        
        cursor = db.query(sql, args)

        # managers table
        sql = """CREATE TABLE IF NOT EXISTS managers(
            user_id VARCHAR(50),
            league_id VARCHAR(50),
            display_name VARCHAR(50),
            team_name VARCHAR(100),
            PRIMARY KEY (league_id, user_id)
        );"""
        cursor = db.query(sql, args)

        # # rosters table
        sql = """CREATE TABLE IF NOT EXISTS rosters(
            manager_id VARCHAR(50),
            league_id VARCHAR(50),
            roster_id INT,
            starters VARCHAR(700),
            players VARCHAR(1000),
            PRIMARY KEY (league_id, manager_id)
        );"""
        cursor = db.query(sql, args)
        
        # # nfl players table
        sql = """CREATE TABLE IF NOT EXISTS players(
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_id VARCHAR(20),
            position VARCHAR(10),
            team VARCHAR(5),
            first_name VARCHAR(20),
            last_name VARCHAR(30),
            full_name VARCHAR(50),
            fantasy_data_id VARCHAR(10),
            espn_id VARCHAR(10),
            yahoo_id VARCHAR(10)
        );"""
        cursor = db.query(sql, args)

    def importLeague(self, league_id = None):
        sleeper = SleeperAPI()
        league = sleeper.getLeague(league_id)        
        sql = """
            INSERT INTO leagues 
            (league_id, season, name)
            VALUES (%s, %s, %s)
            """
        args = (
            league['league_id'], 
            league['season'],
            league['name']
        )
        db = Database()
        newid = db.insert(sql, args)
        print(f"Imported league id: {league['league_id']}")

    def importLeagueManagers(self, league_id = None):
        sleeper = SleeperAPI()
        managers = sleeper.getLeagueManagers(league_id)
        sql = """
            INSERT INTO managers
            (user_id, display_name, team_name, league_id)
            VALUES
            (%s, %s, %s, %s)
            """
        args = []
        for manager in managers:
            display_name = manager["display_name"] if "display_name" in manager else manager["user_id"]
            team_name = manager['metadata']['team_name'] if "team_name" in manager['metadata'] else "Team " + display_name
            args.append((
                manager["user_id"], 
                display_name, 
                team_name, 
                manager["league_id"]
            ))
        db = Database()
        imported = db.insertmany(sql, args)
        print(f"Imported {imported} managers")

    def importLeagueRosters(self, league_id = None):
        sleeper = SleeperAPI()
        rosters = sleeper.getLeagueRosters(league_id)
        args = []
        for roster in rosters:
            starters = '|'.join(roster['starters'])
            players = '|'.join(roster["players"])
            args.append((
                roster["owner_id"], 
                roster["league_id"],
                roster["roster_id"],
                starters,
                players
            ))
        sql = """INSERT INTO rosters
            (manager_id, league_id, roster_id, starters, players)
            VALUES
            (%s, %s, %s, %s, %s)
            ;"""
        db = Database()
        imported = db.insertmany(sql, args)
        print(f"Imported {imported} rosters")

    def importPlayers(self, sport = None):
        sleeper = SleeperAPI()
        players = sleeper.getPlayers()
        args = []
        for key in players:
            player = players[key]
            if player["position"] in self.player_positions and player["team"] is not None:
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

        # # NFL Players INSERT
        sql = """INSERT INTO players
            (player_id, position, team, first_name, last_name, full_name, fantasy_data_id, espn_id, yahoo_id)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ;"""
        db = Database()
        imported = db.insertmany(sql, args)
        print(f"Imported {imported} rosters")
        