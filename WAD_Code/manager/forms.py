from django import forms
from manager.models import Team, Player, Match
from django.contrib.auth.models import User

#I'm pretty sure there was a forms API demonstrated in the lecture
#which cld handle all the form validation and creation for us

# class TeamForm(forms.ModelForm):
#     password = forms.CharField(widget=)

class TeamForm(forms.ModelForm):
    # team_name = forms.CharField()
    # location = forms.CharField()
    # age_range = forms.IntegerField(widget=forms.NumberInput()) - FIX NUMBER INPUT - TWO NUM INPUTS MIN-MAX
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
        fields = ("team_name","location","age_range","bio")
        exclude = ("win_rate","gallery","age_range","slug",)

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
        fields = ("age","location","bio","profile_pic",)
        exclude = ("registered_team",)

class LoginForm(forms.ModelForm):
    pass

class LogoutForm(forms.ModelForm):
    pass