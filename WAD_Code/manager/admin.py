from django.contrib import admin
from manager.models import Player, Team, Match, Team_Request

# Register your models here.
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Team_Request)