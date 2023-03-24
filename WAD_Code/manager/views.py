from django.shortcuts import render
from django.http import HttpResponse
from manager.models import Team, Player
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from manager.decorators import user_teamless
from manager.forms import TeamForm, TeamProfileForm, MatchRequestForm, LoginForm, PlayerForm, UserForm, SearchForm, TeamRequestForm
from django.contrib.auth.models import User
# Create your views here.

#POINTS:
# - I think I've done a requirements file
# - why won't it import Team!! - FIXED
# -  we probs need to have a slug on the teamname and playername properties

def index(request):
    context_dict = {}
    top_teams = Team.objects.order_by('-win_rate')[:5]
    context_dict['teams'] = top_teams
    

    # Could be worth abstracting the logged in, and not logged in index pages to two seperate HTMLs -Stefan
    #if request.user.is_anonymous():
        # Logic for AnonymousUser (Not logged in)
        #pass
    #else:
        # Logic for User (Logged In)
        #pass

    return render(request, 'manager/index.html', context=context_dict)

def leaderboard(request):
    team_list = Team.objects.order_by('-win_rate')
    context_dict = {}
    context_dict['teams'] = team_list
    return render(request, 'manager/leaderboard.html', context=context_dict)

def view_team(request, team_name):
    context_dict = {}

    try:
        team = Team.objects.get(slug=team_name)
        context_dict['team'] = team
    except Team.DoesNotExist:
        context_dict['team'] = None
    if request.method == 'POST':
        user = request.user.id
        player = Player.objects.get(user_id=user)
        player.registered_team = team
        player.save()
        print("Changed team")
    return render(request, 'manager/view_team.html', context=context_dict)

def search_teams(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            return(search_results(request, search_form.cleaned_data['team_name'], search_form.cleaned_data['location_name']))
        else:
            print(search_form.errors)
    else:
        search_form = SearchForm()
    context_dict = {}
    context_dict['search_form'] = search_form
    return render(request, 'manager/search_teams.html', context = context_dict)
#should render a page with search box, wait for input and pass 
#the search term to search_results

def search_results(request, team_search, area_search):
    team_list = Team.objects.order_by('team_name')
    search_list = []
    for team in team_list:
        if (team_search.upper() in team.team_name.upper() and (area_search.upper() in team.team_name.upper())):
            search_list.append(team)
    context_dict = {}
    context_dict['teams'] = search_list
    context_dict['search'] = team_search + ' ' + area_search
    return render(request, 'manager/search_results.html', context = context_dict)
#recieves a search term from search_team and provides a
#list of teams that match that term


def signup_team(request):
    registered = False

    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        # team_profile_form = TeamProfileForm(request.POST)

        if team_form.is_valid() and team_form.is_valid():
            #team = team_form.save
            #team.set_password(team.password)
            team = team_form.save()

            # profile = team_profile_form(commit=False)
            # profile.team = team

            # Hey, sorry to step into your code, Im just making sure when a user makes a team, they automatically get added in -Stefan
            # current_player = Player.objects.get(username=request.user.username) - COMMENTED TO AVOID ERRORS UNTIL IMPLEMENTATION FIXED
            # current_player.registered_team = team 
            # end of added code

            #if 'logo' in request.FILEs: - BROKEN
            #    profile.logo = request.FILES

            #profile.save()
            registered = True

            # Stefan's User Perms Code, if you fix other stuff pls dont touch :)
            current_user = request.user
            # Global Perms
            #current_user.user_permissions.add('is_a_captain')
            #current_user.user_permissions.add('is_a_player')
            # End of User Perms Code

        else:
            print(team_form.errors)

    else:
        team_form = TeamForm()
        # team_profile_form = TeamProfileForm()
    return render(request, 'manager/register_team.html', context={"team_form":team_form, "registered": registered})

def add_player(user, age, location, bio):
    default = Team.objects.get_or_create(team_name='FA')[0]
    default.save()
    p = Player.objects.get_or_create(user=user, registered_team = default)[0]
    p.save()
    p.age = age
    p.location = location
    p.bio = bio
    p.save()

    return p

def signup_individual(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES)
        #player_form = PlayerForm(request.POST)
        if user_form.is_valid():
            
            cd = user_form.cleaned_data
            user = User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password']
            )
            user.save()
            player = add_player(user, user_form.cleaned_data['age'], user_form.cleaned_data['location'], user_form.cleaned_data['bio'])
            player.save()
            registered = True
            current_user = request.user
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'manager/register_individual.html', context={"user_form":user_form, "registered":registered})


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
                return redirect(reverse('manager:index'))
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
    pass # This will most likely be a form where you input a team name and a password
        # - all nessecary information should be accessible from the site 
        # - requesting user/player from login
        # - requested team by team site/slug/context dict
        # - date from system clock

# To be noted, while is_a_captain is under team, seemingly most documentations on this use the name of the folder the models are in instead
#@permission_required('manager.is_a_captain', raise_exception=True)
@login_required
def request_match(request, team_name):
    if request.method == 'POST':

        # Defining the player linked to the request of the user
        current_player = Player.objects.get(username=request.user.username)
        match_request_form = MatchRequestForm(request.POST)
        if match_request_form.is_valid():
            pass
        else:
            print(match_request_form.errors)
        # Defining the team, based on the team name listed in the player's data
        team = Team.objects.get(team_name=current_player.registered_team)
        
        #As the player must be a captain to access this, they logically must be the captain of the team theyre listed under
    else:
        match_request_form = MatchRequestForm()
    return render(request, 'manager/match_request.html', context={"match_request_form":match_request_form}) 

@login_required
def profile(request):
    return render(request, 'manager/profile.html')

def faq(request):
    return render(request, 'manager/faq.html')

def contact_us(request):
    return render(request, 'manager/contact.html')


# Custom decorator, checks if user in a team, please check manager/decorators.py for code





@user_teamless
@login_required
def create_team(request):
    pass

