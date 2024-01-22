from django.contrib import admin

from .models import FantasyLeague
from .models import FantasyTeam
from .models import FantasyRosterWeek

from .models import NFLSeason
from .models import NFLGame
from .models import NFLTeam
from .models import NFLPlayer
from .models import NFLBoxscore

# class NFLSeasonFilter(SimpleListFilter):
#     title = "NFL Season"
#     parameter_name = "nflseason"

#     def lookups(self, request, model_admin):
#         nflseasons = set([c.season for c in model_admin.model.objects.select_related('season').all()])
#         return [(c.id) for c in nflseasons]

#     def queryset(self, request, queryset):
#         if self.value():
#             try:
#                 season_id = int(self.value())
#             except (ValueError):
#                 return queryset.none()
#             else:
#                 return queryset.filter(season__id=season_id)


class NFLSeasonAdmin(admin.ModelAdmin):
    list_display = ( "id", "year", "are_games_imported", "number_of_games")
    list_filter = ("are_games_imported",)

class NFLGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'season',)
    list_filter = ('season__year',)
    search_fields = ("season__year",)

admin.site.register(FantasyLeague)
admin.site.register(FantasyTeam)
admin.site.register(FantasyRosterWeek)

admin.site.register(NFLTeam)
admin.site.register(NFLPlayer)
admin.site.register(NFLBoxscore)

admin.site.register(NFLSeason, NFLSeasonAdmin)
admin.site.register(NFLGame, NFLGameAdmin)






# 
# class ArtworkAdmin(ModelAdmin):
#     model = Artwork
#     list_filter = (ArtistFilter,)