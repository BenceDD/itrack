
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.current_music,name = 'current_music'),
    url(r'^redirect_to_spotify',views.redirect_to_spotify,name = 'redirect_to_spotify'),
    url(r'^login',views.login,name = 'login'),
    # AJAX handling
    url(r'^ajax/get_user_playlists/', views.get_user_playlists, name='get_user_playlists'),
    url(r'^ajax/get_current_listening/', views.get_current_listening, name='get_current_listening'),
    url(r'^ajax/get_playlist_by_id/$', views.get_playlist_by_id, name='get_playlist_by_id'),
    url(r'^ajax/get_song_info/$', views.get_song_info, name='get_song_info'),
] 
