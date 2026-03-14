"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/AirPlayConsumer.java
"""

from abc import ABC, abstractmethod
from ...lib.VideoStreamInfo import VideoStreamInfo

class AirPlayConsumer(ABC):
    """
    Interface for consuming AirPlay media streams (video/audio).
    """

    @abstractmethod
    def on_video_format(self, video_stream_info: VideoStreamInfo) -> None:
        """
        Called when video format/stream info is available
        """
        pass

    @abstractmethod
    def on_video(self, data: bytes) -> None:
        """
        Called when a frame/chunk of raw h264 video data is received
        """
        pass

    @abstractmethod
    def on_video_src_disconnect(self) -> None:
        """
        Called when the video stream disconnects
        """
        pass
