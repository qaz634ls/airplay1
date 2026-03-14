"""
Python rewrite of:
  java-airplay/player/gstreamer/src/main/java/com/github/serezhka/airplay/player/gstreamer/GstPlayerUtils.java

Configures the GStreamer library path on Windows and macOS,
equivalent to the Java JNA-based GstPlayerUtils.configurePaths().
On Linux GStreamer is assumed to already be on the standard library search path.
"""

import os
import sys
import platform


def configure_paths() -> None:
    """
    Equivalent to Java's GstPlayerUtils.configurePaths().

    Windows: resolves GStreamer install from well-known environment variables
             (GSTREAMER_1_0_ROOT_MSVC_X86_64, GSTREAMER_1_0_ROOT_MINGW_X86_64,
              GSTREAMER_1_0_ROOT_X86_64) and prepends <root>\\bin to PATH
             so that the DLLs can be found by gi/PyGObject.
             The 'gstreamer.path' system property is replaced by the
             GSTREAMER_PATH environment variable (or sys.argv override) as
             a Python-idiomatic alternative.

    macOS:   prepends the framework library dir to DYLD_LIBRARY_PATH.

    Linux:   no-op (GStreamer expected to be installed system-wide).
    """
    system = platform.system()

    if system == "Windows":
        gst_path = os.environ.get("GSTREAMER_PATH") or _find_windows_location()
        if gst_path:
            existing_path = os.environ.get("PATH", "")
            os.environ["PATH"] = gst_path + os.pathsep + existing_path

    elif system == "Darwin":
        default_mac_path = "/Library/Frameworks/GStreamer.framework/Libraries/"
        gst_path = os.environ.get("GSTREAMER_PATH", default_mac_path)
        if gst_path:
            existing = os.environ.get("DYLD_LIBRARY_PATH", "").strip()
            if existing:
                os.environ["DYLD_LIBRARY_PATH"] = gst_path + os.pathsep + existing
            else:
                os.environ["DYLD_LIBRARY_PATH"] = gst_path

    # Linux: no action needed


def _find_windows_location() -> str:
    """
    Equivalent to Java's GstPlayerUtils.findWindowsLocation().
    Queries well-known GStreamer environment variable names (64-bit only)
    and returns the first resolved '...\\bin\\' path.
    """
    is_64bit = sys.maxsize > 2**32

    if is_64bit:
        candidate_vars = [
            "GSTREAMER_1_0_ROOT_MSVC_X86_64",
            "GSTREAMER_1_0_ROOT_MINGW_X86_64",
            "GSTREAMER_1_0_ROOT_X86_64",
        ]
        for var in candidate_vars:
            root = os.environ.get(var)
            if root:
                # Append \bin\ as the Java code does
                if root.endswith("\\"):
                    return root + "bin\\"
                else:
                    return root + "\\bin\\"

    return ""
