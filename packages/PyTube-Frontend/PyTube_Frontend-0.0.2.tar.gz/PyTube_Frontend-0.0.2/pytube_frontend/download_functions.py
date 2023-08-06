import os
from pytube_frontend.streams import get_preffered_video_stream

'''
download_functions.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 28 JAN 23

Download the video and/or audio streams of a YouTube video
'''


# Download audio
def download_audio(streams, isTemp, storagePath):
    audioStreams = streams.filter(only_audio=True)
    preferredStream = audioStreams.order_by("abr").last()  # Get the stream with the highest audio bitrate
    if isTemp:
        filename = "audio.mp3"
    else:
        filename = "YouTube-Audio.mp3"
    filepath = os.path.join(storagePath, filename)
    preferredStream.download(storagePath, filename=filename)
    return filepath


# Download video
def download_video(streams, resolution, storagePath):
    videoStreams = streams.filter(only_video=True)
    preferredStream = get_preffered_video_stream(videoStreams, resolution)
    if type(preferredStream) == str and "Error: " in preferredStream: return preferredStream  # I don't like this.
    filetype = preferredStream.mime_type.split("/")[1]  # Get the filetype of that stream
    filename = "video" + "." + filetype
    filepath = os.path.join(storagePath, filename)

    preferredStream.download(storagePath, filename=filename)
    return filepath
