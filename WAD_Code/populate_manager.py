import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD_Code.settings')

import django
django.setup()
from manager.models import Player, Team, Match, Team_Players, Team_Request

def populate():
    pass