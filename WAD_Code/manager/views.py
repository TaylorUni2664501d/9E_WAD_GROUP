from django.shortcuts import render
from django.http import HttpResponse
from models import Team
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

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


def signup_team(request):
    registered = False

    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        team_profile_form = TeamProfileForm(request.POST)

        if team_form.is_valid() and team_form.is_valid():
            team = team_form.save
            team.set_password(team.password)
            team.save()

            profile = team_profile_form(commit=False)
            profile.team = team

            if 'logo' in request.FILEs:
                profile.logo = request.FILES

            profile.save()
            registerd = True
        else:
            print(team_form.errors, team_profile_form.errors)

    else:
        team_form = TeamForm()
        team_profile_form = TeamProfileForm()
    return render(request, 'manager/register_team.htm', context={"team_form":team_form, "team_profile": team_profile_form, "registered": registered})

#both individual players and teams can login the same way i assume
#with just a username and password
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                #need to pass a slug of the username to this URL somehow
                return redirect(reverse('manager: individual_account'))
            else:
                return HttpResponse("Your Manager account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'manager/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('manager:index'))

@login_required
def join_team_request():
    pass

@login_required
def request_match():
    pass