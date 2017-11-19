
import json
import spotipy
from spotipy import oauth2

from django.shortcuts import render, redirect
from django.http import JsonResponse

# Ez nem view, ezt ki kell tenni máshová!

def create_sp_oauth():
    redirect_uri = 'http://localhost:8000/login'
    spotify_scope = 'user-read-playback-state user-read-currently-playing playlist-read-private'
    
    with open('../../credentials.json', encoding='utf-8') as file:
        credentials = json.load(file)
        client_id = credentials['client_id']
        client_secret = credentials['client_secret']
        username = credentials['username']
    
    cache_path = ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=spotify_scope, cache_path=cache_path)
    
    return sp_oauth

def get_spotify_client():
    sp_oauth = create_sp_oauth()
    token_info = sp_oauth.get_cached_token()
    if token_info is None:
        print('Token expired!!!')
        return
    token = token_info['access_token']

    return spotipy.Spotify(auth=token)

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
    return render(request,'current_music.html')


# AJAX Handling.
def get_user_playlists(request):
    spotify = get_spotify_client()

    result = spotify.current_user_playlists()
    playlists = [{'name': item['name'], 'playlist_id': item['id'], 'owner_id': item['owner']['id']} for item in result['items']]

    return JsonResponse({'playlists': playlists})

def get_current_listening(request):
    spotify = get_spotify_client()

    result = spotify.current_playback()
 
    if not result:
        track = {}
    else:
        track = {
            'album': result['item']['album']['name'],
            'artist': result['item']['artists'][0]['name'],
            'title': result['item']['name'],
        }

    return JsonResponse({'track': track })

def get_playlist_by_id(request):
    playlist_id = request.POST.get('playlist_id')
    owner_id = request.POST.get('owner_id')
    spotify = get_spotify_client()

    result = spotify.user_playlist(user=owner_id, playlist_id=playlist_id)

    tracklist = []
    for track in result['tracks']['items']:
        tracklist.append({
            'title': track['track']['name'],
            'album': track['track']['album']['name'],
            'artists': [artist['name'] for artist in track['track']['artists']],
        })

    return JsonResponse({'playlist': tracklist})