"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/AirPlayConfig.java

Java original uses Lombok @Data with no defaults — fields are bound from application.properties
via Spring's @ConfigurationProperties(prefix = "airplay").

Python equivalent: plain data class with no defaults (None), to be populated by the caller
just as Spring would bind properties. Convenience classmethod from_dict() mirrors that binding.
"""


class AirPlayConfig:
    """
    Holds AirPlay server configuration.
    Fields map 1-to-1 with the 'airplay.*' keys in application.properties.
    """

    def __init__(self):
        # All fields start as None — caller must populate before use,
        # just as Spring @ConfigurationProperties would.
        self.server_name: str = None   # airplay.serverName
        self.width: int = None         # airplay.width
        self.height: int = None        # airplay.height
        self.fps: int = None           # airplay.fps

    @classmethod
    def from_dict(cls, props: dict) -> "AirPlayConfig":
        """
        Equivalent to Spring's @ConfigurationProperties binding.
        Reads keys with the 'airplay.' prefix removed.

        Expected keys:  serverName, width, height, fps
        """
        config = cls()
        config.server_name = props.get("serverName")
        config.width  = int(props["width"])  if "width"  in props else None
        config.height = int(props["height"]) if "height" in props else None
        config.fps    = int(props["fps"])    if "fps"    in props else None
        return config

    def __repr__(self) -> str:
        return (
            f"AirPlayConfig(serverName={self.server_name!r}, "
            f"width={self.width}, height={self.height}, fps={self.fps})"
        )
