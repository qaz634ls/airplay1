"""
Python rewrite of:
  java-airplay/player/app/src/main/java/com/github/serezhka/airplay/app/config/PlayerConfig.java

This module provides configuration and dependency injection for the AirPlay player, 
akin to Spring Boot's @Configuration class.
"""

from typing import Dict, Any

from .....server.AirPlayConfig import AirPlayConfig
from .....server.AirPlayConsumerFactory import AirPlayConsumerFactory
from .....server.AirPlayServer import AirPlayServer
from ....gstreamer.GstPlayerFactory import GstPlayerFactory

class PlayerConfig:
    """
    Manages application configuration, mimicking Spring's @Configuration beans.
    """

    def __init__(self, properties: Dict[str, Any]):
        """
        :param properties: Application configuration properties (like application.properties)
        """
        self._properties = properties

    def air_play_config(self) -> AirPlayConfig:
        """
        Creates and returns the AirPlayConfig from the 'airplay' sub-dict of properties.
        Equivalent to Spring's @ConfigurationProperties(prefix = "airplay") binding.
        """
        airplay_props = self._properties.get("airplay", {})
        return AirPlayConfig.from_dict(airplay_props)

    def gstreamer_consumer_factory(self) -> AirPlayConsumerFactory:
        """
        Creates the AirPlayConsumerFactory if the implementation is gstreamer.
        """
        impl = self._properties.get("player.implementation", "gstreamer")
        use_swing = self._properties.get("player.gstreamer.swing", False)
        
        if impl == "gstreamer":
            return GstPlayerFactory(use_swing)
        else:
            raise ValueError(f"Unsupported player implementation: {impl}")

    def air_play_server(self, air_play_config: AirPlayConfig, consumer_factory: AirPlayConsumerFactory) -> AirPlayServer:
        """
        Creates the AirPlayServer using the provided config and consumer factory.
        """
        return AirPlayServer(air_play_config, consumer_factory)

    def build_server(self) -> AirPlayServer:
        """
        Convenience method to resolve dependencies and build the server instance.
        """
        config = self.air_play_config()
        consumer_factory = self.gstreamer_consumer_factory()
        return self.air_play_server(config, consumer_factory)
