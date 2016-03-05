from hashlib import md5

from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from social.pipeline.partial import partial
import json
from . import forms, models, emailauth
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

secret_key = '272c6dff6df2b5d954290ee9bbdcce7f'


def home(request):
    games = models.Game.objects.filter(active=True).order_by('-sold')[0:5]
    return render(request, 'home.html', {'games_list': games})


@login_required
def save_game(request):
    if request.method == "POST":
        try:
            new_save_data = request.POST['save_data']
            new_save_data = json.dumps(new_save_data)
            game_model = models.Game.objects.get(id=request.POST['game_id'])
            player_user = models.User.objects.get(id=request.POST['user_id'])
            player_model = models.Player.objects.get(user=player_user)
            if not models.SavedGame.objects.filter(player=player_model,
                                                   game=game_model):
                models.SavedGame.objects.create(player=player_model,
                                                game=game_model,
                                                save_data=new_save_data)
            else:
                saved_game = models.SavedGame.objects.get(player=player_model,
                                                          game=game_model)
                saved_game.save_data = new_save_data
                saved_game.save()
            return HttpResponse('Save success')
        except MultiValueDictKeyError:
            raise Http404("save game didnt include all necessary data")
        except ObjectDoesNotExist:
            raise Http404("ObjectDoesNotExist")
    else:
        raise Http404("Save_game tried to be", request.method)


@login_required
def load_game(request):
    if request.method == 'GET':
        try:
            game_model = models.Game.objects.get(id=request.GET['game_id'])
            player_user = models.User.objects.get(id=request.GET['user_id'])
            player_model = models.Player.objects.get(user=player_user)
            save_game = models.SavedGame.objects.get(player=player_model,
                                                     game=game_model)
            message = {'messageType': 'LOAD',
                       'gameState': json.loads(save_game.save_data)}
            return JsonResponse(message)
        except MultiValueDictKeyError:
            raise Http404("GameId or UserID not found")
        except ObjectDoesNotExist:
            message = {'messageType': 'ERROR', 'info': 'Save game not found'}
            return JsonResponse(message)

    else:
        raise Http404("Load_game request was not GET")


@login_required
def update_highscores(request):
    try:
        if request.method == "POST":
            new_score = request.POST['score']
            player_user = models.User.objects.get(id=request.POST['user_id'])
            player_model = models.Player.objects.get(user=player_user)
            game_model = models.Game.objects.get(id=request.POST['game_id'])
            if not models.Score.objects.filter(player=player_model, game=game_model, score=new_score):
                score_object = models.Score.objects.create(score=new_score,
                                                           player=player_model,
                                                           game=game_model)
                score_object.save()
            return get_highscores(request, game_model, player_model)
        if request.GET.get('game_id'):
            game_model = models.Game.objects.get(id=request.GET['game_id'])
            player = models.Player.objects.get(user=request.user)
            return get_highscores(request, game_model, player)
    except MultiValueDictKeyError:
        raise Http404("correct request data not found")
    except ObjectDoesNotExist:
        raise Http404("ObjectDoesNotExist")
    raise Http404("update_highscores failed")


@login_required
def get_highscores(request, game_model, player):
    user_scores = game_model.scores.filter(player=player).order_by('-score')[:5]
    user_scores = [s.score for s in user_scores]
    scores = game_model.scores.all().order_by('-score')[:5]
    scores = {s.id: [s.player.user.username, s.score] for s in scores}
    scores['user_scores'] = user_scores
    return JsonResponse(scores)


def register_player(request):
    """
    Gets the required information from the user_form and then creates a user and a player
    based on that information. When the player profile is saved, sends an authentication email to the
    player. If there are errors in the form or it is not complete, reloads the page with the error
    messages.
    """

    if request.method == 'POST':
        player_reg_form = forms.PlayerRegForm(request.POST)
        user_form = forms.UserForm(request.POST)
        if player_reg_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user = user_form.save()
            group = Group.objects.get_or_create(name='players')[0]
            group.user_set.add(user)
            player_profile = player_reg_form.save(commit=False)
            player_profile.user = user
            player_profile.save()
            player_reg_form.save_m2m()
            emailauth.send_auth_email(str(user.username))
            return register_success(request, str(user.username), user.email)
    else:
        user_form = forms.UserForm()
    return render(request, 'registration/register_player.html/',
                  {'user_form': user_form})


def register_dev(request):
    """
    Does the same as register_player but with a developer.
    """
    if request.method == 'POST':
        dev_reg_form = forms.DevRegForm(request.POST)
        user_form = forms.UserForm(request.POST)
        if dev_reg_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.first_name = dev_reg_form.cleaned_data['first_name']
            user.last_name = dev_reg_form.cleaned_data['last_name']
            user.is_active = False
            user.save()
            group = Group.objects.get_or_create(name='developers')[0]
            group.user_set.add(user)
            dev_profile = dev_reg_form.save(commit=False)
            dev_profile.user = user
            dev_profile.iban = dev_reg_form.cleaned_data['iban']
            dev_profile.save()
            dev_reg_form.save_m2m()
            emailauth.send_auth_email(str(user.username))
            return register_success(request, str(user.username), user.email)
    else:
        user_form = forms.UserForm()
        dev_reg_form = forms.DevRegForm()
    return render(request, 'registration/register_dev.html/', {
                  'user_form': user_form,
                  'dev_reg_form': dev_reg_form})


def register_success(request, name_of_user, email):
    return render(request, 'registration/register_success.html/',
                  {'full_name': name_of_user, 'email': email})


def activate_account(request):
    query = request.GET
    try:
        user_id = int(query.get('id'))/42
    except ValueError:
        return HttpResponseRedirect('/home/')
    user = get_object_or_404(models.User, id=user_id)
    email_address = str(query.get('email'))
    if user.email == email_address:
        user.is_active = True
        user.save()
        return render(request, 'registration/activate_success.html',
                      {'email': email_address})
    else:
        raise Http404()


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/home/')
    elif user:
        return render(request, 'registration/not_activated.html')
    else:
        return HttpResponseRedirect('/accounts/invalid/')


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        return render(request, 'registration/login_required.html')


@login_required
def loggedin(request):
    if request.user.groups.filter(name='players'):
        return render(request, 'registration/loggedin_player.html',
                      {'full_name': request.user.username})
    if request.user.groups.filter(name='developers'):
        return render(request, 'registration/loggedin_dev.html',
                      {'full_name': request.user.username})


@login_required
def logout(request):
    name = request.user.username
    auth.logout(request)
    return render(request, 'registration/logout.html', {'full_name': name})


def invalid_login(request):
    return render(request, 'registration/invalid_login.html')


@login_required
def account_page(request):
    """
    Shows the correct account page to the user based on whether he is a player or a developer.
    """
    if request.user.groups.filter(name='developers'):
        developer = models.Developer.objects.get(user=request.user)
        return render(request, 'accounts/dev_page.html',
                      {'games': models.Game.objects.filter(dev=developer),
                       'dev': developer})
    else:
        player = models.Player.objects.get(user=request.user)
        return render(request, 'accounts/player_page.html',
                      {'games': player.games.all()})


@login_required
def add_game(request):
    """
    Gets the required information from the game_form and if the form is valid saves a new game
    to the database. If there are errors in the form or it is empty, reloads the page with the
    error messages.
    """
    if request.method == 'POST' and request.user.groups.filter(name='developers'):
        game_form = forms.GameForm(request.POST)
        if game_form.is_valid():
            game = models.Game(name=game_form.cleaned_data['name'], url=game_form.cleaned_data['url'],
                               price=game_form.cleaned_data['price'],
                               dev=models.Developer.objects.get(user=request.user),
                               genre=game_form.cleaned_data['genre'])
            game.save()
            messages.success(request, 'Game added.')
            return HttpResponseRedirect('/accounts/')
    else:
        game_form = forms.GameForm()
    if request.user.groups.filter(name='developers'):
        return render(request, 'accounts/add_game.html', {'game_form': game_form})
    else:
        return render(request, 'home.html')


def all_games(request):
    games = models.Game.objects.filter(active=True).order_by('-sold')
    return render(request, 'games/all.html', {'games_list': games, 'genres': list(models.Game.GENRE_CHOICES)})


def gamepage(request, id):
    game = get_object_or_404(models.Game, pk=id)
    if game.active:
        return render(request, 'games/gamepage.html', {'game': game})
    else:
        return HttpResponseRedirect('/games/')


@login_required
def buy_game(request, id):
    game = get_object_or_404(models.Game, pk=id)
    player = models.Player.objects.get(user=request.user)
    if game not in player.games.all():
        transaction = models.Transaction(owner=player, game=game)
        transaction.save()
        player.transactions.add(transaction)
        checksum = md5("pid={}&sid={}&amount={}&token={}".format(transaction.pk, 'eelajoo', game.price, secret_key).encode("ascii")).hexdigest()
        return render(request, 'payment/buy_game.html', {'pid': transaction.pk, 'sid': 'eelajoo', 'amount': game.price, 'checksum': checksum})
    else:
        return render(request, 'games/gamepage.html', {'game': game.get(pk=id)})


@login_required
def buy_success(request):
    if request.method == 'GET':
        try:
            pid = request.GET['pid']
            checksum = md5("pid={}&ref={}&result={}&token={}".format(pid, request.GET['ref'], request.GET['result'], secret_key).encode("ascii")).hexdigest()
            trans = models.Transaction.objects.get(pk=pid)
            game = trans.game
            if checksum == request.GET['checksum'] and game:
                models.Player.objects.get(user=request.user).games.add(game)
                trans.success = True
                trans.save()
                game.sold += 1
                game.save()
                return render(request, 'payment/buy_success.html', {'game_id': game.id})
        except:
            raise Http404()
    return all_games(request)


@login_required
def buy_cancel(request):
    if request.method == 'GET':
        try:
            game = models.Transaction.objects.get(pk=request.GET['pid']).game
            if game:
                return render(request, 'payment/buy_cancel.html', {'game_id': game.id})
        except:
            raise Http404()
    return all_games(request)


@login_required
def buy_fail(request):
    if request.method == 'GET':
        try:
            game = models.Transaction.objects.get(pk=request.GET['pid']).game
            if game:
                return render(request, 'payment/buy_fail.html', {'game_id': game.id})
        except:
            raise Http404()
    return all_games(request)


@login_required
def gamepage_dev(request, id):
    if request.user.groups.filter(name='developers'):
        game = get_object_or_404(models.Game, pk=id)
        dev = get_object_or_404(models.Developer, user=request.user)
        if game in dev.games.all():
            trans = models.Transaction.objects.all().filter(game=game).filter(success=True).order_by('-date')[:10]
            return render(request, 'games/gamepage_dev.html', {'game': game, 'transactions': trans})
    return HttpResponseRedirect('/accounts/')


@login_required
def update_game(request, id):
    """
    Developers can update their games' information with this function. Gets the required information
    from the form and if the form is valid, updates the game's information in the database.
    """
    args = {}
    game = get_object_or_404(models.Game, pk=id)
    if request.method == 'POST' and request.user.groups.filter(name='developers'):
        dev = models.Developer.objects.get(user=request.user)
        if game in dev.games.all():
            form = forms.GameForm(request.POST, instance=game)
            if form.is_valid():
                form.save()
                messages.success(request, 'Game updated.')
                return HttpResponseRedirect('/accounts/')
        else:
            return HttpResponseRedirect('/home/')
    else:
        form = forms.GameForm(initial={'name': game.name, 'url': game.url, 'price': game.price,
                                       'genre': game.genre})
    args['form'] = form
    if game:
        args['game'] = game
    return render(request, 'accounts/update_game.html', args)


@login_required
def de_or_reactivate_game(request, id):
    """
    If the developer wants to remove his game from the store, this function marks the game as inactive
    so other people cannot find it from the store.
    """
    if request.user.groups.filter(name='developers'):
        game = get_object_or_404(models.Game, pk=id)
        dev = models.Developer.objects.get(user=request.user)
        if game in dev.games.all() and game.active:
            game.active = False
        else:
            game.active = True
        game.save()
    return HttpResponseRedirect('/accounts/games/' + id + '/')


def search_games(request):
    """
    Finds all the games that have the typed string in their name. The typed string
    comes from the POST request that was made in an ajax request via the search_game
    script. Then renders the search.html template with the found games and returns
    it to the search_game script.
    """
    if request.method == 'POST':
        game_name = request.POST['game_name']
        if len(game_name) > 0:
            games = models.Game.objects.filter(name__contains=game_name)
        else:
            games = models.Game.objects.none()
    else:
        games = models.Game.objects.none()
    return render(request, 'games/search.html', {'games': games})


def save_profile(strategy, backend, user, response, details, *args, **kwargs):
    """
    This is an addition to the facebook login pipeline. The function saves the user
    to the database if this is the first time that facebook login is being used by the user.
    """
    if backend.name == 'facebook':
        if models.Player.objects.filter(user=user).count() == 0:
            user.email = response.get('email')
            user.username = details['username']
            user.save()
            group = Group.objects.get(name='players')
            group.user_set.add(user)
            player = models.Player(user=user)
            player.save()


@partial
def get_user_info(strategy, details, user=None, is_new=False, *args, **kwargs):
    """
    Also an addition to the facebook login pipeline. If the user hasn't logged in via
    Facebook before, this view asks the user to give a username.
    """
    if is_new:
        username = strategy.request_data().get('username')
        if username:
            details['username'] = username
        else:
            return HttpResponseRedirect('/accounts/social_registration/')
    else:
        return


def social_register(request):
    return render(request, 'accounts/social_signup.html', {"form": forms.SocialSignUpForm})


@login_required
def password_change(request):
    """
    Allows the user to change his password. The form asks for the user's old password and then
    for the new one (also asks the new password again for confirmation). If the form is valid,
    saves the new password.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed.')
            return HttpResponseRedirect('/accounts/')
    else:
        form = PasswordChangeForm(request.user)
    data = {'form': form}
    return render(request, "accounts/password_change.html", data)
