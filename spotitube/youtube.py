import requests, json, threading

class Video:
    def __init__(self, videoJSON):
        if not videoJSON['id']['kind'] == 'youtube#video':
            raise Exception('JSON was not a Youtube Video')
        self.id = videoJSON['id']['videoId']
        self.channelTitle = videoJSON['snippet']['channelTitle']
        self.publishDate = videoJSON['snippet']['publishedAt']
        self.title = videoJSON['snippet']['title']
        self.description = videoJSON['snippet']['description']

    def __str__(self):
        return self.channelTitle + ' - ' + self.title

    def todict(self):
        return self.__dict__

def _build_findquery(client, track):
    return client.search().list(
        q='"%s" "%s" %s Official' % (track.name, track.artist, track.year),
        type="video",
        part="id,snippet",
        maxResults=10,
      )

def _add_first_official(d, track):
    def _inner(id, resp, ex):
        hrank, hv = 0, None
        for item in resp.get('items'):
            video = Video(item)
            vrank = _might_be_official(video, track)
            if vrank > hrank:
                hrank, hv = vrank, video

        if hv:
            d[track] = hv

    return _inner

def _might_be_official(video, track):
    rank = 0
    channel, title = video.channelTitle.lower(), video.title.lower()
    if 'vevo' in channel:
        rank += 10

    if 'official audio' in title:
        rank -= 20
    elif 'official' in title:
        rank += 5

    if 'Auto-generated by YouTube.' in video.description:
        rank -= 20

    if track.artist.lower() in channel and not channel.endswith('- topic'):
        rank += 10

    if 'lyric' in title and 'lyric' not in track.name.lower() and 'lyric' not in track.artist.lower():
        rank -= 10

    return rank

def findvideos(client, tracks):
    batch = client.new_batch_http_request()
    videos = {}
    for t in tracks:
        batch.add(_build_findquery(client, t), _add_first_official(videos, t))

    batch.execute()
    return [(t, videos[t]) for t in tracks if t in videos]


def _build_addquery(client, playlistid, video):
    return client.playlistItems().insert(
        part='snippet',
        body={
            'snippet':{
                'playlistId': playlistid,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video.id
                }
            }
        }
    )

def _addvideos(client, playlistid, videos):
    for v in videos:
        _build_addquery(client, playlistid, v).execute()

def createplaylist(client, title, videos):
    # There is a bug in the youtube api, adding as a batch will cause videos to
    # override one another, the workaround is to kick the playlist off with one
    # track, then spawn a new thread to add the rest sequentially

    resp = client.playlists().insert(
            part='snippet,status',
            body={
                'snippet': {'title': title},
                'status': {'privacyStatus': 'private'}
            }
        ).execute()

    playlistid = resp.get('id')
    _build_addquery(client, playlistid, videos[0]).execute()

    t = threading.Thread(target=_addvideos, args=(client, playlistid, videos[1:]))
    t.start()

    return playlistid
