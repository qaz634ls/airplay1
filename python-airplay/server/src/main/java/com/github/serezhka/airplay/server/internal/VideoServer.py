"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/VideoServer.java
"""

import asyncio
import logging
import threading
from typing import Optional

from ....lib.AirPlay import AirPlay
from ....server.AirPlayConsumer import AirPlayConsumer
from .decoder.VideoDecoder import VideoDecoder
from .handler.video.VideoHandler import VideoHandler

log = logging.getLogger(__name__)


class VideoServer:
    """
    TCP server for accepting H.264 video payload streams.
    Replaces the bulky Netty implementation with Python's built-in asyncio server.
    """

    def __init__(self, air_play: AirPlay):
        self._air_play = air_play
        self._air_play_consumer: Optional[AirPlayConsumer] = None
        
        self.port = 0
        self._server = None
        self._loop = None
        self._thread: Optional[threading.Thread] = None

    def start(self, air_play_consumer: AirPlayConsumer) -> None:
        """
        Starts the video streaming server in a dedicated background asyncio thread.
        """
        self._air_play_consumer = air_play_consumer
        startup_event = threading.Event()

        def run_server():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            
            # Start asyncio server on port 0 to bind a random available port
            coro = asyncio.start_server(self._handle_client, '0.0.0.0', 0)
            self._server = self._loop.run_until_complete(coro)
            
            # Retrieve the randomly assigned port
            self.port = self._server.sockets[0].getsockname()[1]
            log.info("AirPlay video server listening on port: %d", self.port)
            
            startup_event.set()
            
            try:
                self._loop.run_forever()
            finally:
                self._server.close()
                self._loop.run_until_complete(self._server.wait_closed())
                self._loop.close()
                log.info("AirPlay video server stopped")

        self._thread = threading.Thread(target=run_server, daemon=True)
        self._thread.start()
        
        # Wait until the port is successfully bound
        startup_event.wait()

    def stop(self) -> None:
        self._air_play_consumer = None
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
            self._thread = None
            
        self.port = 0

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Handles an incoming video stream TCP connection.
        """
        addr = writer.get_extra_info('peername')
        log.info("Video stream connection established from: %s", addr)
        
        decoder = VideoDecoder()
        handler = VideoHandler(self._air_play, self._air_play_consumer)
        
        try:
            while True:
                data = await reader.read(65536)
                if not data:
                    break
                    
                # Decode raw stream bytes into VideoPacket objects
                packets = decoder.decode(data)
                
                # Pass completely parsed packets to the payload handler
                for packet in packets:
                    handler.handle_packet(packet)
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            log.error("Video stream error for %s: %s", addr, e)
        finally:
            log.info("Video stream connection closed from: %s", addr)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
