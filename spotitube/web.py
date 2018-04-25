import spotify, secrets

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Please make dat web req"

#Example: /api/createfor/spotify/37i9dQZF1DWTcqUzwhNmKv
@app.route("/api/createfor/<userid>/<playlistid>")
def api_create(userid, playlistid):
    app.logger.debug('Creating token')
    token = spotify.get_token(secrets.CLIENT_ID, secrets.CLIENT_SECRET)

    app.logger.debug('Loading playlist')
    playlist = spotify.get_playlist(token, userid, playlistid)
    app.logger.debug('Found ' + str(playlist))

app.run(debug=True)
