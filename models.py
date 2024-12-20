# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
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

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
