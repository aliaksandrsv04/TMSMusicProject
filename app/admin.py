from django.contrib import admin

from .models import Artist, Album, Song, Genre


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    # list_editable = ("name",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist")
    search_fields = ("title",)
    # list_editable = ("title","artist")

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "album")
    search_fields = ("title",)
    fields = ("title", "artist", "album")

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    # list_editable = ("name",)