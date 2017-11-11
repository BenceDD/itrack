
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index,name = 'index'),
    url(r'^redirect_to_spotify',views.redirect_to_spotify,name = 'redirect_to_spotify'),
    url(r'^login',views.login,name = 'login'),
    url(r'^current_music',views.current_music,name = 'current_music'),
    # AJAX handling
    url(r'^ajax/get_playlist_by_name/$', views.get_playlist_by_name, name='get_playlist_by_name'),
    url(r'^ajax/get_current_listening/$', views.get_current_listening, name='get_current_listening'),
] 
