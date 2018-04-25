import requests, base64, json

import secrets

def get_token(clientid, clientsecret):
    creds = bytearray(clientid + ':' + clientsecret, 'ansi')
    headers = {'Authorization': 'Basic ' + str(base64.b64encode(creds))[2:-1] }
    data = { 'grant_type': 'client_credentials' }
    res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    res.raise_for_status()

    return res.json()['access_token']

def _add_token(token, **headers):
    return { 'Authorization': 'Bearer ' + token, **headers}

def _get_track_data(track):
    artist = track['artists'][0]['name']
    name = track['name']
    year = track['album']['release_date'][:4]

    return {'artist': artist, 'name': name, 'year': year}

def get_tracks(token, userId, playlistId):
    r = requests.get('https://api.spotify.com/v1/users/%s/playlists/%s' %(userId, playlistId), headers=_add_token(token))
    r.raise_for_status()

    return [_get_track_data(track['track']) for track in r.json()['tracks']['items']]

print("Getting token")
token = get_token(secrets.CLIENT_ID, secrets.CLIENT_SECRET)

print("Getting tracks")
#spotify:user:spotify:playlist:37i9dQZF1DX5WTH49Vcnqp
print(get_tracks(token, 'spotify', '37i9dQZF1DX5WTH49Vcnqp'))
