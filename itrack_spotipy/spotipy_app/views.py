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
        username = credentials['username']
    
    cache_path = ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=spotify_scope, cache_path=cache_path)
    
    return sp_oauth

def spotify_get_and_refresh_token(sp_oauth,prev_token):
    #TODO: Majd itt kell megvalósítani azt, hogy a requestből szedjük ki a
    #tokent!
    return sp_oauth.get_cached_token();

def get_spotify_client():
    sp_oauth = spotify_create_oauth()
    token_info = spotify_get_and_refresh_token(sp_oauth,None) #TODO: None helyett itt majd a
                                                              #      korábbi tokent kell továbbítani.
    if token_info is None:
        print('Token expired!!!') #TODO: Ide ilyenkor már elvileg csak akkor kéne ráfutnunk,
                                  #      ha mindent megírtunk, ha nem sikerül refreshelni.
        return
    token = token_info['access_token']

    return spotipy.Spotify(auth=token)

def current_music(request):
    sp_oauth = spotify_create_oauth()
    token_info = spotify_get_and_refresh_token(sp_oauth,None) #TODO: None helyett itt majd a
                                                              #      korábbi tokent kell továbbítani.
    
    if token_info is None:
        return redirect("/redirect_to_spotify")
    
    return render(request,'current_music.html')

def redirect_to_spotify(request):
    sp_oauth = spotify_create_oauth()
    token_info = spotify_get_and_refresh_token(sp_oauth,None) #TODO: None helyett itt majd a
                                                              #      korábbi tokent kell továbbítani.
    
    if token_info is None:
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    return redirect("/login")

def login(request):
    sp_oauth = spotify_create_oauth()
    token_info = spotify_get_and_refresh_token(sp_oauth,None) #TODO: None helyett itt majd a
                                                              #      korábbi tokent kell továbbítani.
    
    if token_info is None:
        code = sp_oauth.parse_response_code(request.get_full_path())
        token_info = sp_oauth.get_access_token(code)
    
    token = token_info['access_token']
    
    return redirect("/")

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
    spotify = get_spotify_client()
    result = spotify.current_user_playlists()
    playlists = [{'name': item['name'], 'playlist_id': item['id'], 'owner_id': item['owner']['id']} for item in result['items']]
    return JsonResponse({'playlists': playlists})

def get_current_listening(request):
    spotify = get_spotify_client()
    result = spotify.current_playback()
    track = get_data_from_track(result['item'])
    return JsonResponse({'track': track })

def get_playlist_by_id(request):
    playlist_id = request.POST.get('playlist_id')
    owner_id = request.POST.get('owner_id')

    spotify = get_spotify_client()
    result = spotify.user_playlist(user=owner_id, playlist_id=playlist_id)
    tracklist = [get_data_from_track(track['track']) for track in result['tracks']['items']]
    return JsonResponse({'playlist': tracklist})

def get_song_info(request):
    
    track = json.loads(request.POST.get('track'))
    print(track)
    wiki_wapper = WikiDataWrapper()
    
    info = wiki_wapper.get_song_info(artist=track['artists'][0]['name'], artist_spotify_id=track['artists'][0]['id'],
        album=track['album'], album_spotify_id=track['album_id'], track=track['title'], track_spotify_id=track['album'])[0]
    print(info)
    if 'album' in info and 'wiki' in info['album']:
        info['album']['text'] = BeautifulSoup(requests.get(info['album']['wiki']).text,"html.parser").findAll('p')[0].text
    if 'artist' in info and 'wiki' in info['artist']:
        info['artist']['text'] = BeautifulSoup(requests.get(info['artist']['wiki']).text,"html.parser").findAll('p')[0].text
    if 'song' in info and 'wiki' in info['song']:
        info['song']['text'] = BeautifulSoup(requests.get(info['song']['wiki']).text,"html.parser").findAll('p')[0].text

    return JsonResponse({'info': info})