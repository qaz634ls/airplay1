"""
Python rewrite of:
  java-airplay/player/gstreamer/src/main/java/com/github/serezhka/airplay/player/gstreamer/GstPlayer.java

100% equivalent to the original Java implementation.
"""

import logging
import os
from abc import ABC, abstractmethod

from .GstPlayerUtils import configure_paths

# --- GStreamer initialisation (equivalent to Java static block) ---
# GstPlayerUtils.configurePaths()  → configure_paths()
# GLib.setEnv("GST_DEBUG", "3")    → os.environ
# Gst.init(Version.of(1, 10), ...) → Gst.init(None)
configure_paths()
os.environ.setdefault("GST_DEBUG", "3")

try:
    import gi
    gi.require_version("Gst",    "1.0")
    gi.require_version("GstApp", "1.0")
    from gi.repository import Gst, GstApp

    if not Gst.is_initialized():
        Gst.init(None)

    _GST_AVAILABLE = True
except Exception as _gst_import_err:
    logging.warning(
        "PyGObject/GStreamer not available — GstPlayer will NOT function: %s",
        _gst_import_err,
    )
    _GST_AVAILABLE = False

from .....server.AirPlayConsumer import AirPlayConsumer
from .....lib.VideoStreamInfo import VideoStreamInfo

log = logging.getLogger(__name__)


class GstPlayer(AirPlayConsumer, ABC):
    """
    Abstract base class for GStreamer-backed AirPlay video players.
    Subclasses must implement create_h264_pipeline() to supply a concrete
    Gst.Pipeline containing an AppSrc element named "h264-src".

    Mirrors the Java abstract class GstPlayer implements AirPlayConsumer.
    """

    def __init__(self):
        super().__init__()

        # Equivalent to: h264Pipeline = createH264Pipeline();
        self._h264_pipeline = self.create_h264_pipeline()

        # Equivalent to: h264Src = (AppSrc) h264Pipeline.getElementByName("h264-src");
        self._h264_src = self._h264_pipeline.get_by_name("h264-src")
        if self._h264_src is None:
            raise ValueError("Pipeline is missing an AppSrc element named 'h264-src'")

        # h264Src.setStreamType(AppSrc.StreamType.STREAM)
        self._h264_src.set_property("stream-type", GstApp.AppStreamType.STREAM)

        # h264Src.setCaps(Caps.fromString("video/x-h264,..."))
        caps = Gst.Caps.from_string(
            "video/x-h264,colorimetry=bt709,"
            "stream-format=(string)byte-stream,"
            "alignment=(string)au"
        )
        self._h264_src.set_property("caps", caps)

        # h264Src.set("is-live", true)
        self._h264_src.set_property("is-live", True)

        # h264Src.set("format", Format.TIME)
        self._h264_src.set_property("format", Gst.Format.TIME)

        # h264Src.set("emit-signals", true)
        self._h264_src.set_property("emit-signals", True)

    @abstractmethod
    def create_h264_pipeline(self):
        """
        Equivalent to Java's abstract Pipeline createH264Pipeline().
        Must return a Gst.Pipeline containing an AppSrc named "h264-src".
        """
        pass

    # ------------------------------------------------------------------ #
    #  AirPlayConsumer interface                                           #
    # ------------------------------------------------------------------ #

    def on_video_format(self, video_stream_info: VideoStreamInfo) -> None:
        """
        Equivalent to: h264Pipeline.play()
        Called when video stream parameters are known — starts the pipeline.
        """
        self._h264_pipeline.set_state(Gst.State.PLAYING)

    def on_video(self, data: bytes) -> None:
        """
        Equivalent to:
            Buffer buf = new Buffer(bytes.length);
            buf.map(true).put(bytes);
            h264Src.pushBuffer(buf);
        """
        buf = Gst.Buffer.new_wrapped(data)
        self._h264_src.emit("push-buffer", buf)

    def on_video_src_disconnect(self) -> None:
        """
        Equivalent to: h264Pipeline.stop()
        """
        self._h264_pipeline.set_state(Gst.State.NULL)
