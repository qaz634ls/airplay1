"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/decoder/VideoDecoder.java
"""

import logging
from typing import List

from ..packet.VideoPacket import VideoPacket

log = logging.getLogger(__name__)


class VideoDecoder:
    """
    Counterpart to Netty's ReplayingDecoder for Video.
    Maintains internal byte buffer state to yield VideoPacket objects dynamically as bytes arrive.
    """
    READ_HEADER = 0
    READ_PAYLOAD = 1

    def __init__(self):
        self._state = self.READ_HEADER
        self._buffer = bytearray()
        self._payload_size = 0
        self._payload_type = 0

    def decode(self, data: bytes) -> List[VideoPacket]:
        """
        Consumes new data chunks and returns any completely parsed packets.
        
        :param data: Raw stream bytes incoming from the socket
        :return: A list of assembled VideoPackets
        """
        self._buffer.extend(data)
        packets = []

        while True:
            if self._state == self.READ_HEADER:
                if len(self._buffer) < 128:
                    break
                
                header = self._buffer[:128]
                del self._buffer[:128]
                
                self._payload_size = int.from_bytes(header[0:4], byteorder='little', signed=False)
                self._payload_type = int.from_bytes(header[4:6], byteorder='little', signed=False) & 0xFF
                # Note: other parts of header like option and timestamp exist but are ignored
                
                self._state = self.READ_PAYLOAD

            elif self._state == self.READ_PAYLOAD:
                if len(self._buffer) < self._payload_size:
                    break
                
                payload_data = self._buffer[:self._payload_size]
                del self._buffer[:self._payload_size]
                
                if self._payload_type in (0, 1):
                    packets.append(VideoPacket(self._payload_type, self._payload_size, bytes(payload_data)))
                else:
                    log.info("Video packet with type: %d, length: %d bytes is skipped", 
                             self._payload_type, self._payload_size)
                
                self._state = self.READ_HEADER

        return packets
