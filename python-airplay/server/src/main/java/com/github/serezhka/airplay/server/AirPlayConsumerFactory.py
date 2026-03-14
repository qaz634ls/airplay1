"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/AirPlayConsumerFactory.java
"""

from abc import ABC, abstractmethod

from .AirPlayConsumer import AirPlayConsumer


class AirPlayConsumerFactory(ABC):
    """
    Factory for creating per-session AirPlayConsumer instances.
    Each connected device gets its own consumer (e.g. its own video window).
    """

    @abstractmethod
    def create(self, session_id: str) -> AirPlayConsumer:
        """
        Called once per new device connection.
        
        :param session_id: unique session identifier for the connecting device
        :return: a fresh, independent AirPlayConsumer for this session
        """
        pass

    @abstractmethod
    def destroy(self, session_id: str) -> None:
        """
        Called when a device disconnects, so resources can be released.
        
        :param session_id: the session that has ended
        """
        pass
