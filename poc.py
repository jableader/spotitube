import requests, base64, json

import secrets

def get_token(clientid, clientsecret):
    creds = bytearray(clientid + ':' + clientsecret, 'ansi')
    headers = {'Authorization': 'Basic ' + str(base64.b64encode(creds))[2:-1] }
    data = { 'grant_type': 'client_credentials' }
    res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    res.raise_for_status()

    return res.json()['access_token']

def add_token(token, **headers):
    return { 'Authorization': 'Bearer ' + token, **headers}

def get_tracks(token, userId, playlistId):
    resp = requests.get('https://api.spotify.com/v1/users/%s/playlists/%s' %(userId, playlistId), headers=add_token(token))
    

token = get_token(secrets.CLIENT_ID, secrets.CLIENT_SECRET)
resp = print(resp.text)
