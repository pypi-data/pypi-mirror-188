import os
from pytube import YouTube
from pytube_frontend.streams import get_streams
from pytube_frontend.download_functions import download_audio, download_video
from pytube_frontend.ffmpeg_functions import transcode, stitch_video
import ffmpeg
'''
main.py

@Author - Ethan Brown - ewbrowntech@gmail.com
@Version - 29 JAN 23

Get info about a YouTube video or download audio or video copies of it
'''
class Downloader:
    def __init__(self, observer=None):
        self.observer = observer

    # Register a new observer
    def register(self, observer):
        self.observer = observer

    # Get title of a YouTube video
    def get_title(self, url):
        return YouTube(url).title

    # Get the available resolutions of a YouTube video
    def get_resolutions(self, url):
        streams = get_streams(url)
        videoStreams = streams.filter(only_video=True)
        resolutions = []
        for stream in videoStreams:
            if stream.resolution not in resolutions: resolutions.append(stream.resolution)
        return resolutions

    # Get audio copy of the YouTube video
    async def get_audio_copy(self, url, streams, storagePath, isTemp=False):
        if url is not None and streams is None:
            streams = get_streams(url)
        elif url is None and streams is None:
            raise NoSourceError
        if hasattr(self.observer, 'audio_download_commence'):
            await self.observer.audio_download_commence()
        filepath = download_audio(streams, isTemp, storagePath)
        if hasattr(self.observer, 'audio_download_complete'):
            await self.observer.audio_download_complete()
        return filepath

    # Get a video-only copy of the YouTube video
    async def get_video_only_copy(self, url, streams, resolution, doTranscode, storagePath, isTemp=False):
        if url is not None and streams is None:
            streams = get_streams(url)
        elif url is None and streams is None:
            raise NoSourceError

        if isTemp:
            filename = "video.mp4"
        else:
            filename = "YouTube-Video.mp4"
        filepath = os.path.join(storagePath, filename)

        # Download the video
        if hasattr(self.observer, 'video_download_commence'):
            await self.observer.video_download_commence()
        rawVideo = download_video(streams, resolution, storagePath)
        if hasattr(self.observer, 'video_download_complete'):
            await self.observer.video_download_complete()

        if (doTranscode):
            if hasattr(self.observer, 'transcode_commence'):
                await self.observer.transcode_commence()
            transcode(rawVideo, filepath)  # Transcode AV1 or VP8/9 into h.264 for compatability
            if hasattr(self.observer, 'transcode_complete'):
                await self.observer.transcode_complete()

        return filepath

    # Get a video cop of the YouTube video at a specific resolution
    async def get_video_copy(self, url, streams, resolution, doTranscode, storagePath):
        if url is not None and streams is None:
            streams = get_streams(url)
        elif url is None and streams is None:
            raise NoSourceError

        # Download the audio and video components
        audioPath = await self.get_audio_copy(url, streams, storagePath, True)
        videoPath = await self.get_video_only_copy(url, streams, resolution, doTranscode, storagePath, True)

        # Stitch the components together
        filepath = os.path.join(storagePath, "YouTube-Video.mp4")
        if hasattr(self.observer, 'stitch_commence'):  # Signal to the user that a stitch is commencing
            await self.observer.stitch_commence()
        try:
            stitch_video(audioPath, videoPath, filepath)
        except ffmpeg._run.Error as e:
            print(e)
            print("Could not initialize FFmpeg. Are you sure you have it installed in your Python directory?")
        if hasattr(self.observer, 'stitch_complete'):  # Signal to the user that a stitch is commencing
            await self.observer.stitch_complete()

        return filepath

class NoSourceError(Exception):
    """Raised when the get_[media format] methods are given neither a url nor streams"""
