import django_filters
from .models import *

class LeagueFilter(django_filters.FilterSet):
    class Meta:
        model = Leagues
        fields = '__all__'
         