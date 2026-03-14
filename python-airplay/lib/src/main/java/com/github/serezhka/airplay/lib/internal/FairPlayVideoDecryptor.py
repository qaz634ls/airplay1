"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/internal/FairPlayVideoDecryptor.java

Stateful AES-CTR streaming decryptor for AirPlay H.264 video payloads.
100% faithful port of the Java og/nextDecryptCount half-block management logic.
"""

import hashlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class FairPlayVideoDecryptor:
    """
    Equivalent to Java FairPlayVideoDecryptor.

    The Java original manages cross-packet AES-CTR state using two fields:
      og               : byte[16]  — stores the keystream block for the partial tail
      nextDecryptCount : int       — how many bytes of `og` to apply at packet start

    This Python port faithfully reproduces that exact algorithm so that the
    AES-CTR counter advances by exactly the same number of blocks on each call.
    """

    def __init__(self, aes_key: bytes, shared_secret: bytes, stream_connection_id: str):
        self._aes_key = aes_key
        self._shared_secret = shared_secret
        self._stream_connection_id = stream_connection_id

        # Java: private byte[] og = new byte[16];
        self._og = bytearray(16)

        # Java: private int nextDecryptCount;
        self._next_decrypt_count = 0

        # Java: private final Cipher aesCtrDecrypt;  (stateful)
        self._aes_key_bytes, self._aes_iv_bytes = self._derive_key_iv()
        self._cipher_state = self._new_cipher()

    # ------------------------------------------------------------------
    # private void initAesCtrCipher()
    # ------------------------------------------------------------------
    def _derive_key_iv(self):
        """
        Java initAesCtrCipher() key-derivation chain:
          eaesKey  = SHA-512(aesKey || sharedSecret)
          finalKey = SHA-512("AirPlayStreamKey" + streamConnectionID || eaesKey[0:16])[0:16]
          finalIV  = SHA-512("AirPlayStreamIV"  + streamConnectionID || eaesKey[0:16])[0:16]
        """
        # Step 1
        h = hashlib.sha512()
        h.update(self._aes_key)
        h.update(self._shared_secret)
        eaes_key = h.digest()           # 64 bytes

        # Step 2
        skey = ("AirPlayStreamKey" + self._stream_connection_id).encode("utf-8")
        h = hashlib.sha512()
        h.update(skey)
        h.update(eaes_key[:16])
        hash1 = h.digest()

        # Step 3
        siv = ("AirPlayStreamIV" + self._stream_connection_id).encode("utf-8")
        h = hashlib.sha512()
        h.update(siv)
        h.update(eaes_key[:16])
        hash2 = h.digest()

        return hash1[:16], hash2[:16]

    def _new_cipher(self):
        """Creates a fresh stateful AES-CTR encryptor (encryptor == decryptor in CTR mode)."""
        cipher = Cipher(
            algorithms.AES(self._aes_key_bytes),
            modes.CTR(self._aes_iv_bytes),
            backend=default_backend(),
        )
        return cipher.encryptor()

    # ------------------------------------------------------------------
    # public void decrypt(byte[] video)
    # ------------------------------------------------------------------
    def decrypt(self, video: bytearray) -> None:
        """
        100% faithful port of Java decrypt(byte[] video).

        Java logic:
          1. If nextDecryptCount > 0: XOR the first nextDecryptCount bytes of video
             with the tail of the previously computed og keystream block.
          2. Decrypt the largest 16-byte-aligned chunk of the remaining payload
             in-place using aesCtrDecrypt.update().
          3. If there is a remainder (< 16 bytes), pad it into og[], decrypt
             the full 16-byte og block, copy the relevant bytes back into video,
             and record how many bytes of og are still unused (nextDecryptCount).
        """
        ndc = self._next_decrypt_count

        # --- Step 1: apply leftover keystream from previous packet ---
        # Java: for (int i = 0; i < nextDecryptCount; i++)
        #           video[i] = (byte)(video[i] ^ og[(16 - nextDecryptCount) + i]);
        for i in range(ndc):
            video[i] ^= self._og[(16 - ndc) + i]

        # --- Step 2: decrypt the 16-byte-aligned middle section ---
        # Java: int encryptlen = ((video.length - nextDecryptCount) / 16) * 16;
        #       aesCtrDecrypt.update(video, nextDecryptCount, encryptlen, video, nextDecryptCount);
        encrypt_len = ((len(video) - ndc) // 16) * 16
        if encrypt_len > 0:
            chunk = bytes(video[ndc:ndc + encrypt_len])
            decrypted_chunk = self._cipher_state.update(chunk)
            video[ndc:ndc + encrypt_len] = decrypted_chunk

        # --- Step 3: handle the tail remainder (< 16 bytes) ---
        # Java: int restlen  = (video.length - nextDecryptCount) % 16;
        #       int reststart = video.length - restlen;
        #       nextDecryptCount = 0;
        rest_len = (len(video) - ndc) % 16
        rest_start = len(video) - rest_len
        self._next_decrypt_count = 0

        if rest_len > 0:
            # Java: Arrays.fill(og, (byte) 0);
            #       System.arraycopy(video, reststart, og, 0, restlen);
            #       aesCtrDecrypt.update(og, 0, 16, og, 0);
            #       System.arraycopy(og, 0, video, reststart, restlen);
            #       nextDecryptCount = 16 - restlen;
            self._og[:] = b'\x00' * 16
            self._og[:rest_len] = video[rest_start:rest_start + rest_len]
            decrypted_og = self._cipher_state.update(bytes(self._og))
            self._og[:] = decrypted_og
            video[rest_start:rest_start + rest_len] = self._og[:rest_len]
            self._next_decrypt_count = 16 - rest_len
