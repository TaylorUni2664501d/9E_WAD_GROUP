from django.template.defaultfilters import slugify
import os
import random
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD_Code.settings')

import django
django.setup()
from manager.models import Player, Team, Match, Team_Request
from django.contrib.auth.models import User

def populate():
    locations = ["Glasgow", "Stirling", "Edinburgh", "Cumbernauld", "Alloa", "Falkirk", "Queensferry", "Livingston", "Perth", "Kirkcaldy", "St Andrews", "Cupar", "Glenrothes", "Dundee", "Lanark", "Douglas", "Selkirk", "Jedburgh", "Haddington", "Dunfermline", "Ayr", "Aberdeen", "Durham", "Lockerbie", "Carlisle"]
    with(open("population_data/players.txt",'r') as f):
        players = []
        for line in f:
            split = line.split(",")
            info = {"forename":split[0], "surname":split[1], "age":split[2], "location":split[3], "bio":split[4]}
            players.append(info)
        
    with(open("population_data/teams.txt",'r') as f):
        teams = []
        for line in f:
            split = line.split(",")
            info = {"name":split[0], "location":split[1], "age_range":split[2], "win_rate":split[3], "bio":split[4]}
            teams.append(info)

    for team in teams:
        t = add_team(team["name"], team["location"], team["age_range"], team["win_rate"], team["bio"])
        print(f"added team {t}")
        player_choices = []
        selection_range = min(len(players), random.randint(6,9)) #numbers selected to have no or few orphan players 200/23 = 8.6
        print(f"selected {selection_range} players")
        for i in range(selection_range): #select players to be in the team and removes them from the selection pool
            select = random.choice(players)
            if select not in player_choices:
                player_choices.append(select)
                players.remove(select)

        for player in player_choices: #add selected players to database connected to appropriate team
            u = add_user(player["forename"], player["surname"], player["age"]) #make user based off player info
            add_player(u, player["age"], player["location"], player["bio"], t)

    #Make some match requests - not every team will have a match
    max = 9
    i = 0
    for t in Team.objects.all():
        if i <= max:
            matched_teams = []
            if t not in matched_teams:
                opposition = random.choice(Team.objects.all())
                while opposition in matched_teams:
                    opposition = random.choice(Team.objects.all())
                
                add_match(t, opposition, locations)
                matched_teams.append(t)
                matched_teams.append(opposition)
                i += 1

    #print added teams and players
    for t in Team.objects.all():
        print(f"NEW TEAM: {t}")
        print("Players:")
        for p in Player.objects.filter(registered_team=t):
            print(f"- {p} \t attached user: {p.user}")
        print()

    for m in Match.objects.all():
        print(f"NEW MATCH: {m}")
        

def add_player(user, age, location, bio, team):
    p = Player.objects.get_or_create(user=user, registered_team=team)[0]
    p.age = age
    p.location = location
    p.bio = bio
    p.save()

    return p

def add_user(forename, surname, age):
    try:
        u = User.objects.create_user(username=f"{forename}{surname[:2]}_{age}", email=f"{forename}.{surname}{age}@email.com", password=f"{forename}{age}password")
    except:
        u = User.objects.create_user(username=f"{forename}{surname[:2]}_{age}_{random.randint(0,9999)}", email=f"{forename}.{surname}{age}@email.com", password=f"{forename}{age}password")

    u.first_name = forename
    u.last_name = surname

    u.save()

    return u

def add_team(name,location,age_range,win_rate,bio):
    t = Team.objects.get_or_create(team_name = name, team_password=hash(f"{slugify(name)}_Password"))[0]
    t.location = location
    t.age_range = age_range
    t.win_rate = win_rate
    t.bio = bio
    t.save()

    return t

def add_match(team1, team2, locations):
    date = make_date()
    m = Match.objects.get_or_create(team1=team1, team2=team2, date=date, pitch=random.choice(locations))[0]

def make_date():
    return datetime.date(random.randint(2022,2026), random.randint(1,12), random.randint(1,28))

if __name__ == "__main__":
    print("Starting manager population script...")
    populate()