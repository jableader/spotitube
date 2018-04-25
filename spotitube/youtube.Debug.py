from youtube import youtube
import secrets

ytAPI = youtube(secrets.YOUTUBE_API_KEY)

searchResult = ytAPI.search('mgmt,kids,song')

print(searchResult)
