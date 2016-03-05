from django import template
from storeapp.models import Game, Player

register = template.Library()

# Checks if the given user has bought the given game
@register.filter()
def has_game(user, game_id):
    game = Game.objects.get(pk=int(game_id))
    if game in Player.objects.get(user=user).games.all():
        return True
    else:
        return False
