"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/AirPlayServer.java
"""

from .AirPlayConfig import AirPlayConfig
from .AirPlayConsumerFactory import AirPlayConsumerFactory
from .internal.ControlServer import ControlServer


class AirPlayServer:
    """
    Main entrypoint for managing the AirPlay server lifecycle.
    """

    def __init__(self, air_play_config: AirPlayConfig, consumer_factory: AirPlayConsumerFactory):
        self._control_server = ControlServer(air_play_config, consumer_factory)

    def start(self) -> None:
        """
        Starts the underlying control server.
        """
        self._control_server.start()

    def stop(self) -> None:
        """
        Stops the underlying control server and cleans up resources.
        """
        self._control_server.stop()
