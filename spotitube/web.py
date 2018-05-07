import spotify, secrets, flask, google_auth_oauthlib.flow, os

app = flask.Flask(__name__)
app.secret_key = secrets.APP_SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

flow = google_auth_oauthlib.flow.Flow.from_client_config({
        "installed": {
          "client_id": secrets.YOUTUBE_OAUTH_CLIENT_ID,
          "client_secret": secrets.YOUTUBE_OAUTH_CLIENT_SECRET,
          "redirect_uris": [],
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://accounts.google.com/o/oauth2/token"
        }
    }, ['https://www.googleapis.com/auth/youtube'])
flow.redirect_uri = 'http://localhost/oauth2callback'

def get_page(name):
    with open('html/%s.html' % name, 'r') as f:
        return f.read()

#Example: /api/createfor/spotify/37i9dQZF1DWTcqUzwhNmKv
@app.route("/api/createfor/<userid>/<playlistid>", methods=['POST'])
def api_create(userid, playlistid):
    app.logger.debug('Creating token')
    token = spotify.get_token(secrets.SPOTIFY_CLIENT_ID, secrets.SPOTIFY_CLIENT_SECRET)

    app.logger.debug('Loading playlist')
    playlist = spotify.get_playlist(token, userid, playlistid)

    app.logger.debug('Found %s', str(playlist))
    return json.dumps([{ t.__dict__ for t in playlist.tracks}])


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['oauth_state']
  flow.fetch_token(authorization_response=flask.request.url)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  flask.session['credentials'] = {
      'token': credentials.token,
      'refresh_token': credentials.refresh_token,
      'token_uri': credentials.token_uri,
      'client_id': credentials.client_id,
      'client_secret': credentials.client_secret,
      'scopes': credentials.scopes
  }
  return flask.redirect("/")

@app.route("/")
def hello():
    if 'credentials' not in flask.session:
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')

        # Store the state so the callback can verify the auth server response.
        flask.session['oauth_state'] = state
        return flask.redirect(authorization_url)

    return get_page("index")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['DEBUG'] = "1"
app.run(debug=True)
