"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/internal/RTSP.java

Parses RTSP binary property lists (bplist) to extract ekey/eiv or stream info.
"""

import logging
import plistlib
from typing import Optional, Dict, Any

from ..VideoStreamInfo import VideoStreamInfo

log = logging.getLogger(__name__)

class RTSP:
    """
    对应 Java RTSP 类。
    处理 AirPlay 镜像投屏的 RTSP SETUP / TEARDOWN 消息中的二进制 Plist 数据。
    """

    def __init__(self):
        self._ekey: Optional[bytes] = None
        self._eiv: Optional[bytes] = None
        self._stream_connection_id: Optional[str] = None

    def setup(self, rtsp_setup_payload: bytes) -> Optional[Any]:
        """
        对应 Java 的 setup(InputStream rtspSetupPayload)
        
        :param rtsp_setup_payload: RTSP 请求体的二进制 Plist 内容
        :return: VideoStreamInfo 如果有媒体流，否则 None
        """
        setup_dict = plistlib.loads(rtsp_setup_payload)
        
        if "ekey" in setup_dict or "eiv" in setup_dict:
            self._ekey = setup_dict.get("ekey")
            self._eiv = setup_dict.get("eiv")
            log.info("Encrypted AES key: %s, iv: %s", 
                     self._ekey.hex() if self._ekey else "None", 
                     self._eiv.hex() if self._eiv else "None")
            return None
            
        elif "streams" in setup_dict:
            log.debug("RTSP SETUP streams:\n%s", setup_dict)
            return self._get_media_stream_info(setup_dict)
            
        else:
            log.error("Unknown RTSP setup content\n%s", setup_dict)
            return None

    def teardown(self, rtsp_teardown_payload: bytes) -> Optional[Any]:
        """
        对应 Java 的 teardown(InputStream rtspTeardownPayload)
        """
        teardown_dict = plistlib.loads(rtsp_teardown_payload)
        log.debug("RTSP TEARDOWN streams:\n%s", teardown_dict)
        
        if "streams" in teardown_dict:
            return self._get_media_stream_info(teardown_dict)
            
        return None

    def _get_media_stream_info(self, request: Dict[str, Any]) -> Optional[Any]:
        streams = request.get("streams", [])
        if len(streams) > 1:
            log.warning("Request contains more than one stream info")

        if not streams:
            return None

        stream = streams[0]
        stream_type = stream.get("type", -1)

        # 110 signifies video stream
        if stream_type == 110:
            if "streamConnectionID" in stream:
                # Java 代码在此处使用了 Long.toUnsignedString
                conn_id = stream["streamConnectionID"]
                if conn_id < 0:
                    conn_id += (1 << 64)  # 转换为无符号 64 位整数
                self._stream_connection_id = str(conn_id)
            
            return VideoStreamInfo(self._stream_connection_id)
            
        else:
            log.warning("Unsupported or non-video stream type: %s — ignored", stream_type)
            return None

    @property
    def stream_connection_id(self) -> Optional[str]:
        return self._stream_connection_id

    @property
    def ekey(self) -> Optional[bytes]:
        return self._ekey

    @property
    def eiv(self) -> Optional[bytes]:
        return self._eiv
