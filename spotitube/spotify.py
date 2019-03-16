import requests, base64, json, datetime, secrets

class Track:
    def __init__(self, name, artist, year, art):
        self.name = name
        self.artist = artist
        self.year = year
        self.art = art

    def __str__(self):
        return "%s: %s (%s)" % (self.artist, self.name, self.year)

    def todict(self):
        return { 'name': self.name, 'artist': self.artist, 'year': self.year, 'art': self.art }

class Playlist:
    def __init__(self, name, tracks):
        self.name = name
        self.tracks = tracks

    def __str__(self):
        return "Playlist('%s', %d)" % (self.name, len(self.tracks))

class Token:
    def __init__(self, access_token, expires_in, **kwargs):
        self.access_token = access_token
        self.expire_date = datetime.date.today()

    def is_expired(self):
        return datetime.date.today() > self.expire_date

spotify_auth_token = Token('', expires_in=0)
def get_token(clientid=secrets.SPOTIFY_CLIENT_ID, clientsecret=secrets.SPOTIFY_CLIENT_SECRET):
    global spotify_auth_token
    if not spotify_auth_token.is_expired:
        return token

    creds = bytearray(clientid + ':' + clientsecret, 'utf8')
    headers = {'Authorization': 'Basic ' + base64.b64encode(creds).decode('utf8') }
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
    album = track['album']
    year = album['release_date'][:4]
    image = album['images'][0]['url']

    return Track(name, artist, year, image)

def get_playlist(token, playlistId):
    r = requests.get('https://api.spotify.com/v1/playlists/%s' % playlistId, headers=_add_token(token))
    r.raise_for_status()

    data = r.json()
    tracks = [_to_track(track['track']) for track in data['tracks']['items']]
    return Playlist(data['name'], tracks)
