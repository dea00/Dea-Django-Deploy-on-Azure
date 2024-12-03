from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse
from django.contrib.auth.models import Group
 
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import *
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth. decorators import login_required

from django.db import IntegrityError

 
from .filters import LeagueFilter
 
from django.contrib import messages

 
# def dashboard(request):
#     leagues = Leagues.objects.filter(user=request.user)  # Leagues owned by the user
#     teams = Teams.objects.filter(team_owner=request.user)  # Teams owned by the user
#     waivers = Waivers.objects.filter(team__team_owner=request.user)  # Waivers related to user's teams
#     drafts = Drafts.objects.filter(league__user=request.user)  # Drafts related to user's leagues
#     trades = Trades.objects.filter(
#         team1__team_owner=request.user
#     ) | Trades.objects.filter(
#         team2__team_owner=request.user
#     )  # Trades where the user owns either team1 or team2
 
#     context = {
#         'leagues': leagues,
#         'teams': teams,
#         'waivers': waivers,
#         'drafts': drafts,
#         'trades': trades,
#     }
#     return render(request, 'index.html', context)
 
from django.db import connection
 
def execute_query(query, params):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
 
def get_user_data(request):
    user_id = request.user.id  # Get the logged-in user's ID
 
    # SQL queries
    leagues_query = "SELECT * FROM leagues WHERE user_id = %s"
    teams_query = "SELECT * FROM teams WHERE team_owner = %s"
    waivers_query = """
        SELECT waivers.* FROM waivers
        JOIN teams ON waivers.team_id = teams.team_id
        WHERE teams.team_owner = %s
    """
    drafts_query = """
        SELECT drafts.* FROM drafts
        JOIN leagues ON drafts.league_id = leagues.league_id
        WHERE leagues.user_id = %s
    """
    trades_query = """
        SELECT trades.* FROM trades
        WHERE trades.team1_id IN (SELECT team_id FROM teams WHERE team_owner = %s)
        OR trades.team2_id IN (SELECT team_id FROM teams WHERE team_owner = %s)
    """
 
    # Execute queries
    leagues = execute_query(leagues_query, [user_id])
    teams = execute_query(teams_query, [user_id])
    waivers = execute_query(waivers_query, [user_id])
    drafts = execute_query(drafts_query, [user_id])
    trades = execute_query(trades_query, [user_id, user_id])
 
    context = {
        'leagues': leagues,
        'teams': teams,
        'waivers': waivers,
        'drafts': drafts,
        'trades': trades,
    }
 
    return render(request, 'mydjangoapp/dashboard.html', context) 





@unauthenticated_user
def register_view(request):
    # form = CreateUserForm()
    if request.method  == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username =form.cleaned_data.get('username')
           
            group = Group.objects.get(name='just user')
            user.groups.add(group)
 
            messages.success(request, 'Account was sucessfully created for '+ username)
            return redirect('login')
    else:
        form = CreateUserForm()
 
    context = {'form':form}
    return render(request, 'mydjangoapp/register.html', context)
 
@unauthenticated_user
def loginPage(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
 
        user = authenticate(request, username=username, password=password)
 
        if user is not None:
            if user.is_superuser:  # Check if the user is an admin
                return redirect('/admin/')
            else:
                login(request, user)
                # Correctly returning after login
                return redirect(reverse('users', args=[request.user.id]))
        else:
            messages.error(request, 'Username or password is incorrect')
 
    context = {}
    return render(request, 'mydjangoapp/login.html', context)
 
def logoutUser(request):
    logout(request)
    return redirect('login')
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def index(request):
    users = AuthUser.objects.all()
    context={
        'users': users
    }
    return render(request, 'mydjangoapp/index.html', context)
 
@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, 'mydjangoapp/main.html')
 
@login_required(login_url='login')
def about(request):
    return render(request, 'mydjangoapp/about.html')
 
@login_required(login_url='login')
def drafts(request):
    drafts = Drafts.objects.all()
    context={
        'drafts': drafts
    }
    return render(request, 'mydjangoapp/drafts.html', context)


def viewLogs(request):
    try:
        with connection.cursor() as cursor:
            # Fetch the most recent logs
            cursor.execute("SELECT action_time, message FROM deletion_logs ORDER BY action_time DESC")
            logs = cursor.fetchall()
        return render(request, 'mydjangoapp/viewLogs.html', {'logs': logs})
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
    

@login_required(login_url='login')
def createDraft(request):
    form = DraftForm()
    if request.method == 'POST':
        form = DraftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('users', args=[request.user.id]))  # Redirect to the drafts page after successful creation
    context = {'form': form}
    return render(request, 'mydjangoapp/createDraft.html', context)
 
 
@login_required(login_url='login')
def leagues(request):
    leagues = Leagues.objects.all()
    context={
        'leagues': leagues
    }
    return render(request, 'mydjangoapp/leagues.html', context)
 
@login_required(login_url='login')
# def createLeague(request):
#     form = LeagueForm()
#     if request.method == 'POST':
#         # print('Printing POST:', request.POST)
#         form = LeagueForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('users', args=[request.user.id]))
#     context={'form':form}
#     return render(request, 'mydjangoapp/createLeague.html', context)

@login_required
def createLeague(request):
    if request.method == 'POST':
        # Retrieve the form data
        leaguename = request.POST.get('leaguename')
        maxteams = request.POST.get('maxteams')
        user_id = request.user.id  # Always set the logged-in user as the owner
        draftdate = request.POST.get('draftdate')
        leaguetype = request.POST.get('leaguetype')

        # Insert the data using raw SQL
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO leagues (leaguename, maxteams, user_id, draftdate, leaguetype)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [leaguename, maxteams, user_id, draftdate, leaguetype]
            )
        return redirect('leagues')

    # Pass the current user to the template for the dropdown
    context = {'users': [request.user]}
    return render(request, 'mydjangoapp/createLeague.html', context)


@login_required
def createTeam(request):
    if request.method == 'POST':
        # Retrieve the form data
        teamname = request.POST.get('teamname')
        team_owner = request.user.id  # Automatically set the logged-in user as the owner
        league = request.POST.get('league')
        totalpoints = request.POST.get('totalpoints')
        ranking = request.POST.get('ranking')
        status = request.POST.get('status')

        # Insert the data using raw SQL
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO teams (teamname, team_owner, league_id, totalpoints, ranking, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [teamname, team_owner, league, totalpoints, ranking, status]
            )
        return redirect(reverse('users', args=[request.user.id]))

    # Filter leagues to show only those belonging to the logged-in user
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT league_id, leaguename FROM leagues WHERE user_id = %s
            """,
            [request.user.id]
        )
        leagues = cursor.fetchall()

    context = {
        'leagues': leagues,
        'users': [request.user],  # Restrict the dropdown to the logged-in user
    }
    return render(request, 'mydjangoapp/createTeam.html', context)

 
# @login_required(login_url='login')
# def createTeam(request):
#     form = TeamForm()
#     if request.method == 'POST':
#         form = TeamForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('teams')  # Redirect to the teams page after successful creation
#     context = {'form': form}
#     return render(request, 'mydjangoapp/createTeam.html', context)
 
 
@login_required(login_url='login')
# def updateLeague(request, pk):
#     league = Leagues.objects.get(league_id=pk)  # Fetch the league to be updated
#     form = LeagueForm(instance=league)  # Pre-fill the form with the current league data
 
#     if request.method == 'POST':
#         form = LeagueForm(request.POST, instance=league)  # Use LeagueForm to handle the POST data
#         if form.is_valid():
#             form.save()  # Save the updated data to the database
#             return redirect('/')  # Redirect to the homepage (or any desired page)
       
#     context = {'form': form}
#     return render(request, 'mydjangoapp/createLeague.html', context)

def updateLeague(request, pk):
    if request.method == 'POST':
        leaguename = request.POST.get('leaguename')
        leaguetype = request.POST.get('leaguetype')
        maxteams = request.POST.get('maxteams')
        draftdate = request.POST.get('draftdate')
        user_id = request.POST.get('user')
 
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE leagues
                    SET leaguename = %s, leaguetype = %s, maxteams = %s, draftdate = %s, user_id = %s
                    WHERE league_id = %s
                """, [leaguename, leaguetype, maxteams, draftdate, user_id, pk])
            return redirect('leagues')
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
 
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM leagues WHERE league_id = %s", [pk])
            league = dictfetchone(cursor)  # Helper function for fetching one result as a dictionary
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
 
    users = AuthUser.objects.all()
    return render(request, 'mydjangoapp/updateLeague.html', {'league': league, 'users': users})
    
def updateTeam(request, pk):
    team = Teams.objects.get(team_id=pk)  # Fetch the team to be updated
    form = TeamForm(instance=team)  # Pre-fill the form with the current team data
 
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)  # Handle POST data with TeamForm
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('teams')  # Redirect to the teams page
 
    context = {'form': form}
    return render(request, 'mydjangoapp/createTeam.html', context)
 
def updateMatch(request, pk):
    match = Matches.objects.get(match_id=pk)  # Fetch the match to be updated
    form = MatchForm(instance=match)  # Pre-fill the form with the current match data
 
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)  # Handle POST data with MatchForm
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('matches')  # Redirect to the matches page
 
    context = {'form': form}
    return render(request, 'mydjangoapp/createMatch.html', context)
 
 
def updateDraft(request, pk):
    draft = Drafts.objects.get(draft_id=pk)  # Fetch the draft to be updated
    form = DraftForm(instance=draft)  # Pre-fill the form with the current draft data
 
    if request.method == 'POST':
        form = DraftForm(request.POST, instance=draft)  # Handle POST data with DraftForm
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('drafts')  # Redirect to the drafts page
 
    context = {'form': form}
    return render(request, 'mydjangoapp/createDraft.html', context)
 
def updateTrade(request, pk):
    trade = Trades.objects.get(trade_id=pk)  # Fetch the trade to be updated
    form = TradeForm(instance=trade)  # Pre-fill the form with the current trade data
 
    if request.method == 'POST':
        form = TradeForm(request.POST, instance=trade)  # Handle POST data with TradeForm
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('trades')  # Redirect to the trades page
 
    context = {'form': form}
    return render(request, 'mydjangoapp/createTrade.html', context)
 
def updateWaiver(request, pk):
    waiver = Waivers.objects.get(waiver_id=pk)  # Fetch the waiver to be updated
    form = WaiverForm(instance=waiver)  # Pre-fill the form with the current waiver data
 
    if request.method == 'POST':
        form = WaiverForm(request.POST, instance=waiver)  # Handle POST data with WaiverForm
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('waivers')  # Redirect to the waivers page
 
    context = {'form': form}
    return render(request, 'mydjangoapp/createWaiver.html', context)
 
def updatePlayer(request, pk):
    player = Players.objects.get(player_id=pk)  # Fetch the player to be updated
    form = PlayerForm(instance=player)  # Pre-fill the form with the current player data
 
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)  # Handle POST data with PlayerForm
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('players')  # Redirect to the players page
 
    context = {'form': form}
    return render(request, 'mydjangoapp/createPlayer.html', context)
 
def updatePlayerStatistic(request, pk):
    statistic = Playerstatistics.objects.get(statistic_id=pk)  # Fetch the player statistic to be updated
    form = PlayerStatisticsForm(instance=statistic)  # Pre-fill the form with the current player statistic data
 
    if request.method == 'POST':
        form = PlayerStatisticsForm(request.POST, instance=statistic)  # Handle POST data with PlayerStatisticForm
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('player_statistics')  # Redirect to the player statistics page
 
    context = {'form': form}
    return render(request, 'mydjangoapp/createPlayerStatistic.html', context)
 
@login_required(login_url='login')
# def deleteLeague(request, pk):
#     league = Leagues.objects.get(league_id=pk)
#     if request.method== 'POST':
#         league.delete()
#         return redirect(reverse('users', args=[request.user.id]))
#     context={'item': league}
#     return render(request, 'mydjangoapp/deleteLeague.html', context)

def deleteLeague(request, pk):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM leagues WHERE league_id = %s", [pk])
            return redirect('leagues')
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
 
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT leaguename FROM leagues WHERE league_id = %s", [pk])
            league = cursor.fetchone()
            if league:
                league = {'leaguename': league[0]}
            else:
                return HttpResponse("League not found.")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
 
    return render(request, 'mydjangoapp/deleteLeague.html', {'league': league})
 
def dictfetchone(cursor):
    """Return a single row from a cursor as a dict"""
    desc = cursor.description
    row = cursor.fetchone()
    if row is None:
        return None
    return {desc[i][0]: value for i, value in enumerate(row)}
 
# @login_required(login_url='login')
def matches(request):
    matches = Matches.objects.all()
    context={
        'matches': matches
    }   
    return render(request, 'mydjangoapp/matches.html', context)
 
@login_required(login_url='login')
@unauthenticated_user
def createMatch(request):
    form = MatchForm()
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('matches')  # Redirect to the matches page after successful creation
    context = {'form': form}
    return render(request, 'mydjangoapp/createMatch.html', context)
 
 
# @login_required(login_url='login')
def match_teams(request):
    match_teams = Matchteams.objects.all()
    return render(request, 'mydjangoapp/match_teams.html')
 
@login_required(login_url='login')
def players(request):
    players = Players.objects.all()
    context={
        'players': players
    }
    return render(request, 'mydjangoapp/players.html', context)
 
# @login_required(login_url='login')
# def createPlayer(request):
#     form = PlayerForm()
#     if request.method == 'POST':
#         form = PlayerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('players')  # Redirect to the players page after successful creation
#     context = {'form': form}
#     return render(request, 'mydjangoapp/createPlayer.html', context)

def createPlayer(request):
    form = PlayerForm()
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Player created successfully!')
                return redirect('players')  # Redirect to the players page after successful creation
        except IntegrityError as e:
            # Extract the error message and add it to Django messages
            messages.error(request, f"Database error: {str(e)}")
    context = {'form': form}
    return render(request, 'mydjangoapp/createPlayer.html', context)
 
 
# @login_required(login_url='login')
def player_statistics(request):
    player_statistics = Playerstatistics.objects.all()
    context={
        'player_statistics': player_statistics
    }
    return render(request, 'mydjangoapp/player_statistics.html', context)

 
@login_required(login_url='login')
def createPlayerStatistics(request):
    form = PlayerStatisticsForm()
    if request.method == 'POST':
        form = PlayerStatisticsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_statistics')  # Redirect to the player statistics page
    context = {'form': form}
    return render(request, 'mydjangoapp/createPlayerStatistics.html', context)
 
 
# @login_required(login_url='login')
def teams(request):
    teams = Teams.objects.all()
    context={
        'teams': teams
    }
    return render(request, 'mydjangoapp/teams.html', context)
 
 
# @login_required(login_url='login')
def team_trades(request):
    team_trades = Teamtrades.objects.all()
    return render(request, 'mydjangoapp/team_trades.html')
 
# @login_required(login_url='login')
def team_waivers(request):
    team_waivers = Teamwaivers.objects.all()
    return render(request, 'mydjangoapp/team_waivers.html')
 
# @login_required(login_url='login')
def trades(request):
    trades = Trades.objects.all()
    context={
        'trades': trades
    }
    return render(request, 'mydjangoapp/trades.html', context)
 
@login_required(login_url='login')
def createTrade(request):
    form = TradeForm()
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('users', args=[request.user.id])) # Redirect to the trades page
    context = {'form': form}
    return render(request, 'mydjangoapp/createTrade.html', context)
 
 
@login_required(login_url='login')
# def users(request, pk_test):
#     try:
#         # Fetch the specific user by ID
#         user = AuthUser.objects.get(id=pk_test)
#     except AuthUser.DoesNotExist:
#         messages.error(request, "User not found.")
#         return redirect('home')
 
#     # Use the reverse relationship to fetch leagues related to the user
#     leagues = user.leagues_set.all()  # Django's default reverse relation name
#     leagues_count = leagues.count()
 
#     teams = Teams.objects.filter(team_owner=user.id)  # Assuming Teams has user_id field
#     teams_count = teams.count()
 
#     myFilter = LeagueFilter(request.GET, queryset=leagues)
#     leagues = myFilter.qs
 
#     context = {
#         'user': user,
#         'leagues': leagues,
#         'teams': teams,
#         'leagues_count': leagues_count,
#         'teams_count': teams_count,
#         'myFilter': myFilter,
#     }
 
#     return render(request, 'mydjangoapp/users.html', context)

def users(request, pk_test):
    try:
        # Fetch the specific user by ID
        user = AuthUser.objects.get(id=pk_test)
    except AuthUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('home')
 
    # Fetch leagues and teams related to the user
    leagues = user.leagues_set.all()
    leagues_count = leagues.count()
 
    teams = Teams.objects.filter(team_owner=user.id)
    teams_count = teams.count()
 
    # Fetch waivers related to the user's teams using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                w.waiver_id, 
                t.teamname AS team_name, 
                p.fullname AS player_name, 
                w.waiverorder, 
                w.waiverstatus, 
                w.waiverpickupdate
            FROM waivers w
            INNER JOIN teams t ON w.team_id = t.team_id
            INNER JOIN players p ON w.player_id = p.player_id
            WHERE t.team_owner = %s
        """, [user.id])
        waivers = cursor.fetchall()

    waivers_data = [
        {
            'waiver_id': row[0],
            'team_name': row[1],
            'player_name': row[2],
            'waiverorder': row[3],
            'waiverstatus': row[4],
            'waiverpickupdate': row[5],
        }
        for row in waivers
    ]

 
    # Fetch trades related to the user's teams using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                tr.trade_id, 
                t1.teamname AS team1_name, 
                t2.teamname AS team2_name, 
                p1.fullname AS player1_name, 
                p2.fullname AS player2_name, 
                tr.tradedate
            FROM trades tr
            INNER JOIN teams t1 ON tr.team1_id = t1.team_id
            INNER JOIN teams t2 ON tr.team2_id = t2.team_id
            INNER JOIN players p1 ON tr.tradedplayer1_id = p1.player_id
            INNER JOIN players p2 ON tr.tradedplayer2_id = p2.player_id
            WHERE t1.team_owner = %s OR t2.team_owner = %s
        """, [user.id, user.id])
        trades = cursor.fetchall()

    # Process fetched data into a structured format
    trades_data = [
        {
            'trade_id': row[0],
            'team1_name': row[1],
            'team2_name': row[2],
            'player1_name': row[3],
            'player2_name': row[4],
            'tradedate': row[5],
        }
        for row in trades
    ]

 
    # Fetch drafts related to the user's leagues using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT d.draft_id, d.league_id, d.draftdate, d.draftorder, d.draftstatus
            FROM drafts d
            INNER JOIN leagues l ON d.league_id = l.league_id
            WHERE l.user_id = %s
        """, [user.id])
        drafts = cursor.fetchall()
 
    drafts_data = [
        {
            'draft_id': row[0],
            'league_id': row[1],
            'draftdate': row[2],
            'draftorder': row[3],
            'draftstatus': row[4],
        }
        for row in drafts
    ]
 
    # Apply filter for leagues
    myFilter = LeagueFilter(request.GET, queryset=leagues)
    leagues = myFilter.qs
 
    context = {
        'user': user,
        'leagues': leagues,
        'teams': teams,
        'waivers': waivers_data,
        'trades': trades_data,
        'drafts': drafts_data,
        'leagues_count': leagues_count,
        'teams_count': teams_count,
        'myFilter': myFilter,
    }
 
    return render(request, 'mydjangoapp/users.html', context)

 
 
# @login_required(login_url='login')
def waivers(request):
    waivers = Waivers.objects.all()
    context={
        'waivers': waivers
    }
    return render(request, 'mydjangoapp/waivers.html', context)
 
@login_required(login_url='login')
# def createWaiver(request):
#     form = WaiverForm()
#     if request.method == 'POST':
#         form = WaiverForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('users', args=[request.user.id]))  # Redirect to the waivers page
#     context = {'form': form}
#     return render(request, 'mydjangoapp/createWaiver.html', context)
 
def createWaiver(request):
    if request.method == 'POST':
        # Retrieve the form data
        team_id = request.POST.get('team')  # Team dropdown selection
        player_id = request.POST.get('player')  # Player dropdown selection
        waiverorder = request.POST.get('waiverorder')
        waiverstatus = request.POST.get('waiverstatus')
        waiverpickupdate = request.POST.get('waiverpickupdate')

        # Insert the data into the waivers table using raw SQL
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO waivers (team_id, player_id, waiverorder, waiverstatus, waiverpickupdate)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [team_id, player_id, waiverorder, waiverstatus, waiverpickupdate]
            )
        return redirect(reverse('users', args=[request.user.id]))

    # Fetch all teams where the logged-in user is the owner
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT team_id, teamname FROM teams WHERE team_owner = %s
            """,
            [request.user.id]
        )
        teams = cursor.fetchall()

    # Fetch all available players
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT player_id, fullname FROM players
            """
        )
        players = cursor.fetchall()

    context = {
        'teams': teams,  # Teams belonging to the logged-in user
        'players': players,  # All players available in the database
    }
    return render(request, 'mydjangoapp/createWaiver.html', context)


# def loginPage(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)  # Assume you have a LoginForm in forms.py
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')  # Redirect to index after successful login
#             else:
#                 form.add_error(None, "Invalid username or password")
#     else:
#         form = LoginForm()
 
#     return render(request, 'mydjangoapp/login.html', {'form': form})

def deleteTeam(request, pk):
    team = Teams.objects.get(team_id=pk)
    if request.method == 'POST':
        team.delete()
        return redirect(reverse('users', args=[request.user.id]))
    context = {'item': team}
    return render(request, 'mydjangoapp/deleteTeam.html', context)

 
def deleteMatch(request, pk):
    match = Matches.objects.get(match_id=pk)
    if request.method == 'POST':
        match.delete()
        return redirect('matches')  # Redirect to the matches page
    context = {'item': match}
    return render(request, 'mydjangoapp/deleteMatch.html', context)
 
def deleteTrade(request, pk):
    trade = Trades.objects.get(trade_id=pk)
    if request.method == 'POST':
        trade.delete()
        return redirect('trades')  # Redirect to the trades page
    context = {'item': trade}
    return render(request, 'mydjangoapp/deleteTrade.html', context)
 
def deleteDraft(request, pk):
    draft = Drafts.objects.get(draft_id=pk)
    if request.method == 'POST':
        draft.delete()
        return redirect('drafts')  # Redirect to the drafts page
    context = {'item': draft}
    return render(request, 'mydjangoapp/deleteDraft.html', context)
 
def deleteWaiver(request, pk):
    waiver = Waivers.objects.get(waiver_id=pk)
    if request.method == 'POST':
        waiver.delete()
        return redirect('waivers')  # Redirect to the waivers page
    context = {'item': waiver}
    return render(request, 'mydjangoapp/deleteWaivers.html', context)
 
def deletePlayer(request, pk):
    player = Players.objects.get(player_id=pk)
    if request.method == 'POST':
        player.delete()
        return redirect('players')  # Redirect to the players page
    context = {'item': player}
    return render(request, 'mydjangoapp/deletePlayer.html', context)
 
def deletePlayerStatistics(request, pk):
    player_statistic = Playerstatistics.objects.get(statistic_id=pk)
    if request.method == 'POST':
        player_statistic.delete()
        return redirect('player_statistics')  # Redirect to the player statistics page
    context = {'item': player_statistic}
    return render(request, 'mydjangoapp/deletePlayerStatistics.html', context)