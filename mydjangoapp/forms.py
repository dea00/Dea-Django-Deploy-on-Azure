from django.forms import ModelForm
from django import forms
from .models import *
# from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import AuthUser
 
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
 
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
 
class LeagueForm(ModelForm):
    class Meta:
        model=Leagues
        fields= '__all__'
 
class TeamForm(ModelForm):
    class Meta:
        model=Teams
        fields= '__all__'
 
# Form for Players
class PlayerForm(ModelForm):
    class Meta:
        model = Players
        fields = '__all__'
 
# Form for Player Statistics
class PlayerStatisticsForm(ModelForm):
    class Meta:
        model = Playerstatistics
        fields = '__all__'
 
# Form for Matches
class MatchForm(ModelForm):
    class Meta:
        model = Matches
        fields = '__all__'
 
# Form for Trades
class TradeForm(forms.ModelForm):
    class Meta:
        model = Trades
        fields = '__all__'
        widgets = {
            'team1': forms.Select(attrs={'class': 'form-control'}),
            'team2': forms.Select(attrs={'class': 'form-control'}),
            'tradedplayer1': forms.Select(attrs={'class': 'form-control'}),
            'tradedplayer2': forms.Select(attrs={'class': 'form-control'}),
            'tradedate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
 
# Form for Drafts
class DraftForm(ModelForm):
    class Meta:
        model = Drafts
        fields = '__all__'
 
# Form for Waivers
class WaiverForm(ModelForm):
    class Meta:
        model = Waivers
        fields = '__all__'