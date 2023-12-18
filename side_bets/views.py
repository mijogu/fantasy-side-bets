from django.shortcuts import render
from .models.fantasy_manager import FantasyManager

def home(request):
    managers = FantasyManager.objects.all()
    return render(request, 'home.html', { 'managers' : managers })