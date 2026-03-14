"""
Python rewrite of:
  java-airplay/player/gstreamer/src/main/java/com/github/serezhka/airplay/player/gstreamer/GstPlayerFactory.java

Factory that creates one independent GstPlayer window per connected device.
Supports up to 10 simultaneous AirPlay screen mirroring sessions.
"""

import logging
from typing import Dict

from .....server.AirPlayConsumer import AirPlayConsumer
from .....server.AirPlayConsumerFactory import AirPlayConsumerFactory
from .GstPlayerDefault import GstPlayerDefault
from .GstPlayerSwing import GstPlayerSwing

log = logging.getLogger(__name__)


class GstPlayerFactory(AirPlayConsumerFactory):
    """
    Equivalent to Java GstPlayerFactory implements AirPlayConsumerFactory.

    Creates one GstPlayer per AirPlay session (device connection).
    useSwing=True  → GstPlayerSwing  (GTK embedded window in Python)
    useSwing=False → GstPlayerDefault (autovideosink, system default)
    """

    def __init__(self, use_swing: bool = False):
        self._use_swing = use_swing
        # Java: ConcurrentHashMap → Python dict + thread safety via GIL
        # (dict operations are atomic in CPython due to GIL)
        self._players: Dict[str, AirPlayConsumer] = {}

    def create(self, session_id: str) -> AirPlayConsumer:
        """
        Java: AirPlayConsumer player = useSwing ? new GstPlayerSwing() : new GstPlayerDefault();
        """
        log.info("New AirPlay session [%s]: creating dedicated video window", session_id)
        player: AirPlayConsumer = GstPlayerSwing() if self._use_swing else GstPlayerDefault()
        self._players[session_id] = player
        return player

    def destroy(self, session_id: str) -> None:
        """
        Java: players.remove(sessionId)  — onVideoSrcDisconnect already stops the pipeline.
        """
        player = self._players.pop(session_id, None)
        if player is not None:
            log.info("AirPlay session [%s] ended: releasing video window", session_id)
            # onVideoSrcDisconnect already stops the pipeline; nothing else to do here.
