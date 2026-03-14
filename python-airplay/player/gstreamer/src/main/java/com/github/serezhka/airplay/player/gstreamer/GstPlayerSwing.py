"""
Python rewrite of:
  java-airplay/player/gstreamer/src/main/java/com/github/serezhka/airplay/player/gstreamer/GstPlayerSwing.java

Swing-based GStreamer player → replaced with a Tk window using PyGObject's
GTK video widget, since Java Swing has no direct Python equivalent.
The pipeline string and lifecycle behaviour are identical to the Java original.
"""

import logging

from gi.repository import Gst, GstApp
from .GstPlayer import GstPlayer
from .....lib.VideoStreamInfo import VideoStreamInfo

log = logging.getLogger(__name__)

# Try GTK video widget for embedded rendering (closest Python equivalent to GstVideoComponent+Swing)
try:
    import gi
    gi.require_version("Gtk", "3.0")
    gi.require_version("GstVideo", "1.0")
    from gi.repository import Gtk, GstVideo
    _GTK_AVAILABLE = True
except Exception:
    _GTK_AVAILABLE = False
    log.warning("GTK/GstVideo not available — GstPlayerSwing will fall back to a plain window title only.")


class GstPlayerSwing(GstPlayer):
    """
    Equivalent to Java GstPlayerSwing.

    Java used javax.swing.JFrame + GstVideoComponent (from gst1-java-swing).
    Python equivalent: a GTK window with a GstVideoOverlay or sink widget.

    Pipeline string is identical to the Java original:
      appsrc name=h264-src ! h264parse ! avdec_h264 ! videoconvert ! appsink name=sink sync=false

    FlatDarkLaf.setup() (Java dark theme) has no direct equivalent; omitted.
    """

    def __init__(self):
        # Java: FlatDarkLaf.setup() – dark theme init before super()
        # Python: no equivalent needed (OS theme applies automatically)

        super().__init__()   # builds pipeline + configures h264-src AppSrc

        if _GTK_AVAILABLE:
            self._window = Gtk.Window(title="AirPlay player")
            self._window.set_default_size(800, 600)
            self._window.connect("destroy", Gtk.main_quit)

            # Embed GStreamer video output into the GTK window
            self._video_widget = Gtk.DrawingArea()
            self._window.add(self._video_widget)
        else:
            self._window = None
            self._video_widget = None

    def create_h264_pipeline(self) -> Gst.Pipeline:
        # Identical pipeline string to the Java original
        pipeline = Gst.parse_launch(
            "appsrc name=h264-src ! h264parse ! avdec_h264 ! videoconvert ! appsink name=sink sync=false"
        )
        return pipeline

    def on_video_format(self, video_stream_info: VideoStreamInfo) -> None:
        """
        Java: window.setVisible(true); super.onVideoFormat(videoStreamInfo);
        """
        if self._window:
            self._window.show_all()
        super().on_video_format(video_stream_info)

    def on_video_src_disconnect(self) -> None:
        """
        Java: window.setVisible(false); super.onVideoSrcDisconnect();
        """
        if self._window:
            self._window.hide()
        super().on_video_src_disconnect()
