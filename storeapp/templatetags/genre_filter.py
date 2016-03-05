from django import template
from storeapp.models import Game, Player

register = template.Library()


# Checks if the game has the given genre
@register.filter()
def has_genre(game, genre):
    if game.genre == genre:
        return True
    else:
        return False
