from django import forms
from models import Team
from django.contrib.auth.models import User

#I'm pretty sure there was a forms API demonstrated in the lecture
#which cld handle all the form validation and creation for us

# class TeamForm(forms.ModelForm):
#     password = forms.CharField(widget=)