import json
import spotipy
import spotipy.util as util

SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

with open('../credentials.json', encoding='utf-8') as file:
    credentials = json.load(file)
    SPOTIPY_CLIENT_ID = credentials['client_id']
    SPOTIPY_CLIENT_SECRET = credentials['client_secret']

token = util.prompt_for_user_token(username, scope='', client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI)

spotify = spotipy.Spotify(auth=token)
result = spotify.search(q='artist:' + 'Akon', type='artist')
print(result)

