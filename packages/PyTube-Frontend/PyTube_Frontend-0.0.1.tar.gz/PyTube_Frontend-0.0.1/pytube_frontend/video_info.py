from pytube import YouTube
from pytube_frontend.streams import get_streams

# Get title of a YouTube video
def get_title(url):
    return YouTube(url).title

# Get the available resolutions of a YouTube video from a url (slower)
def get_resolutions_url(url):
    streams = get_streams(url)
    videoStreams = streams.filter(only_video=True)
    resolutions = []
    for stream in videoStreams:
        if stream.resolution not in resolutions: resolutions.append(stream.resolution)
    return resolutions

# Get the available resolutions of a YouTube video from streams (faster)
def get_resolutions_streams(streams):
    videoStreams = streams.filter(only_video=True)
    resolutions = []
    for stream in videoStreams:
        if stream.resolution not in resolutions: resolutions.append(stream.resolution)
    return resolutions

