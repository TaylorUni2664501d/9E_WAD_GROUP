from django import forms
from manager.models import Team, Player, Match
from django.contrib.auth.models import User

#I'm pretty sure there was a forms API demonstrated in the lecture
#which cld handle all the form validation and creation for us

# class TeamForm(forms.ModelForm):
#     password = forms.CharField(widget=)

class TeamForm(forms.ModelForm): # form to create a new team
    team_name = forms.CharField()
    team_password = forms.CharField(widget=forms.PasswordInput())
    # location = forms.CharField()
    # age_range = forms.IntegerField(widget=forms.NumberInput())
    age_min = forms.IntegerField(widget=forms.NumberInput(), min_value=13, max_value=50)
    age_max = forms.IntegerField(widget=forms.NumberInput(), min_value=13, max_value=50)
    # bio = forms.CharField(widget=forms.Textarea())

    logo = forms.ImageField(required=False)
    
    def save(self, commit=True):
        instance = super(TeamForm, self).save(commit=False)
        instance.age_range = f"{self.data['age_min']}-{self.data['age_max']}"
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Team
        fields = ("team_name","team_password", "location","age_range","bio")
        exclude = ("win_rate","gallery","age_range","slug",)

class TeamProfileForm(forms.ModelForm): # form to log in to a team as admin
    pass

class MatchRequestForm(forms.ModelForm): # form to create a new Match Request
    team_choices = ((team, str(team)) for team in Team.objects.all())
    team2 = forms.ChoiceField(choices=team_choices)

    date = forms.DateField()

    locations = ["Glasgow", "Stirling", "Edinburgh", "Cumbernauld", "Alloa", "Falkirk", "Queensferry", "Livingston", "Perth", "Kirkcaldy", "St Andrews", "Cupar", "Glenrothes", "Dundee", "Lanark", "Douglas", "Selkirk", "Jedburgh", "Haddington", "Dunfermline", "Ayr", "Aberdeen", "Durham", "Lockerbie", "Carlisle"]
    location_choices = ((location, location) for location in locations)
    pitch = forms.ChoiceField(choices=location_choices)
    class Meta:
        model = Match
        fields = ("team2", "date", "pitch") #should be within team 1's page, team1 gotten from there
        exclude = ("winner", "loser", "status")

class TeamRequestForm(forms.ModelForm): 
    pass

class UserForm(forms.ModelForm): # form to create a new user
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username","email","password",)

class PlayerForm(forms.ModelForm): # form to create a new player
    class Meta:
        model = Player
        fields = ("age","location","bio","profile_pic",)
        exclude = ("registered_team","user")

class LoginForm(forms.ModelForm): # form to log in a user
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("username", "password",)

class LogoutForm(forms.ModelForm):
    pass