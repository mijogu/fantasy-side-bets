from django.shortcuts import render

from .models import FantasyLeague

def home(request):
    leagues = FantasyLeague.objects.all()
    return render(request, 'home.html', { 'league' : leagues })