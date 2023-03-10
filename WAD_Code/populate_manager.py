import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD_Code.settings')

import django
django.setup()
from manager.models import Player, Team, Match, Team_Request

def populate():
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
            print(select)
            if select not in player_choices:
                player_choices.append(select)
                players.remove(select)

        for player in player_choices: #add selected players to database connected to appropriate team
            add_player(player["forename"], player["surname"], player["age"], player["location"], player["bio"], t)

    #print added teams and players
    for t in Team.objects.all():
        print(f"NEW TEAM: {t}")
        print("Players:")
        for p in Player.objects.filter(registered_team=t):
            print(f"- {p}")
        print()
        

def add_player(forename,surname,age,location,bio,team):
    p = Player.objects.get_or_create(registered_team=team, forename=forename, surname=surname)[0]
    p.age = age
    p.location = location
    p.bio = bio
    p.save()

    return p

def add_team(name,location,age_range,win_rate,bio):
    t = Team.objects.get_or_create(team_name = name)[0]
    t.location = location
    t.age_range = age_range
    t.win_rate = win_rate
    t.bio = bio
    t.save()

    return t

if __name__ == "__main__":
    print("Starting manager population script...")
    populate()