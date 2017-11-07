
import json
import spotipy
from spotipy import oauth2

from django.shortcuts import render, redirect

# Ez nem view, ezt ki kell tenni máshová!

def create_sp_oauth():
    redirect_uri = 'http://localhost:8000/login'
    spotify_scope = 'user-read-playback-state user-read-currently-playing'
    
    with open('../../credentials.json', encoding='utf-8') as file:
        credentials = json.load(file)
        client_id = credentials['client_id']
        client_secret = credentials['client_secret']
        username = credentials['username']
    
    cache_path = ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=spotify_scope, cache_path=cache_path)
    
    return sp_oauth

# Create your views here.

def index(request):
    return render(request,'index.html')

def redirect_to_spotify(request):
    sp_oauth = create_sp_oauth()
    token_info = sp_oauth.get_cached_token()
    
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    return redirect("/login")

def login(request):
    sp_oauth = create_sp_oauth()
    token_info = sp_oauth.get_cached_token()
    
    if not token_info:
        code = sp_oauth.parse_response_code(request.get_full_path())
        token_info = sp_oauth.get_access_token(code)
    
    token = token_info['access_token']
    
    return redirect("/current_music")

def current_music(request):
    sp_oauth = create_sp_oauth()
    token_info = sp_oauth.get_cached_token()
    token = token_info['access_token']
    
    spotify = spotipy.Spotify(auth=token)

    result = spotify.current_playback()
    
    if not result:
        return render(request,'current_music.html',context = {"Field":"Not listening"})
    
    return render(request,'current_music.html',context = {"Field":result['item']['artists'][0]['name'] + ' - ' + result['item']['name']})
