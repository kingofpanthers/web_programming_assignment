from django.shortcuts import render
from .models import Player

def home(request):
    return render(request, 'school/home.html', {'players': Player.objects.prefetch_related('positions').all()})
