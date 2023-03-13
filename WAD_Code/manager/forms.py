from django import forms
from manager.models import Team, Player, Match
from django.contrib.auth.models import User

#I'm pretty sure there was a forms API demonstrated in the lecture
#which cld handle all the form validation and creation for us

# class TeamForm(forms.ModelForm):
#     password = forms.CharField(widget=)

class TeamForm(forms.ModelForm):
    pass

class TeamProfileForm(forms.ModelForm):
    pass

class MatchRequestForm(forms.ModelForm):
    pass

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username","email","password",)

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ("age","location","bio","profile_pic")
        exclude = ("registered_team")

class LoginForm(forms.ModelForm):
    pass

class LogoutForm(forms.ModelForm):
    pass