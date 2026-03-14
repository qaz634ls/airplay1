"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/handler/video/VideoHandler.java

100% equivalent to the original Java logic.
"""

import logging

from .....lib.AirPlay import AirPlay
from .....server.AirPlayConsumer import AirPlayConsumer
from ...packet.VideoPacket import VideoPacket

log = logging.getLogger(__name__)


class VideoHandler:
    """
    Processes video packets, decrypts them, and converts AVCC-style
    length-prefix NAL units into Annex B start-code NAL units for downstream
    decoders (e.g. GStreamer).
    """

    def __init__(self, air_play: AirPlay, data_consumer: AirPlayConsumer):
        self._air_play = air_play
        self._data_consumer = data_consumer

    def handle_packet(self, packet: VideoPacket) -> None:
        """
        Equivalent to Netty channelRead:
          payloadType 0 → encrypted H.264 picture frame
          payloadType 1 → SPS/PPS parameter-set packet
        """
        try:
            if packet.payload_type == 0:
                # Java: airPlay.decryptVideo(packet.getPayload())
                # Java payload is byte[], mutable — we mirror that with bytearray
                payload = bytearray(packet.payload)
                self._air_play.decrypt_video(payload)
                self._prepare_picture_nal_units(payload)
                self._data_consumer.on_video(bytes(payload))

            elif packet.payload_type == 1:
                sps_pps = self._prepare_sps_pps_nal_units(packet.payload)
                self._data_consumer.on_video(sps_pps)

        except Exception as e:
            log.error("%s", e, exc_info=e)

    def _prepare_picture_nal_units(self, payload: bytearray) -> None:
        """
        Equivalent to Java preparePictureNALUnits(byte[] payload).

        Walks the AVCC-format payload, rewriting each 4-byte length field
        (big-endian) in-place to the standard H.264 Annex B start code
        00 00 00 01.
        """
        idx = 0
        while idx < len(payload):
            # Read 4-byte big-endian NALU length
            nalu_size = (
                (payload[idx]     << 24) |
                (payload[idx + 1] << 16) |
                (payload[idx + 2] <<  8) |
                 payload[idx + 3]
            )

            # Java: if (naluSize == 1) return;
            if nalu_size == 1:
                return

            # Java: if (naluSize > 0) { overwrite header; advance idx }
            if nalu_size > 0:
                payload[idx]     = 0
                payload[idx + 1] = 0
                payload[idx + 2] = 0
                payload[idx + 3] = 1
                idx += nalu_size + 4

            # Java: if (payload.length - naluSize > 4) { log error; return }
            # This check is OUTSIDE the naluSize > 0 block in the original Java.
            if len(payload) - nalu_size > 4:
                log.error("Video packet contains corrupted NAL unit. It might be decrypt error")
                return

    def _prepare_sps_pps_nal_units(self, payload: bytes) -> bytes:
        """
        Equivalent to Java prepareSpsPpsNALUnits(byte[] payload).

        Parses the AVCC/AVC decoder configuration record and emits
        a standard Annex B byte-stream:
          00 00 00 01 <SPS bytes> 00 00 00 01 <PPS bytes>

        Offset layout (matching Java's payloadBuf.readerIndex(6)):
          [0:6]              – skipped header
          [6:8]              – SPS length (unsigned big-endian short)
          [8 : 8+spsLen]     – SPS NAL data
          [8+spsLen]         – PPS count (1 byte, skipped)
          [8+spsLen+1 : +2]  – PPS length (unsigned big-endian short)
          [8+spsLen+3 : ...]  – PPS NAL data
        """
        # Java: payloadBuf.readerIndex(6); short spsLen = payloadBuf.readUnsignedShort()
        sps_len = int.from_bytes(payload[6:8], byteorder='big', signed=False)
        sps     = payload[8 : 8 + sps_len]

        # Java: payloadBuf.skipBytes(1)  // pps count
        pps_offset = 8 + sps_len + 1
        pps_len    = int.from_bytes(payload[pps_offset : pps_offset + 2], byteorder='big', signed=False)
        pps        = payload[pps_offset + 2 : pps_offset + 2 + pps_len]

        # Java: int spsPpsLen = spsLen + ppsLen + 8
        sps_pps_len = sps_len + pps_len + 8
        log.info("SPS PPS length: %d", sps_pps_len)

        sps_pps = bytearray(sps_pps_len)
        sps_pps[0:4]            = b'\x00\x00\x00\x01'
        sps_pps[4 : 4+sps_len]  = sps

        off = 4 + sps_len
        sps_pps[off : off+4]            = b'\x00\x00\x00\x01'
        sps_pps[off+4 : off+4+pps_len]  = pps

        return bytes(sps_pps)
