"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/handler/control/ControlHandler.java

Generic Controller that processes parsed RTSP/HTTP requests and returns responses.
"""

import logging
from typing import Optional, Dict

from .....server.AirPlayConfig import AirPlayConfig
from .....lib.VideoStreamInfo import VideoStreamInfo
from .session.Session import Session
from .session.SessionManager import SessionManager
from ..util.PropertyListUtil import PropertyListUtil

log = logging.getLogger(__name__)


class RtspRequest:
    def __init__(self, method: str, uri: str, protocol_version: str, headers: Dict[str, str], content: bytes):
        self.method = method
        self.uri = uri
        self.protocol_version = protocol_version
        self.headers = headers
        self.content = content


class RtspResponse:
    def __init__(self, protocol_version: str, status_code: int, status_message: str):
        self.protocol_version = protocol_version
        self.status_code = status_code
        self.status_message = status_message
        self.headers: Dict[str, str] = {}
        self.content = bytearray()


class ControlHandler:
    """
    Counterpart to Netty's ControlHandler.
    Processes parsed RtspRequest objects and generates RtspResponse objects.
    """

    def __init__(self, session_manager: SessionManager, air_play_config: AirPlayConfig):
        self._session_manager = session_manager
        self._air_play_config = air_play_config

    def handle_request(self, request: RtspRequest) -> RtspResponse:
        """
        Main entrypoint replacing Netty's channelRead
        """
        try:
            if request.protocol_version == "RTSP/1.0":
                if request.method == "GET" and request.uri == "/info":
                    return self._handle_get_info(request)
                elif request.method == "POST" and request.uri == "/pair-setup":
                    return self._handle_pair_setup(request)
                elif request.method == "POST" and request.uri == "/pair-verify":
                    return self._handle_pair_verify(request)
                elif request.method == "POST" and request.uri == "/fp-setup":
                    return self._handle_fair_play_setup(request)
                elif request.method == "SETUP":
                    return self._handle_rtsp_setup(request)
                elif request.method == "POST" and request.uri == "/feedback":
                    return self._handle_rtsp_feedback(request)
                elif request.method == "GET_PARAMETER":
                    return self._handle_rtsp_get_parameter(request)
                elif request.method == "RECORD":
                    return self._handle_rtsp_record(request)
                elif request.method == "SET_PARAMETER":
                    return self._handle_rtsp_set_parameter(request)
                elif request.method == "FLUSH":
                    return self._handle_rtsp_flush(request)
                elif request.method == "TEARDOWN":
                    return self._handle_rtsp_teardown(request)
                else:
                    log.error("Unknown control request: %s %s %s", request.protocol_version, request.method, request.uri)
                    response = self._create_rtsp_response(request)
                    response.status_code = 404
                    response.status_message = "Not Found"
                    return response
            else:
                log.warning("Unsupported RTSP version: %s", request.protocol_version)
                return self._create_rtsp_response(request)
                
        except Exception as e:
            log.exception("Error handling control request: %s %s", request.method, request.uri)
            response = self._create_rtsp_response(request)
            response.status_code = 500
            response.status_message = "Internal Server Error"
            return response

    def _resolve_session(self, request: RtspRequest) -> Optional[Session]:
        session_id = request.headers.get("Active-Remote")
        if not session_id:
            session_id = request.headers.get("X-Apple-Session-ID")
        if not session_id:
            return None
        return self._session_manager.get_session(session_id)

    def _handle_get_info(self, request: RtspRequest) -> RtspResponse:
        info_bytes = PropertyListUtil.prepare_info_response(self._air_play_config)
        response = self._create_rtsp_response(request)
        response.content.extend(info_bytes)
        return response

    def _handle_pair_setup(self, request: RtspRequest) -> RtspResponse:
        session = self._resolve_session(request)
        response = self._create_rtsp_response(request)
        setup_res = session.air_play.pair_setup()
        response.content.extend(setup_res)
        return response

    def _handle_pair_verify(self, request: RtspRequest) -> RtspResponse:
        session = self._resolve_session(request)
        response = self._create_rtsp_response(request)
        verify_res = session.air_play.pair_verify(request.content)
        response.content.extend(verify_res)
        return response

    def _handle_fair_play_setup(self, request: RtspRequest) -> RtspResponse:
        session = self._resolve_session(request)
        response = self._create_rtsp_response(request)
        fp_res = session.air_play.fair_play_setup(request.content)
        response.content.extend(fp_res)
        return response

    def _handle_rtsp_setup(self, request: RtspRequest) -> RtspResponse:
        session = self._resolve_session(request)
        consumer = session.consumer
        response = self._create_rtsp_response(request)
        
        media_stream_info = session.air_play.rtsp_setup(request.content)
        if media_stream_info:
            if media_stream_info.stream_type.name == "VIDEO":
                consumer.on_video_format(media_stream_info)
                session.video_server.start(consumer)
                
                # Mock port bindings. Ideally populated from real VideoServer bindings
                # Using 0 if not implemented exactly like Netty ServerSocketChannel
                setup_res = PropertyListUtil.prepare_setup_video_response(
                    session.video_server.port,
                    0,  # Event Port
                    0   # Timing port
                )
                response.content.extend(setup_res)
        
        return response

    def _handle_rtsp_feedback(self, request: RtspRequest) -> RtspResponse:
        return self._create_rtsp_response(request)

    def _handle_rtsp_get_parameter(self, request: RtspRequest) -> RtspResponse:
        content = b"volume: 0.000000\r\n"
        response = self._create_rtsp_response(request)
        response.content.extend(content)
        return response

    def _handle_rtsp_record(self, request: RtspRequest) -> RtspResponse:
        return self._create_rtsp_response(request)

    def _handle_rtsp_set_parameter(self, request: RtspRequest) -> RtspResponse:
        return self._create_rtsp_response(request)

    def _handle_rtsp_flush(self, request: RtspRequest) -> RtspResponse:
        return self._create_rtsp_response(request)

    def _handle_rtsp_teardown(self, request: RtspRequest) -> RtspResponse:
        session = self._resolve_session(request)
        if session:
            consumer = session.consumer
            media_stream_info = session.air_play.rtsp_teardown(request.content)
            
            if media_stream_info:
                if media_stream_info.stream_type.name == "VIDEO":
                    consumer.on_video_src_disconnect()
                    session.video_server.stop()
            else:
                consumer.on_video_src_disconnect()
                session.video_server.stop()
                
            self._session_manager.remove_session(session.id)
            
        return self._create_rtsp_response(request)

    def _create_rtsp_response(self, request: RtspRequest) -> RtspResponse:
        response = RtspResponse("RTSP/1.0", 200, "OK")
        
        c_seq = request.headers.get("CSeq")
        if c_seq:
            response.headers["CSeq"] = c_seq
            response.headers["Server"] = "AirTunes/220.68"
            
        return response
