import graphene
from graphene_django import DjangoObjectType, DjangoListField
from side_bets.models import NFLPlayer, NFLTeam, NFLGame, NFLBoxscore, NFLSeason

class NFLPlayerType(DjangoObjectType):
    class Meta:
        model = NFLPlayer
        fields = ("id", "first_name", "last_name", "position", "team")

class NFLTeamType(DjangoObjectType):
    class Meta:
        model = NFLTeam
        fields = ("id", "city", "name", "conference", "division")

class NFLGameType(DjangoObjectType):
    class Meta: 
        model = NFLGame
        fields = ("id", "home_team", "away_team", "season")

class Query(graphene.ObjectType):
    # all_players = graphene.List(NFLPlayerType)
    all_players = graphene.Field(NFLPlayerType, id=graphene.Int())

    def resolve_all_players(root, info, id):
        # return NFLPlayer.objects.filter(position="QB")
        # return NFLPlayer.objects.all()
        return NFLPlayer.objects.get(pk=id)
    
    all_teams = graphene.List(NFLTeamType)
    def resolve_all_teams(root, info):
        return NFLTeam.objects.all()
    
    all_games = DjangoListField(NFLGameType)
    def resolve_all_games(root, info):
        return NFLGame.objects.all()
    


schema = graphene.Schema(query=Query)