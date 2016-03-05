from django.contrib import admin
from storeapp.models import Player, Game, Developer, Transaction, Score, SavedGame
# Register your models here.
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Developer)
admin.site.register(Transaction)
admin.site.register(Score)
admin.site.register(SavedGame)
