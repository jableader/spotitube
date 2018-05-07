import requests, base64, json, datetime

class Track:
    def __init__(self, name, artist, year):
        self.name = name
        self.artist = artist
        self.year = year

    def __str__(self):
        return "%s: %s (%s)" % (self.artist, self.name, self.year)

class Playlist:
    def __init__(self, name, tracks):
        self.name = name
        self.tracks = tracks

    def __str__(self):
        return "Playlist('%s', %d)" % (self.name, len(self.tracks))

class Token:
    def __init__(self, access_token, expires_in):
        self.access_token = access_token
        self.expire_date = datetime.date.today()

    def is_expired(self):
        return datetime.date.today() > self.expire_date

spotify_auth_token = Token('', expires_in=0)
def get_token(clientid, clientsecret):
    global spotify_auth_token
    if not spotify_auth_token.is_expired:
        return token

    creds = clientid + ':' + clientsecret
    headers = {'Authorization': 'Basic ' + str(base64.b64encode(bytearray(creds))) }
    data = { 'grant_type': 'client_credentials' }
    res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    res.raise_for_status()
    spotify_auth_token = Token(**res.json())

    return spotify_auth_token

def _add_token(token, **headers):
    return { 'Authorization': 'Bearer ' + token.access_token, **headers}

def _to_track(track):
    artist = track['artists'][0]['name']
    name = track['name']
    year = track['album']['release_date'][:4]

    return Track(name, artist, year)

def get_playlist(token, userId, playlistId):
    r = requests.get('https://api.spotify.com/v1/users/%s/playlists/%s' %(userId, playlistId), headers=_add_token(token))
    r.raise_for_status()

    data = r.json()
    tracks = [_to_track(track['track']) for track in data['tracks']['items']]
    return Playlist(data['name'], tracks)
