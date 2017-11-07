
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index,name = 'index'),
    url(r'^redirect_to_spotify',views.redirect_to_spotify,name = 'redirect_to_spotify'),
    url(r'^login',views.login,name = 'login'),
    url(r'^current_music',views.current_music,name = 'current_music'),
] 
