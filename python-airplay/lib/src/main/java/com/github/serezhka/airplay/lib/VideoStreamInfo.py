"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/VideoStreamInfo.java

100% equivalent to the original Java class.
"""

from .MediaStreamInfo import MediaStreamInfo, StreamType


class VideoStreamInfo(MediaStreamInfo):
    """
    Holds information about an active AirPlay video stream.
    """

    def __init__(self, stream_connection_id: str):
        # Java: super() implicitly sets StreamType via getStreamType()
        super().__init__(StreamType.VIDEO)
        self._stream_connection_id = stream_connection_id

    @property
    def stream_connection_id(self) -> str:
        """Equivalent to Java getStreamConnectionId()"""
        return self._stream_connection_id

    def __repr__(self) -> str:
        """
        Equivalent to Java toString():
          "VideoStreamInfo{streamConnectionId='...'}"
        """
        return f"VideoStreamInfo{{streamConnectionId='{self._stream_connection_id}'}}"
