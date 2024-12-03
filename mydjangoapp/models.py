from django.db import models
from datetime import datetime

# Create your models here.
class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define the primary key
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    USERNAME_FIELD = 'username'
    # profilesettings = models.JSONField(blank=True, null=True)
    def __str__(self):
        return self.username
    class Meta:
        managed = False
        db_table = 'auth_user'


class Drafts(models.Model):
    draft_id = models.AutoField(primary_key=True)
    league = models.ForeignKey('Leagues', models.DO_NOTHING, blank=True, null=True)
    draftdate = models.DateField(blank=True, null=True)
    draftorder = models.CharField(max_length=1, blank=True, null=True)
    draftstatus = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drafts'


class Leagues(models.Model):
    league_id = models.AutoField(primary_key=True)
    leaguename = models.CharField(max_length=30, blank=True, null=True)
    leaguetype = models.CharField(max_length=1, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    maxteams = models.DecimalField(max_digits=2, decimal_places=0)
    draftdate = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.leaguename
    class Meta:
        managed = False
        db_table = 'leagues'


class Matches(models.Model):
    match_id = models.AutoField(primary_key=True)
    team1 = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    team2 = models.ForeignKey('Teams', models.DO_NOTHING, related_name='matches_team2_set', blank=True, null=True)
    match_date = models.DateField(blank=True, null=True)
    finalscore = models.CharField(max_length=10, blank=True, null=True)
    winner = models.ForeignKey('Teams', models.DO_NOTHING, db_column='winner', related_name='matches_winner_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matches'


class Matchteams(models.Model):
    match = models.OneToOneField(Matches, models.DO_NOTHING, primary_key=True)  # The composite primary key (match_id, team_id) found, that is not supported. The first column is selected.
    team = models.ForeignKey('Teams', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'matchteams'
        unique_together = (('match', 'team'),)


class Players(models.Model):
    player_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    sport = models.CharField(max_length=3)
    playerposition = models.CharField(max_length=3, blank=True, null=True)
    realteam = models.CharField(max_length=50, blank=True, null=True)
    fantasypoints = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    availabilitystatus = models.CharField(max_length=1, blank=True, null=True)
    def __str__(self):
        return self.fullname
    class Meta:
        managed = False
        db_table = 'players'


class Playerstatistics(models.Model):
    statistic_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Players, models.DO_NOTHING, blank=True, null=True)
    gamedate = models.DateField(blank=True, null=True)
    performancestats = models.TextField(blank=True, null=True)
    injurystatus = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playerstatistics'


class Teams(models.Model):
    team_id = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=25)
    team_owner = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='team_owner', blank=True, null=True)
    league = models.ForeignKey(Leagues, models.DO_NOTHING, blank=True, null=True)
    totalpoints = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ranking = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    def __str__(self):
        return self.teamname
    class Meta:
        managed = False
        db_table = 'teams'


class Teamtrades(models.Model):
    trade = models.OneToOneField('Trades', models.DO_NOTHING, primary_key=True)  # The composite primary key (trade_id, team_id) found, that is not supported. The first column is selected.
    team = models.ForeignKey(Teams, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teamtrades'
        unique_together = (('trade', 'team'),)


class Teamwaivers(models.Model):
    waiver = models.OneToOneField('Waivers', models.DO_NOTHING, primary_key=True)  # The composite primary key (waiver_id, team_id) found, that is not supported. The first column is selected.
    team = models.ForeignKey(Teams, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teamwaivers'
        unique_together = (('waiver', 'team'),)


class Trades(models.Model):
    trade_id = models.AutoField(primary_key=True)
    team1 = models.ForeignKey(Teams, models.DO_NOTHING, blank=True, null=True)
    team2 = models.ForeignKey(Teams, models.DO_NOTHING, related_name='trades_team2_set', blank=True, null=True)
    tradedplayer1 = models.ForeignKey(Players, models.DO_NOTHING, blank=True, null=True)
    tradedplayer2 = models.ForeignKey(Players, models.DO_NOTHING, related_name='trades_tradedplayer2_set', blank=True, null=True)
    tradedate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trades'


class Waivers(models.Model):
    waiver_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Teams, models.DO_NOTHING, blank=True, null=True)
    player = models.ForeignKey(Players, models.DO_NOTHING, blank=True, null=True)
    waiverorder = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    waiverstatus = models.CharField(max_length=1, blank=True, null=True)
    waiverpickupdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waivers'


