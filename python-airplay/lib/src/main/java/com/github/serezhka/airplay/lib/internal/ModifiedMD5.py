"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/internal/ModifiedMD5.java

A custom modified MD5 hash. Different from standard MD5:
    - It parses message chunks as BIG_ENDIAN words (instead of LITTLE_ENDIAN)
    - It introduces a random byte-block swap step during MD5 round 31.
"""

import struct


class ModifiedMD5:
    """
    对应 Java ModifiedMD5 类。
    """

    _SHIFT = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    # Precalculated T[i] constants: floor(abs(sin(i+1)) * 2^32)
    _T = [
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
    ]

    def modified_md5(self, original_block_in: bytes, key_in: bytes, key_out: bytearray) -> None:
        """
        :param original_block_in: read-only bytes buffer, size >= 64
        :param key_in: read-only bytes buffer, size >= 16
        :param key_out: writable bytearray, size >= 16
        """
        block_in = bytearray(64)
        block_in[:64] = original_block_in[:64]

        # keyIn parsed as Little-Endian
        A0, B0, C0, D0 = struct.unpack("<IIII", key_in[:16])
        A, B, C, D = A0, B0, C0, D0

        for i in range(64):
            if i < 16:
                j = i
            elif i < 32:
                j = (5 * i + 1) % 16
            elif i < 48:
                j = (3 * i + 5) % 16
            else:
                j = (7 * i) % 16

            input_val = (block_in[4 * j] << 24) | (block_in[4 * j + 1] << 16) | \
                        (block_in[4 * j + 2] << 8) | block_in[4 * j + 3]

            Z = (A + input_val + self._T[i]) & 0xFFFFFFFF
            
            if i < 16:
                Z = self._rol(Z + self._F(B, C, D), self._SHIFT[i])
            elif i < 32:
                Z = self._rol(Z + self._G(B, C, D), self._SHIFT[i])
            elif i < 48:
                Z = self._rol(Z + self._H(B, C, D), self._SHIFT[i])
            else:
                Z = self._rol(Z + self._I(B, C, D), self._SHIFT[i])

            Z = (Z + B) & 0xFFFFFFFF

            tmp = D
            D = C
            C = B
            B = Z
            A = tmp

            if i == 31:
                self._swap(block_in, 4 * (A & 15), 4 * (B & 15))
                self._swap(block_in, 4 * (C & 15), 4 * (D & 15))
                self._swap(block_in, 4 * ((A >> 4) & 15), 4 * ((B >> 4) & 15))
                self._swap(block_in, 4 * ((A >> 8) & 15), 4 * ((B >> 8) & 15))
                self._swap(block_in, 4 * ((A >> 12) & 15), 4 * ((B >> 12) & 15))

        # Write out updated keys as Little-Endian
        key_out[:16] = struct.pack("<IIII",
                                   (A0 + A) & 0xFFFFFFFF,
                                   (B0 + B) & 0xFFFFFFFF,
                                   (C0 + C) & 0xFFFFFFFF,
                                   (D0 + D) & 0xFFFFFFFF)

    @staticmethod
    def _F(B: int, C: int, D: int) -> int:
        return (B & C) | ((~B & 0xFFFFFFFF) & D)

    @staticmethod
    def _G(B: int, C: int, D: int) -> int:
        return (B & D) | (C & (~D & 0xFFFFFFFF))

    @staticmethod
    def _H(B: int, C: int, D: int) -> int:
        return B ^ C ^ D

    @staticmethod
    def _I(B: int, C: int, D: int) -> int:
        return C ^ (B | (~D & 0xFFFFFFFF))

    @staticmethod
    def _rol(input_val: int, count: int) -> int:
        input_val &= 0xFFFFFFFF
        return ((input_val << count) & 0xFFFFFFFF) | (input_val >> (32 - count))

    @staticmethod
    def _swap(arr: bytearray, idx_a: int, idx_b: int) -> None:
        """
        Swaps two 4-byte chunks in bytearray.
        """
        temp = arr[idx_a:idx_a + 4]
        arr[idx_a:idx_a + 4] = arr[idx_b:idx_b + 4]
        arr[idx_b:idx_b + 4] = temp
