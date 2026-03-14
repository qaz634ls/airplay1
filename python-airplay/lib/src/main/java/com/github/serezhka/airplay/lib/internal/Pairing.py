"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/internal/Pairing.java

Handles Ed25519 pairing and Curve25519/X25519 ECDH key exchange over /pair-setup and /pair-verify.
"""

import logging
import hashlib

from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from cryptography.exceptions import InvalidSignature

log = logging.getLogger(__name__)

class Pairing:
    """
    对应 Java Pairing 类。
    处理 AirPlay 设备的配对和加密验证。
    """

    def __init__(self):
        # 相当于 Java 的 new KeyPairGenerator().generateKeyPair() (EdDSA)
        self._ed_private_key = ed25519.Ed25519PrivateKey.generate()
        self._ed_public_key = self._ed_private_key.public_key()
        
        self._ed_theirs = None
        self._ecdh_ours = None
        self._ecdh_theirs = None
        self._ecdh_secret = None
        
        self._pair_verified = False

        # 用于保存本轮 X25519 会话密钥以供握手时使用
        self._x25519_private_key = None

    def pair_setup(self) -> bytes:
        """
        对应 Java 的 pairSetup(OutputStream out)
        Returns the raw 32-byte Ed25519 public key.
        """
        return self._ed_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def pair_verify(self, data: bytes) -> bytes:
        """
        对应 Java pairVerify(InputStream request, OutputStream response)
        
        :param data: The request body
        :return: The response body to write back
        """
        flag = data[0]
        # data[1:4] is skipped in Java (request.skip(3))
        payload = data[4:]
        
        if flag > 0:
            # 第一次请求
            if len(payload) < 64:
                raise ValueError("Payload too short for pairVerify flag > 0")

            self._ecdh_theirs = payload[:32]
            self._ed_theirs = payload[32:64]

            # 相当于 Curve25519 curve25519 = Curve25519.getInstance(...)
            self._x25519_private_key = x25519.X25519PrivateKey.generate()
            self._ecdh_ours = self._x25519_private_key.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )

            # 计算 Agreement (Shared Secret)
            theirs_public_key = x25519.X25519PublicKey.from_public_bytes(self._ecdh_theirs)
            self._ecdh_secret = self._x25519_private_key.exchange(theirs_public_key)

            log.info("Shared secret: %s", self._ecdh_secret.hex())

            # Java 初始化 Cipher
            encryptor = self._init_cipher()

            # Data to sign: ecdhOurs + ecdhTheirs
            data_to_sign = self._ecdh_ours + self._ecdh_theirs

            # Ed25519 Sign
            signature = self._ed_private_key.sign(data_to_sign)

            # Encrypt the signature
            encrypted_signature = encryptor.update(signature) + encryptor.finalize()

            # responseContent = ecdhOurs + encryptedSignature
            return self._ecdh_ours + encrypted_signature

        else:
            # 第二次请求 (flag == 0)
            signature = payload[:64]

            encryptor = self._init_cipher()

            # Java 中的做法:
            # aesCtr128Encrypt.update(new byte[64])
            # sigBuffer = aesCtr128Encrypt.doFinal(signature);
            # 这实际上是先跳过 64 字节的 keystream，再用接下来的 keystream 解密 signature。
            # 这是因为 Java 对第一个请求加密后没有保存 cipher state，所以通过 update 64个 null byte 把 counter 推到对齐位置！
            encryptor.update(b'\x00' * 64)
            sig_buffer = encryptor.update(signature) + encryptor.finalize()

            sig_message = self._ecdh_theirs + self._ecdh_ours

            try:
                theirs_ed_pub = ed25519.Ed25519PublicKey.from_public_bytes(self._ed_theirs)
                theirs_ed_pub.verify(sig_buffer, sig_message)
                self._pair_verified = True
            except InvalidSignature:
                self._pair_verified = False

            log.info("Pair verified: %s", self._pair_verified)
            return b""  # 返回空内容，对应原本不再有 response.write

    def is_pair_verified(self) -> bool:
        return self._pair_verified

    def get_shared_secret(self) -> bytes:
        return self._ecdh_secret

    def _init_cipher(self):
        # 提取 AES Key
        h = hashlib.sha512()
        h.update(b"Pair-Verify-AES-Key")
        h.update(self._ecdh_secret)
        aes_key = h.digest()[:16]

        # 提取 AES IV
        h = hashlib.sha512()
        h.update(b"Pair-Verify-AES-IV")
        h.update(self._ecdh_secret)
        aes_iv = h.digest()[:16]

        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CTR(aes_iv),
            backend=default_backend()
        )
        return cipher.encryptor()
