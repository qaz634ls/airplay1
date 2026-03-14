"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/ControlServer.java
"""

import asyncio
import logging
import os
import tempfile
import threading
from typing import Optional

from .....server.AirPlayConfig import AirPlayConfig
from .....server.AirPlayConsumerFactory import AirPlayConsumerFactory
from .handler.control.ControlHandler import ControlHandler, RtspRequest
from .handler.session.SessionManager import SessionManager

log = logging.getLogger(__name__)


# 端口文件路径：系统临时目录下，Python mDNS 侧从此处读取实际端口
PORT_FILE = os.path.join(tempfile.gettempdir(), "airplay-control.port")


class ControlServer:
    """
    TCP server for accepting RTSP/HTTP AirPlay handshake requests.
    Replaces the Netty ServerBootstrap implementation with Python asyncio.
    """

    def __init__(self, air_play_config: AirPlayConfig, consumer_factory: AirPlayConsumerFactory):
        self._air_play_config = air_play_config
        self._consumer_factory = consumer_factory
        self._session_manager = SessionManager(consumer_factory)
        
        self.port = 0
        self._server = None
        self._loop = None
        self._thread: Optional[threading.Thread] = None
        self._control_handler = ControlHandler(self._session_manager, self._air_play_config)

    def start(self) -> None:
        """
        Starts the control server in a dedicated background asyncio thread.
        Halts the calling thread until the server has bound its socket.
        """
        startup_event = threading.Event()

        def run_server():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            
            # Start asyncio server on port 0 to bind a random available port
            coro = asyncio.start_server(self._handle_client, '0.0.0.0', 0)
            self._server = self._loop.run_until_complete(coro)
            
            # Retrieve the randomly assigned port
            self.port = self._server.sockets[0].getsockname()[1]
            log.info("AirPlay control server listening on port: %d", self.port)
            
            self._write_port_file(self.port)
            startup_event.set()
            
            try:
                self._loop.run_forever()
            finally:
                self._server.close()
                self._loop.run_until_complete(self._server.wait_closed())
                self._loop.close()
                self._delete_port_file()
                log.info("AirPlay control server stopped")

        self._thread = threading.Thread(target=run_server, daemon=True)
        self._thread.start()
        
        # Wait until the port is successfully bound
        startup_event.wait()

    def stop(self) -> None:
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
            self._thread = None
            
        self.port = 0

    def _write_port_file(self, port: int) -> None:
        """
        写端口文件：以保证 Python 另一独立进程的 mDNS 服务拿得到真正的端口
        """
        try:
            tmp_file = PORT_FILE + ".tmp"
            with open(tmp_file, 'w', encoding='utf-8') as f:
                f.write(str(port))
            # Rename for atomic write replacement
            if os.name == 'nt' and os.path.exists(PORT_FILE):
                os.replace(tmp_file, PORT_FILE)
            else:
                os.rename(tmp_file, PORT_FILE)
            log.info("端口文件已写入: %s -> port=%d", PORT_FILE, port)
        except Exception as e:
            log.warning("写入端口文件失败: %s, %s", PORT_FILE, e)

    def _delete_port_file(self) -> None:
        try:
            if os.path.exists(PORT_FILE):
                os.remove(PORT_FILE)
                log.info("端口文件已删除: %s", PORT_FILE)
        except Exception as e:
            log.warning("删除端口文件失败: %s, %s", PORT_FILE, e)

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Minimalistic HTTP/RTSP non-blocking parser and dispatcher loop.
        """
        addr = writer.get_extra_info('peername')
        
        try:
            while True:
                # 1. Read Request Line
                request_line = await reader.readline()
                if not request_line:
                    break
                    
                request_line_str = request_line.decode('utf-8').strip()
                if not request_line_str:
                    continue
                    
                parts = request_line_str.split(' ')
                if len(parts) >= 3:
                    method, uri, protocol_version = parts[0], parts[1], parts[2]
                else:
                    method, uri, protocol_version = parts[0], "/", "RTSP/1.0"
                    
                # 2. Read Headers
                headers = {}
                content_length = 0
                while True:
                    header_line = await reader.readline()
                    header_str = header_line.decode('utf-8').strip()
                    if not header_str:
                        break # End of headers
                    
                    if ':' in header_str:
                        k, v = header_str.split(':', 1)
                        k, v = k.strip(), v.strip()
                        headers[k] = v
                        if k.lower() == "content-length":
                            content_length = int(v)

                # 3. Read Content Body
                content = b""
                if content_length > 0:
                    content = await reader.readexactly(content_length)

                # 4. Dispatch using ControlHandler
                rtsp_req = RtspRequest(method, uri, protocol_version, headers, content)
                rtsp_res = self._control_handler.handle_request(rtsp_req)
                
                # 5. Send Response
                # e.g., RTSP/1.0 200 OK
                response_data = bytearray()
                response_data.extend(f"{rtsp_res.protocol_version} {rtsp_res.status_code} {rtsp_res.status_message}\r\n".encode('ascii'))
                
                # We overwrite/set Content-Length based on actual payload
                rtsp_res.headers["Content-Length"] = str(len(rtsp_res.content))
                
                for k, v in rtsp_res.headers.items():
                    response_data.extend(f"{k}: {v}\r\n".encode('ascii'))
                response_data.extend(b"\r\n")
                
                if rtsp_res.content:
                    response_data.extend(rtsp_res.content)
                
                writer.write(response_data)
                await writer.drain()
                
                # In HTTP/1.0 or RTSP without keep-alive, we would close. 
                # Apple AirPlay uses Keep-Alive.
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            log.warning("Control connection aborted for %s: %s", addr, e)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
