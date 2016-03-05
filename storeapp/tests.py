from django.test import TestCase
from storeapp.models import Game, Player, Developer
from storeapp.templatetags.buy_button_filter import has_game
from storeapp.templatetags.genre_filter import has_genre
from storeapp.templatetags.group_filter import has_group
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import json


class BuyButtonTagTestCase(TestCase):

    def setUp(self):
        playerUser = User.objects.create_user(username="eetu", password="sipulionpahaa")
        group = Group.objects.get_or_create(name='players')[0]
        group.user_set.add(playerUser)
        playerUser.save()
        devUser = User.objects.create_user(username="devaaja", password="olenparas")
        groupDev = Group.objects.get_or_create(name='developers')[0]
        groupDev.user_set.add(devUser)
        devUser.save()
        self.player = Player.objects.create(user=playerUser)
        self.dev = Developer.objects.create(user=devUser, iban="asd")

    def test_player_should_have_game(self):
        game = Game.objects.create(
            name="test",
            dev=self.dev,
            price=0,
            url="http://www.google.com/"
        )
        self.player.games.add(game)
        self.assertEqual(True, has_game(self.player.user, game.pk))

    def test_player_should_not_have_game(self):
        game = Game.objects.create(
            name="test",
            dev=self.dev,
            price=0,
            url="http://www.google.com/"
        )
        self.assertEqual(False, has_game(self.player.user, game.pk))


class GenreFilterTagTestCase(TestCase):

    def setUp(self):
        devUser = User.objects.create_user(username="devaaja", password="olenparas")
        groupDev = Group.objects.get_or_create(name='developers')[0]
        groupDev.user_set.add(devUser)
        devUser.save()
        dev = Developer.objects.create(user=devUser, iban="asd")
        self.game = Game.objects.create(
            name="test",
            dev=dev,
            genre='RPG',
            price=0,
            url="http://www.google.com/"
        )

    def test_should_be_equal_genre(self):
        self.assertEqual(True, has_genre(self.game, 'RPG'))

    def test_should_not_be_equal_genre(self):
        self.assertEqual(False, has_genre(self.game, 'Action/Adventure'))


class GroupFilterTagTestCase(TestCase):

    def setUp(self):
        playerUser = User.objects.create_user(username="eetu", password="sipulionpahaa")
        group = Group.objects.get_or_create(name='players')[0]
        group.user_set.add(playerUser)
        playerUser.save()
        devUser = User.objects.create_user(username="devaaja", password="olenparas")
        groupDev = Group.objects.get_or_create(name='developers')[0]
        groupDev.user_set.add(devUser)
        devUser.save()
        self.player = Player.objects.create(user=playerUser)
        self.dev = Developer.objects.create(user=devUser, iban="asd")

    def test_player_has_correct_group(self):
        self.assertEqual(True, has_group(self.player.user, 'players'))

    def test_player_has_not_dev_group(self):
        self.assertEqual(False, has_group(self.player.user, 'developers'))

    def test_dev_has_correct_group(self):
        self.assertEqual(True, has_group(self.dev.user, 'developers'))

    def test_dev_has_not_player_group(self):
        self.assertEqual(False, has_group(self.dev.user, 'players'))


class PlayerRegistrationTestCase(TestCase):

    def test_valid_form(self):
        data = {
            'username': 'eetu',
            'email': 'ed-94@live.com',
            'password1': 'eetupoika94',
            'password2': 'eetupoika94'
        }
        response = self.client.post('/accounts/player_registration/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register_success.html/')

    def test_passwords_dont_match(self):
        data = {
            'username': 'eetu',
            'email': 'ed-94@live.com',
            'password1': 'eetupoika94',
            'password2': 'eetupoika9'
        }
        response = self.client.post('/accounts/player_registration/', data)
        self.assertFormError(response, 'user_form', 'password2', u"The two password fields didn't match.")

    def test_invalid_email(self):
        data = {
            'username': 'eetu',
            'email': 'abab',
            'password1': 'eetupoika94',
            'password2': 'eetupoika94'
        }
        response = self.client.post('/accounts/player_registration/', data)
        self.assertFormError(response, 'user_form', 'email', u'Enter a valid email address.')


class DevRegistrationTestCase(TestCase):

    def test_valid_form(self):
        data = {
            'first_name': 'eetu',
            'last_name': 'vilkki',
            'iban': 'asd',
            'username': 'eetu',
            'email': 'ed-94@live.com',
            'password1': 'eetupoika94',
            'password2': 'eetupoika94'
        }
        response = self.client.post('/accounts/developer_registration/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register_success.html/')


class AddGameTestCase(TestCase):

    def setUp(self):
        devUser = User.objects.create_user(username="devaaja", password="olenparas")
        groupDev = Group.objects.get_or_create(name='developers')[0]
        groupDev.user_set.add(devUser)
        devUser.save()
        dev = Developer.objects.create(user=devUser, iban="asd")

    def test_valid_game_form(self):
        self.client.login(username='devaaja', password='olenparas')
        data = {
            'name': 'test',
            'url': 'http://google.com/',
            'price': 5,
            'genre': 'RPG'
        }
        response = self.client.post('/accounts/add/', data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/')

    def test_invalid_game_price(self):
        self.client.login(username='devaaja', password='olenparas')
        data = {
            'name': 'test',
            'url': 'http://google.com/',
            'price': -2,
            'genre': 'RPG'
        }
        response = self.client.post('/accounts/add/', data)
        self.assertFormError(response, 'game_form', 'price', 'The price can not be a negative value')

    def test_invalid_game_url(self):
        self.client.login(username='devaaja', password='olenparas')
        data = {
            'name': 'test',
            'url': 'asd',
            'price': 4,
            'genre': 'RPG'
        }
        response = self.client.post('/accounts/add/', data)
        self.assertFormError(response, 'game_form', 'url', u'Enter a valid URL.')


class PasswordChangeTestCase(TestCase):

    def setUp(self):
        devUser = User.objects.create_user(username="devaaja", password="olenparas")
        groupDev = Group.objects.get_or_create(name='developers')[0]
        groupDev.user_set.add(devUser)
        devUser.save()
        dev = Developer.objects.create(user=devUser, iban="asd")
        self.client.login(username='devaaja', password='olenparas')

    def test_valid_password_change(self):
        data = {
            'old_password': 'olenparas',
            'new_password1': 'hilipatiheijaa',
            'new_password2': 'hilipatiheijaa'
        }
        response = self.client.post('/accounts/change_password/', data)
        self.assertRedirects(response, '/accounts/')

    def test_invalid_password_change(self):
        data = {
            'old_password': 'olenparas',
            'new_password1': 'hilipatiheijaa',
            'new_password2': 'hilipatiheija'
        }
        response = self.client.post('/accounts/change_password/', data)
        self.assertFormError(response, 'form', 'new_password2', u"The two password fields didn't match.")


class HighscoreTestCase(TestCase):

    def test_highscore_update(self):
        playerUser = User.objects.create_user(username="eetu", password="sipulionpahaa")
        group = Group.objects.get_or_create(name='players')[0]
        group.user_set.add(playerUser)
        playerUser.save()
        player = Player.objects.create(user=playerUser)
        devUser = User.objects.create_user(username="devaaja", password="olenparas")
        groupDev = Group.objects.get_or_create(name='developers')[0]
        groupDev.user_set.add(devUser)
        devUser.save()
        dev = Developer.objects.create(user=devUser, iban="asd")
        game = Game.objects.create(
            name="test",
            dev=dev,
            price=0,
            url="http://www.google.com/"
        )
        player.games.add(game)

        self.client.login(username="eetu", password="sipulionpahaa")
        data = {
            'score': 50,
            'user_id': player.user.pk,
            'game_id': game.pk
        }
        response = self.client.post('/update_score/', data)
        self.assertJSONEqual(response.content, {u'1': [u'eetu', 50.0], u'user_scores': [50.0]})


class SaveLoadTestCase(TestCase):

    def setUp(self):
        playerUser = User.objects.create_user(username="eetu", password="sipulionpahaa")
        group = Group.objects.get_or_create(name='players')[0]
        group.user_set.add(playerUser)
        playerUser.save()
        self.player = Player.objects.create(user=playerUser)
        devUser = User.objects.create_user(username="devaaja", password="olenparas")
        groupDev = Group.objects.get_or_create(name='developers')[0]
        groupDev.user_set.add(devUser)
        devUser.save()
        dev = Developer.objects.create(user=devUser, iban="asd")
        self.game = Game.objects.create(
            name="test",
            dev=dev,
            price=0,
            url="http://www.google.com/"
        )
        self.player.games.add(self.game)

        self.client.login(username="eetu", password="sipulionpahaa")

    def test_save(self):
        game_data = {
            "score": 50
        }
        data = {
            "save_data": json.dumps(game_data),
            "user_id": self.player.user.pk,
            "game_id": self.game.pk
        }
        response = self.client.post('/save_game/', data)
        self.assertHTMLEqual(response.content, 'Save success')

    def test_load(self):
        load_data = {
            "user_id": self.player.user.pk,
            "game_id": self.game.pk
        }
        response = self.client.get('/load_game/', load_data)
        self.assertJSONEqual(response.content, {'messageType': 'ERROR', 'info': 'Save game not found'})
        game_data = {
            "score": 50
        }
        data = {
            "save_data": json.dumps(game_data),
            "user_id": self.player.user.pk,
            "game_id": self.game.pk
        }
        self.client.post('/save_game/', data)

        message = {u'gameState': u'{"score": 50}', u'messageType': u'LOAD'}
        response = self.client.get('/load_game/', load_data)
        self.assertJSONEqual(response.content, message)
