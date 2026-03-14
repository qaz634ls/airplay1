"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/AirPlay.java

Responds on pairing setup, fairplay setup requests, decrypts data
"""

from typing import Optional

from .internal.Pairing import Pairing
from .internal.FairPlay import FairPlay
from .internal.RTSP import RTSP
from .internal.FairPlayVideoDecryptor import FairPlayVideoDecryptor
from .MediaStreamInfo import MediaStreamInfo


class AirPlay:
    def __init__(self):
        self._pairing = Pairing()
        self._fairplay = FairPlay()
        self._rtsp = RTSP()
        self._fair_play_video_decryptor: Optional[FairPlayVideoDecryptor] = None

    def pair_setup(self) -> bytes:
        """
        /pair-setup
        Writes EdDSA public key bytes to output stream
        """
        return self._pairing.pair_setup()

    def pair_verify(self, data: bytes) -> bytes:
        """
        /pair-verify
        On first request writes curve25519 public key + encrypted signature bytes to output stream;
        On second request verifies signature
        """
        return self._pairing.pair_verify(data)

    def is_pair_verified(self) -> bool:
        """
        Pair was verified successfully
        """
        return self._pairing.is_pair_verified()

    def fair_play_setup(self, request: bytes) -> bytes:
        """
        /fp-setup
        Writes fp-setup response bytes to output stream
        """
        return self._fairplay.fair_play_setup(request)

    def rtsp_setup(self, request_payload: bytes) -> Optional[MediaStreamInfo]:
        """
        RTSP SETUP
        Sets encrypted EAS key and IV or retrieves media stream info
        """
        return self._rtsp.setup(request_payload)

    def rtsp_teardown(self, request_payload: bytes) -> Optional[MediaStreamInfo]:
        """
        RTSP TEARDOWN
        Retrieves media stream info
        """
        return self._rtsp.teardown(request_payload)

    def get_fair_play_aes_key(self) -> bytes:
        return self._fairplay.decrypt_aes_key(self._rtsp.ekey)

    def is_fair_play_video_decryptor_ready(self) -> bool:
        """
        True if we got shared secret during pairing, ekey & stream connection id during RTSP SETUP
        """
        return (self._pairing.get_shared_secret() is not None and 
                self._rtsp.ekey is not None and 
                self._rtsp.stream_connection_id is not None)

    def decrypt_video(self, video: bytearray) -> None:
        """
        Decrypts a raw AirPlay H.264 video payload in-place using AES-CTR.
        The FairPlayVideoDecryptor is constructed lazily on the first call
        once all prerequisites (shared secret, ekey, streamConnectionID) are available.

        video raw encrypted video bytes — decrypted in-place
        """
        if self._fair_play_video_decryptor is None:
            if not self.is_fair_play_video_decryptor_ready():
                # Prerequisites not yet available; skip decryption for this packet
                return
            
            self._fair_play_video_decryptor = FairPlayVideoDecryptor(
                self.get_fair_play_aes_key(),
                self._pairing.get_shared_secret(),
                self._rtsp.stream_connection_id
            )
            
        self._fair_play_video_decryptor.decrypt(video)
