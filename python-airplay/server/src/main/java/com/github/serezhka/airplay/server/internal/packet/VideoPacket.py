"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/packet/VideoPacket.java
"""

class VideoPacket:
    def __init__(self, payload_type: int, payload_size: int, payload: bytes):
        self._payload_type = payload_type
        self._payload_size = payload_size
        self._payload = payload

    @property
    def payload_type(self) -> int:
        return self._payload_type

    @property
    def payload_size(self) -> int:
        return self._payload_size

    @property
    def payload(self) -> bytes:
        return self._payload

    def __repr__(self) -> str:
        return f"VideoPacket(type={self._payload_type}, size={self._payload_size})"
