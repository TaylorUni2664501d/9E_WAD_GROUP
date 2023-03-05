from django.shortcuts import render
from django.http import HttpResponse
from manager.models import Team

# Create your views here.

#POINTS:
# - I think I've done a requirements file
# - why won't it import Team!!
# -  we probs need to have a slug on the teamname and playername properties

def index(request):
    context_dict = {}

    return render(request, 'manager/index.html', context=context_dict)

def leaderboard(request):
    team_list = Team.objects.order_by('win_rate')
    context_dict = {}
    context_dict['teams'] = team_list
    return render(request, 'manager/leaderboard.html', context=context_dict)

def view_team(request, team_name):
    context_dict = {}

    try:
        team = Team.objects.get(team_name = team_name)
        # context_dict['team'] = team
    except Team.DoesNotExist:
        context_dict['team'] = None

    return render(request, 'manager/view_team.html', context=context_dict)


