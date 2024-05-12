import requests 
import json 
from decouple import config
from datetime import time, datetime

from side_bets.models import \
    NFLBoxscore, NFLGame, NFLPlayer, NFLTeam

class TankStatsAPI():
    use_json_server = True
    season = '2023'

    def __init__(self):
        self.host = config('RAPID_API_HOST')
        self.apikey = config('RAPID_API_KEY')

        self.headers = {
            "X-RapidAPI-Key": self.apikey,
            "X-RapidAPI-Host": self.host
        }

        if self.use_json_server:
            self.url = "http://localhost:3000"
        else:
            self.url = "https://" + self.host

    def getGameBoxScores(self, game_id, fantasy_points = "false"):
        # "twoPointConversions":"2",
        # "passYards":".04",
        # "passAttempts":"0",
        # "passTD":"4",
        # "passCompletions":"0",
        # "passInterceptions":"-2",
        # "pointsPerReception":".5",
        # "carries":".2",
        # "rushYards":".1",
        # "rushTD":"6",
        # "fumbles":"-2",
        # "receivingYards":".1",
        # "receivingTD":"6",
        # "targets":"0",
        # "defTD":"6"     
        args = {
            "gameID": game_id, # REQUIRED
            "fantasyPoints": fantasy_points
        }
        request = requests.get(f"{self.url}/getNFLBoxScore", headers=self.headers, params=args)
        return request.json()

    def getScheduleGames(self, week = 'all', season = season, season_type = 'reg'):
        # seasonType = pre, post, reg, or all
        args = {
            "week": week,
            "season": season,
            "seasonType": season_type
        }
        request = requests.get(f"{self.url}/getNFLGamesForWeek", headers=self.headers, params=args)        
        return request.json()


class TankStatsImporter():    
    def __init__(self):
        pass

    # TODO is 'all' working correctly?
    @staticmethod
    def importNFLGames(week = None, season = None, season_type = None):
        if week is None or season is None:
            return False 
        
        tankstats = TankStatsAPI()
        games = tankstats.getScheduleGames(week=week, season=season)
        
        game_ids = NFLGame.objects.filter(season_id=season).values_list('id', flat=True)
        new_games = []
        for game in games["body"]:
            # skip if game ID is already found in db
            if game["gameID"] not in game_ids:
                try:
                    new_games.append(NFLGame(                    
                        id = game["gameID"],
                        away_team_id = NFLTeam.cleanAbbreviation(game["away"]),
                        home_team_id = NFLTeam.cleanAbbreviation(game["home"]),
                        date = game["gameDate"],
                        time = game["gameTime"],
                        week = int(game["gameWeek"].replace('Week ', '')),
                        # season = int(game["season"]),
                        season_id = season,
                    ))
                except Exception as exception:
                    print(f"{exception}")
                    print("...from the following data...")
                    print(json.dumps(game))
            else:
                print(f"NFLGame {game['gameID']} already exists")
        games_imported = NFLGame.objects.bulk_create(new_games) 
        print(f"Imported {len(games_imported)} games")
        return games_imported

    # game_id required
    @staticmethod
    def importBoxScores(game_id):
        tankstats = TankStatsAPI()
        game_result = tankstats.getGameBoxScores(game_id=game_id, fantasy_points="false")
        
        # playerStats = game_result["body"]["playerStats"]
        # for playerID in playerStats:
        #     try:
        #         plyr = NFLPlayer.objects.get(espn_id=playerID)
        #         print(playerID)
        #     except Exception as e:
        #         print(playerID, e)
        # exit()

        boxscores = [] 
        playerStats = game_result["body"]["playerStats"]
        for playerID in playerStats:
            player = playerStats[playerID]
            hasRelevantStats = False
            try:
                newboxscore = NFLBoxscore(
                    player_id=player["playerID"],
                    game_id=player["gameID"],
                )
                if "Rushing" in player:
                    hasRelevantStats = True                    
                    newboxscore.rush_tds=int(player["Rushing"]["rushTD"])
                    newboxscore.rush_yards=int(player["Rushing"]["rushYds"])
                    newboxscore.carries=int(player["Rushing"]["carries"])
                # else: 
                #     newboxscore.extend([0, 0, 0])
                if "Passing" in player:
                    hasRelevantStats = True
                    newboxscore.passing_tds=int(player["Passing"]["passTD"])
                    newboxscore.passing_yards=int(player["Passing"]["passYds"])
                    newboxscore.passing_completions=int(player["Passing"]["passCompletions"])
                    newboxscore.passing_ints=int(player["Passing"]["int"])
                # else: 
                #     newboxscore.extend([0, 0, 0, 0])
                if "Receiving" in player:
                    hasRelevantStats = True
                    newboxscore.receiving_tds=int(player["Receiving"]["recTD"])
                    newboxscore.receiving_yards=int(player["Receiving"]["recYds"])
                    newboxscore.receptions=int(player["Receiving"]["receptions"])
                    newboxscore.targets=int(player["Receiving"]["targets"])
                # else:
                #     newboxscore.extend([0, 0, 0, 0])
                if "Defense" in player:
                    newboxscore.fumbles=int(player["Defense"]["fumbles"]) if "fumbles" in player["Defense"] else 0
                    newboxscore.fumbles_lost=int(player["Defense"]["fumblesLost"]) if "fumblesLost" in player["Defense"] else 0
                # else: 
                #     newboxscore.extend([0, 0])
                if hasRelevantStats:
                    boxscores.append(newboxscore)

            except KeyError as error:
                print(f"Key error for '{error}'")
            except Exception as exception:
                print(f"{exception}")
                print("...from the following data...")
                print(json.dumps(player))

        boxscores_imported = NFLBoxscore.objects.bulk_create(boxscores) 
        
        # TODO confirm this works
        fields_updated = NFLGame.objects.filter(id=game_id).update(
            away_score=game_result['body']['awayPts'],
            away_result=game_result['body']['awayResult'],
            home_score=game_result['body']['homePts'],
            home_result=game_result['body']['homeResult'],
            are_scores_imported=True,
        )

        print(f"Imported {len(boxscores_imported)} boxscores")
        print(f"Updated {fields_updated} NFLGame fields")

