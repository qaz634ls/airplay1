"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/MediaStreamInfo.java
"""

from enum import Enum

class StreamType(Enum):
    VIDEO = 1

class MediaStreamInfo:
    def __init__(self, stream_type: StreamType):
        self._stream_type = stream_type

    @property
    def stream_type(self) -> StreamType:
        return self._stream_type
