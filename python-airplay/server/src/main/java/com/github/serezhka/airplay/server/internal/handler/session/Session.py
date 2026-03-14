"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/handler/session/Session.java
"""

from .....lib.AirPlay import AirPlay
from .....server.AirPlayConsumer import AirPlayConsumer

# We can mock importing VideoServer until it's written
from ...VideoServer import VideoServer


class Session:
    """
    Represents an active AirPlay connection session.
    """

    def __init__(self, session_id: str, consumer: AirPlayConsumer):
        self._id = session_id
        self._consumer = consumer
        self._air_play = AirPlay()
        self._video_server = VideoServer(self._air_play)

    @property
    def id(self) -> str:
        return self._id

    @property
    def air_play(self) -> AirPlay:
        return self._air_play

    @property
    def video_server(self) -> VideoServer:
        return self._video_server

    @property
    def consumer(self) -> AirPlayConsumer:
        return self._consumer
