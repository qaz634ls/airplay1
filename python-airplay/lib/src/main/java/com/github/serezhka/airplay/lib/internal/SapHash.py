"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/internal/SapHash.java
"""

import struct
from .HandGarble import HandGarble

class SapHash:
    """
    Java SapHash.java Python counterpart.
    Performs hashing of SAP payloads using HandGarble.
    """

    def __init__(self):
        self._hand_garble = HandGarble()

    def _rol8(self, input_val: int, count: int) -> int:
        input_val &= 0xFF
        count &= 7
        return ((input_val << count) & 0xFF) | (input_val >> (8 - count))

    def sap_hash(self, block_in: bytes, key_out: bytearray) -> None:
        buffer0 = bytearray([x & 0xFF for x in [-106, 95, -58, 83, -8, 70, -52, 24, -33, -66, -78, -8, 56, -41, -20, 34, 3, -47, 32, -113]])
        buffer1 = bytearray(210)
        buffer2 = bytearray([x & 0xFF for x in [67, 84, 98, 122, 24, -61, -42, -77, -102, 86, -10, 28, 20, 63, 12, 29, 59, 54, -125, -79, 57, 81, 74, -86, 9, 62, -2, 68, -81, -34, -61, 32, -99, 66, 58]])
        buffer3 = bytearray(132)
        buffer4 = bytearray([x & 0xFF for x in [-19, 37, -47, -69, -68, 39, -97, 2, -94, -87, 17, 0, 12, -77, 82, -64, -67, -29, 27, 73, -57]])
        
        i0_index = [18, 22, 23, 0, 5, 19, 32, 31, 10, 21, 30]

        # Load the input into the buffer
        for i in range(210):
            # We need to swap the byte order around so it is the right endianness
            word_idx = ((i % 64) >> 2) * 4
            in_word = struct.unpack('<I', block_in[word_idx:word_idx+4])[0]
            in_byte = (in_word >> ((3 - (i % 4)) << 3)) & 0xFF
            buffer1[i] = in_byte

        # Next a scrambling
        for i in range(840):
            # We have to do unsigned, 32-bit modulo, or we get the wrong indices
            x = buffer1[((i - 155) & 0xFFFFFFFF) % 210]
            y = buffer1[((i - 57) & 0xFFFFFFFF) % 210]
            z = buffer1[((i - 13) & 0xFFFFFFFF) % 210]
            w = buffer1[(i & 0xFFFFFFFF) % 210]
            buffer1[i % 210] = (self._rol8(y, 5) + (self._rol8(z, 3) ^ w) - self._rol8(x, 7)) & 0xFF

        # Garble!
        self._hand_garble.garble(buffer0, buffer1, buffer2, buffer3, buffer4)

        # Fill the output with 0xE1
        for i in range(16):
            key_out[i] = 0xE1

        # Now we use all the buffers we have calculated to grind out the output. First buffer3
        for i in range(11):
            if i == 3:
                key_out[i] = 0x3d
            else:
                key_out[i] = (key_out[i] + buffer3[i0_index[i] * 4]) & 0xFF

        # Then buffer0
        for i in range(20):
            key_out[i % 16] ^= buffer0[i]

        # Then buffer2
        for i in range(35):
            key_out[i % 16] ^= buffer2[i]

        # Do buffer1
        for i in range(210):
            key_out[i % 16] ^= buffer1[i]

        # Now we do a kind of reverse-scramble
        for j in range(16):
            for i in range(16):
                x = key_out[((i - 7) & 0xFFFFFFFF) % 16]
                y = key_out[i % 16]
                z = key_out[((i - 37) & 0xFFFFFFFF) % 16]
                w = key_out[((i - 177) & 0xFFFFFFFF) % 16]
                key_out[i] = (self._rol8(x, 1) ^ y ^ self._rol8(z, 6) ^ self._rol8(w, 5)) & 0xFF
