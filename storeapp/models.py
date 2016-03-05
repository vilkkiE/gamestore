from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iban = models.CharField(max_length=50)


class Game(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    url = models.URLField(unique=True, blank=False)
    dev = models.ForeignKey(Developer, related_name='games')
    price = models.FloatField(blank=False)
    sold = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    ACTION = 'Action/Adventure'
    RPG = 'RPG'
    SHOOTER = 'Shooter'
    PUZZLE = 'Puzzle'
    GENRE_CHOICES = (
        (ACTION, 'Action/Adventure'),
        (RPG, 'RPG'),
        (SHOOTER, 'Shooter'),
        (PUZZLE, 'Puzzle'),
    )
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default=SHOOTER)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)

    class Meta:
        permissions = ()


class Transaction(models.Model):
    owner = models.ForeignKey(Player, related_name='transactions')
    game = models.ForeignKey(Game)
    date = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)


class SavedGame(models.Model):
    game = models.ForeignKey(Game)
    save_data = models.TextField(default='')
    player = models.ForeignKey(Player, related_name='saved_games')


class Score(models.Model):
    score = models.FloatField(default=0)
    game = models.ForeignKey(Game, related_name='scores')
    player = models.ForeignKey(Player, related_name='scores')
