import requests

def get_token(clientid, clientsecret):
    requests.post('https://accounts.spotify.com/api/token', data = { \
        'grant_type': 'authorization_code', \
        'code':  # TODO
        'redirect_uri':
    })

resp = requests.get('https://api.spotify.com/v1/users/spotify/playlists/37i9dQZF1DX5WTH49Vcnqp')
