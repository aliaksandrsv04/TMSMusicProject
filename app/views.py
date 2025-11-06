from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import RegisterForm
from .models import Genre, Song, Playlist


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            login(request, user)  # сразу авторизуем пользователя
            return redirect('main')  # редирект на главную
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def main_view(request):
    genres = Genre.objects.all()
    genre_id = request.GET.get('genre')
    query = request.GET.get('q')
    songs = Song.objects.all()
    if genre_id:
        songs = songs.filter(genre_id=genre_id)
    if query:
        songs = songs.filter(
            Q(title__icontains=query) |
            Q(artist__name__icontains=query)
        )
    user = request.user
    is_connected = tuple(user.playlists.values_list('songs_id', flat=True))
    if request.GET.get('song'):
        playlist = Playlist.objects.filter(Q(user_id=request.user) & Q(songs_id =request.GET.get('song')))
        if not playlist:
            Playlist.objects.create(user=request.user, songs_id =request.GET.get('song'))
        return redirect('main')
    #можно было часть удаления сделать попроще, но на что головы хватило
    if request.GET.get('song_delete'):
        Playlist.objects.filter(Q(songs_id = request.GET.get('song_delete')) & Q(user_id = request.user.id)).delete()
        return redirect('main')
    return render(request, 'main.html', {
        'songs': songs,
        'genres': genres,
        'selected_genre': genre_id,
        'is_connected': is_connected
    })

@login_required(login_url='login')
def playlist_view(request):
        user = request.user

        genre_id = request.GET.get('genre')
        query = request.GET.get('q')
        songs = Song.objects.filter(id__in = tuple(user.playlists.all().values_list('songs_id', flat=True)))
        list_id = songs.values_list('genre_id', flat=True)
        genres = Genre.objects.filter(id__in=list_id)
        if genre_id:
            songs = songs.filter(genre_id=genre_id)
        if query:
            songs = songs.filter(
                Q(title__icontains=query) |
                Q(artist__name__icontains=query)
            )
        is_connected = tuple(user.playlists.values_list('songs_id', flat=True))
        # можно было часть удаления сделать попроще, но на что головы хватило
        if request.GET.get('song_delete'):
            Playlist.objects.filter(Q(songs_id=request.GET.get('song_delete')) & Q(user_id=request.user.id)).delete()
            return redirect('playlist_view')
        return render(request, 'playlist_view.html', {
            'songs': songs,
            'genres': genres,
            'selected_genre': genre_id,
            'is_connected': is_connected
        })