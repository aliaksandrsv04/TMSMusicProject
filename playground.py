import os
import sys

import django

from django.db.models import Q

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicPortal.settings')
django.setup()
from django.contrib.auth.models import User

import random
from app.models import Song, Playlist, Genre

user = User.objects.get(id=1)
song = Song.objects.get(id=10)

# Способ 1: Через фильтрацию плейлистов
user = User.objects.get(id=1)
a = Song.objects.filter(id__in = tuple(user.playlists.all().values_list('songs_id', flat=True)))
list_id = a.values_list('genre_id', flat=True)
print(list_id)
b = Genre.objects.filter(id__in = list_id)
print(a)
print(b)