"""
Python rewrite of:
  java-airplay/player/gstreamer/src/main/java/com/github/serezhka/airplay/player/gstreamer/GstPlayerDefault.java

Default (non-Swing) GStreamer pipeline: decodes H.264 and renders via autovideosink.
Pipeline string is identical to the Java original.
"""

from gi.repository import Gst
from .GstPlayer import GstPlayer


class GstPlayerDefault(GstPlayer):
    """
    Equivalent to Java GstPlayerDefault.
    Uses the system's default video sink (autovideosink).
    """

    def create_h264_pipeline(self) -> Gst.Pipeline:
        # Identical pipeline string to the Java original:
        # "appsrc name=h264-src ! h264parse ! avdec_h264 ! autovideosink sync=false"
        pipeline = Gst.parse_launch(
            "appsrc name=h264-src ! h264parse ! avdec_h264 ! autovideosink sync=false"
        )
        return pipeline
