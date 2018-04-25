import requests
import json

class youtube:
    """Allows calls against Youtube API"""
    key = ''
    maxResults = 10
    searchType = 'video'
    part = 'snippet'
    order = 'viewCount'

    def __init__(self, key):
        if not key:
            raise ValueError('key was blank')
        self.key = key
    
    def search(self, query, order):
        if not query:
            raise ValueError('query was blank')
        payload = {'q':query,
                   'key':self.key, 
                   'maxResults':self.maxResults, 
                   'type':self.searchType, 
                   'part':self.part,
                   'order':order}
        r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
        return r.json()

    def getBestMusicVideo(self, query):
        # Get most viewed view. See if its a Vevo video, return it if it is
        results = self.search(query, 'viewCount')['items']        
        for result in results:
            vid = video(result)            
            if 'vevo' in vid.channelTitle.lower():
                return vid
        return video(results[0]) # Return most viewed if no vevo

class video:
    """Youtube Video"""
    id = ''
    channelTitle = ''
    publishDate = ''
    title = ''
    description = ''

    def __init__(self, videoJSON):
        if not videoJSON['id']['kind'] == 'youtube#video':
            raise Exception('JSON was not a Youtube Video')
        self.id = videoJSON['id']['videoId']
        self.channelTitle = videoJSON['snippet']['channelTitle']
        self.publishDate = videoJSON['snippet']['publishedAt']
        self.title = videoJSON['snippet']['title']
        self.description = videoJSON['snippet']['description']    

    def toString(self):
        return self.channelTitle + ' - ' + self.title