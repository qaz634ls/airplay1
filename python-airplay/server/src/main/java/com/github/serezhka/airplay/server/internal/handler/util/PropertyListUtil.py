"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/handler/util/PropertyListUtil.java

100% equivalent to the original Java output. All field names, values, and structure are preserved exactly.
"""

import plistlib
from typing import Dict, Any

from .....server.AirPlayConfig import AirPlayConfig


class PropertyListUtil:

    @staticmethod
    def prepare_info_response(air_play_config: AirPlayConfig) -> bytes:
        """
        Equivalent to Java's prepareInfoResponse(AirPlayConfig).
        Uses plistlib to produce the same binary plist as BinaryPropertyListWriter.writeToArray().
        """
        display: Dict[str, Any] = {
            "features":      14,
            "height":        air_play_config.height,
            "heightPhysical": False,
            "heightPixels":  air_play_config.height,
            "maxFPS":        air_play_config.fps,
            "overscanned":   False,
            "refreshRate":   60,
            "rotation":      False,
            "uuid":          "e5f7a68d-7b0f-4305-984b-974f677a150b",
            "width":         air_play_config.width,
            "widthPhysical": False,
            "widthPixels":   air_play_config.width,
        }

        response: Dict[str, Any] = {
            "displays":                [display],
            "features":                130367356919,
            "keepAliveSendStatsAsBody": 1,
            "model":                   "AppleTV3,2",
            "name":                    "Apple TV",       # hardcoded in original Java
            "pi":                      "b08f5a79-db29-4384-b456-a4784d9e6055",
            "sourceVersion":           "220.68",
            "statusFlags":             68,
            "vv":                      2,
        }

        return plistlib.dumps(response, fmt=plistlib.FMT_BINARY)

    @staticmethod
    def prepare_setup_video_response(data_port: int, event_port: int, timing_port: int) -> bytes:
        """
        Equivalent to Java's prepareSetupVideoResponse(int, int, int).
        Produces: streams=[{dataPort, type:110}], eventPort, timingPort
        """
        data_stream: Dict[str, Any] = {
            "dataPort": data_port,
            "type":     110,
        }

        response: Dict[str, Any] = {
            "streams":    [data_stream],
            "eventPort":  event_port,
            "timingPort": timing_port,
        }

        return plistlib.dumps(response, fmt=plistlib.FMT_BINARY)
