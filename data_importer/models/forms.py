from django import forms 
from side_bets.models import FantasyLeague, FantasyTeam
from .sleeper import SleeperImporter, SleeperAPI

class ImportFantasyLeagueForm(forms.ModelForm):
    class Meta:
        model = FantasyLeague
        fields = ['league_id']
        widgets = {
            'league_id': forms.TextInput(
                attrs={
                    'placeholder': 'Enter sleeper league ID',
                },
                
            )
        }

    def save(self, commit=True):
        # don't commit yet because we need fields from sleeper
        instance = super(ImportFantasyLeagueForm, self).save(commit=False)

        # we know that league_id is valid / not in DB already
        sleeper = SleeperAPI()
        league = sleeper.getLeague(self.cleaned_data['league_id'])
        
        # TODO error handling 
        
        # add missing fields
        instance.name = league['name']
        instance.season_id = league['season']

        # save and commit
        instance.save()

        # return the saved instance
        return instance        

