import json
import spotipy
import spotipy.util as util

redirect_uri = 'http://localhost:8888/callback'
spotify_scope = 'user-read-playback-state user-read-currently-playing'

with open('../credentials.json', encoding='utf-8') as file:
    credentials = json.load(file)
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    username = credentials['username']

print(username)

token = util.prompt_for_user_token(username, scope=spotify_scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)
spotify = spotipy.Spotify(auth=token)

result = spotify.current_playback()

print(result['item']['artists'][0]['name'] + ' - ' + result['item']['name'])

