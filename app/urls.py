import debug_toolbar
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from .views import register_view, main_view

from .views import playlist_view

urlpatterns = [
    path('', main_view, name='main'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('playlist_view', playlist_view, name='playlist_view'),
]