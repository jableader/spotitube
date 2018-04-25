import requests
import json

class youtube:
    """Allows calls against Youtube API"""
    key = ''
    maxResults = 10
    searchType = 'video'
    part = 'snippet'

    def __init__(self, key):
        self.key = key
    
    def search(self, query):
        if not query:
            raise ValueError('query was blank')
        payload = {'q':query,
                   'key':self.key, 
                   'maxResults':self.maxResults, 
                   'type':self.searchType, 
                   'part':self.part}
        r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
        return r.json()
    
class video:
    """Youtube Video"""
    id = ''
    publishDate = '2001-01-01'
    title = ''
    description = ''
    thumbnail = ''


