import json
import spotipy
import requests
from bs4 import BeautifulSoup
from spotipy import oauth2

from django.shortcuts import render, redirect
from django.http import JsonResponse

from spotipy_app.models import WikiDataWrapper
# Ez nem view, ezt ki kell tenni máshová!

def spotify_create_oauth():
    redirect_uri = 'http://localhost:8000/login'
    spotify_scope = 'user-read-playback-state user-read-currently-playing playlist-read-private'
    
    with open('../../credentials.json', encoding='utf-8') as file:
        credentials = json.load(file)
        client_id = credentials['client_id']
        client_secret = credentials['client_secret']
        #username = credentials['username']
    
    cache_path = None # ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=spotify_scope, cache_path=cache_path)
    
    return sp_oauth

def spotify_get_and_refresh_token(sp_oauth,prev_token):
    
    if prev_token is None:
        return None
    
    token_info = prev_token
    
    if sp_oauth.is_token_expired(prev_token):
        token_info = sp_oauth.refresh_access_token(prev_token["refresh_token"])
    
    return token_info;

def spotify_get_token_from_request(request):
    prev_token_cookie = request.COOKIES.get("spotify_id")
    prev_token_info = None;
    if prev_token_cookie is not None:
        prev_token_info = json.loads(prev_token_cookie)
    
    return prev_token_info

def get_spotify_client(previous_token):
    sp_oauth = spotify_create_oauth()
    token_info = spotify_get_and_refresh_token(sp_oauth,previous_token)
    
    if token_info is None:
        print('Token expired!!!') #TODO: Ide ilyenkor már elvileg csak akkor kéne ráfutnunk,
                                  #      ha mindent megírtunk, ha nem sikerül refreshelni.
        return
    
    token = token_info['access_token']
    return (spotipy.Spotify(auth=token),token_info)

def current_music(request):
    sp_oauth = spotify_create_oauth()
    
    prev_token_info = spotify_get_token_from_request(request)
    token_info = spotify_get_and_refresh_token(sp_oauth,prev_token_info)
    
    if token_info is None:
        return redirect("/redirect_to_spotify")
    
    response = render(request,'current_music.html')
    response.set_cookie("spotify_id",json.dumps(token_info))
    return response

def redirect_to_spotify(request):
    sp_oauth = spotify_create_oauth()
    
    prev_token_info = spotify_get_token_from_request(request)
    token_info = spotify_get_and_refresh_token(sp_oauth,prev_token_info)
    
    if token_info is None:
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    response = redirect("/login")
    response.set_cookie("spotify_id",json.dumps(token_info))
    return response

def login(request):
    sp_oauth = spotify_create_oauth()
    
    prev_token_info = spotify_get_token_from_request(request)
    token_info = spotify_get_and_refresh_token(sp_oauth,prev_token_info)
    
    if token_info is None:
        code = sp_oauth.parse_response_code(request.get_full_path())
        token_info = sp_oauth.get_access_token(code)
    
    response = redirect("/")
    response.set_cookie("spotify_id",json.dumps(token_info))
    return response

# AJAX Handling.
def get_data_from_track(track):
    if track is None:
        return {}

    image = None
    if len(track['album']['images']) > 1:
        image = track['album']['images'][1]['url']

    return {
        'track_id': track['id'],
        'album': track['album']['name'],
        'album_id': track['album']['id'],
        'artists': [{'name': artist['name'], 'id': artist['id']} for artist in track['artists']],
        'title': track['name'],
        'image': image,
    }

def get_user_playlists(request):
    
    prev_token_info = spotify_get_token_from_request(request)
    spotify,token_info = get_spotify_client(prev_token_info)
    
    result = spotify.current_user_playlists()
    playlists = [{'name': item['name'], 'playlist_id': item['id'], 'owner_id': item['owner']['id']} for item in result['items']]
    
    response = JsonResponse({'playlists': playlists})
    response.set_cookie("spotify_id",json.dumps(token_info))
    return response

def get_current_listening(request):
    
    prev_token_info = spotify_get_token_from_request(request)
    spotify,token_info = get_spotify_client(prev_token_info)
    
    result = spotify.current_playback()
    track = get_data_from_track(result['item'])
    
    response = JsonResponse({'track': track})
    response.set_cookie("spotify_id",json.dumps(token_info))
    return response

def get_playlist_by_id(request):
    playlist_id = request.POST.get('playlist_id')
    owner_id = request.POST.get('owner_id')
    
    prev_token_info = spotify_get_token_from_request(request);
    spotify,token_info = get_spotify_client(prev_token_info)
    
    result = spotify.user_playlist(user=owner_id, playlist_id=playlist_id)
    tracklist = [get_data_from_track(track['track']) for track in result['tracks']['items']]
    
    response = JsonResponse({'playlist': tracklist})
    response.set_cookie("spotify_id",json.dumps(token_info))
    return response

def get_song_info(request):
    track = json.loads(request.POST.get('track'))
    wiki_wapper = WikiDataWrapper()
    
    info = wiki_wapper.get_song_info(artist=track['artists'][0]['name'], artist_spotify_id=track['artists'][0]['id'],
        album=track['album'], album_spotify_id=track['album_id'], track=track['title'], track_spotify_id=track['album'])[0]

    if 'album' in info and 'wiki' in info['album']:
        info['album']['text'] = BeautifulSoup(requests.get(info['album']['wiki']).text,"html.parser").findAll('p')[0].text
    if 'artist' in info and 'wiki' in info['artist']:
        info['artist']['text'] = BeautifulSoup(requests.get(info['artist']['wiki']).text,"html.parser").findAll('p')[0].text
    if 'song' in info and 'wiki' in info['song']:
        info['song']['text'] = BeautifulSoup(requests.get(info['song']['wiki']).text,"html.parser").findAll('p')[0].text

    return JsonResponse({'info': info})
