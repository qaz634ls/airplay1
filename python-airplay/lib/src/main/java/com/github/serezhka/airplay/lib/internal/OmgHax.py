"""
Python rewrite of:
  java-airplay/lib/src/main/java/com/github/serezhka/airplay/lib/internal/OmgHax.java
"""

import struct
from . import OmgHaxConst as consts
from .ModifiedMD5 import ModifiedMD5
from .SapHash import SapHash


class OmgHax:
    def __init__(self):
        self._modified_md5 = ModifiedMD5()
        # SapHash will be implemented later, assuming it's imported
        self._sap_hash = SapHash()

    def decrypt_aes_key(self, message3: bytes, cipher_text: bytes, key_out: bytearray) -> None:
        chunk1 = bytes(cipher_text[16:])
        chunk2 = bytes(cipher_text[56:])
        block_in = bytearray(16)
        sap_key = bytearray(16)
        key_schedule = [[0]*4 for _ in range(11)]
        
        self.generate_session_key(consts.default_sap, message3, sap_key)
        self.generate_key_schedule(sap_key, key_schedule)
        self._z_xor(chunk2, block_in, 1)
        self.cycle(block_in, key_schedule)
        
        for i in range(16):
            key_out[i] = (block_in[i] ^ chunk1[i]) & 0xFF
            
        self._x_xor(key_out, key_out, 1)
        self._z_xor(key_out, key_out, 1)

    def decrypt_message(self, message_in: bytes, decrypted_message: bytearray) -> None:
        buffer = bytearray(16)
        mode = message_in[12] & 0xFF  # 0,1,2,3

        for i in range(8):
            for j in range(16):
                if mode == 3:
                    buffer[j] = message_in[(0x80 - 0x10 * i) + j]
                elif mode in (2, 1, 0):
                    buffer[j] = message_in[(0x10 * (i + 1)) + j]

            for j in range(9):
                base = 0x80 - 0x10 * j

                buffer[0x0] = self._msg_tbl_idx(base + 0x0)[buffer[0x0]] ^ consts.message_key[mode][base + 0x0]
                buffer[0x4] = self._msg_tbl_idx(base + 0x4)[buffer[0x4]] ^ consts.message_key[mode][base + 0x4]
                buffer[0x8] = self._msg_tbl_idx(base + 0x8)[buffer[0x8]] ^ consts.message_key[mode][base + 0x8]
                buffer[0xc] = self._msg_tbl_idx(base + 0xc)[buffer[0xc]] ^ consts.message_key[mode][base + 0xc]

                tmp = buffer[0x0d]
                buffer[0xd] = self._msg_tbl_idx(base + 0xd)[buffer[0x9]] ^ consts.message_key[mode][base + 0xd]
                buffer[0x9] = self._msg_tbl_idx(base + 0x9)[buffer[0x5]] ^ consts.message_key[mode][base + 0x9]
                buffer[0x5] = self._msg_tbl_idx(base + 0x5)[buffer[0x1]] ^ consts.message_key[mode][base + 0x5]
                buffer[0x1] = self._msg_tbl_idx(base + 0x1)[tmp] ^ consts.message_key[mode][base + 0x1]

                tmp = buffer[0x02]
                buffer[0x2] = self._msg_tbl_idx(base + 0x2)[buffer[0xa]] ^ consts.message_key[mode][base + 0x2]
                buffer[0xa] = self._msg_tbl_idx(base + 0xa)[tmp] ^ consts.message_key[mode][base + 0xa]
                
                tmp = buffer[0x06]
                buffer[0x6] = self._msg_tbl_idx(base + 0x6)[buffer[0xe]] ^ consts.message_key[mode][base + 0x6]
                buffer[0xe] = self._msg_tbl_idx(base + 0xe)[tmp] ^ consts.message_key[mode][base + 0xe]

                tmp = buffer[0x3]
                buffer[0x3] = self._msg_tbl_idx(base + 0x3)[buffer[0x7]] ^ consts.message_key[mode][base + 0x3]
                buffer[0x7] = self._msg_tbl_idx(base + 0x7)[buffer[0xb]] ^ consts.message_key[mode][base + 0x7]
                buffer[0xb] = self._msg_tbl_idx(base + 0xb)[buffer[0xf]] ^ consts.message_key[mode][base + 0xb]
                buffer[0xf] = self._msg_tbl_idx(base + 0xf)[tmp] ^ consts.message_key[mode][base + 0xf]

                t0 = (consts.table_s9[0x000 + buffer[0x0]] ^ consts.table_s9[0x100 + buffer[0x1]] ^ consts.table_s9[0x200 + buffer[0x2]] ^ consts.table_s9[0x300 + buffer[0x3]]) & 0xFFFFFFFF
                t1 = (consts.table_s9[0x000 + buffer[0x4]] ^ consts.table_s9[0x100 + buffer[0x5]] ^ consts.table_s9[0x200 + buffer[0x6]] ^ consts.table_s9[0x300 + buffer[0x7]]) & 0xFFFFFFFF
                t2 = (consts.table_s9[0x000 + buffer[0x8]] ^ consts.table_s9[0x100 + buffer[0x9]] ^ consts.table_s9[0x200 + buffer[0xa]] ^ consts.table_s9[0x300 + buffer[0xb]]) & 0xFFFFFFFF
                t3 = (consts.table_s9[0x000 + buffer[0xc]] ^ consts.table_s9[0x100 + buffer[0xd]] ^ consts.table_s9[0x200 + buffer[0xe]] ^ consts.table_s9[0x300 + buffer[0xf]]) & 0xFFFFFFFF

                buffer[:16] = struct.pack('<IIII', t0, t1, t2, t3)

            buffer[0x0] = consts.table_s10[(0x0 << 8) + buffer[0x0]]
            buffer[0x4] = consts.table_s10[(0x4 << 8) + buffer[0x4]]
            buffer[0x8] = consts.table_s10[(0x8 << 8) + buffer[0x8]]
            buffer[0xc] = consts.table_s10[(0xc << 8) + buffer[0xc]]

            tmp = buffer[0x0d]
            buffer[0xd] = consts.table_s10[(0xd << 8) + buffer[0x9]]
            buffer[0x9] = consts.table_s10[(0x9 << 8) + buffer[0x5]]
            buffer[0x5] = consts.table_s10[(0x5 << 8) + buffer[0x1]]
            buffer[0x1] = consts.table_s10[(0x1 << 8) + tmp]

            tmp = buffer[0x02]
            buffer[0x2] = consts.table_s10[(0x2 << 8) + buffer[0xa]]
            buffer[0xa] = consts.table_s10[(0xa << 8) + tmp]
            tmp = buffer[0x06]
            buffer[0x6] = consts.table_s10[(0x6 << 8) + buffer[0xe]]
            buffer[0xe] = consts.table_s10[(0xe << 8) + tmp]

            tmp = buffer[0x3]
            buffer[0x3] = consts.table_s10[(0x3 << 8) + buffer[0x7]]
            buffer[0x7] = consts.table_s10[(0x7 << 8) + buffer[0xb]]
            buffer[0xb] = consts.table_s10[(0xb << 8) + buffer[0xf]]
            buffer[0xf] = consts.table_s10[(0xf << 8) + tmp]

            xor_result = bytearray(16)
            if mode in (2, 1, 0):
                if i > 0:
                    self._xor_blocks(buffer, message_in[0x10 * i : 0x10 * i + 16], xor_result)
                else:
                    self._xor_blocks(buffer, consts.message_iv[mode], xor_result)
                decrypted_message[0x10 * i : 0x10 * i + 16] = xor_result
            else:
                if i < 7:
                    offs = 0x70 - 0x10 * i
                    self._xor_blocks(buffer, message_in[offs : offs + 16], xor_result)
                    decrypted_message[offs : offs + 16] = xor_result
                else:
                    offs = 0x70 - 0x10 * i
                    self._xor_blocks(buffer, consts.message_iv[mode], xor_result)
                    decrypted_message[offs : offs + 16] = xor_result

    def generate_key_schedule(self, key_material: bytes, key_schedule: list[list[int]]) -> None:
        key_data = [0] * 4
        for i in range(11):
            key_schedule[i][0] = 0xdeadbeef
            key_schedule[i][1] = 0xdeadbeef
            key_schedule[i][2] = 0xdeadbeef
            key_schedule[i][3] = 0xdeadbeef
            
        buffer = bytearray(16)
        ti = 0
        self._t_xor(key_material, buffer)

        key_data[0:4] = list(struct.unpack('<IIII', buffer))

        for round_idx in range(11):
            key_schedule[round_idx][0] = key_data[0]
            t1 = self._tbl_idx(ti)
            t2 = self._tbl_idx(ti + 1)
            t3 = self._tbl_idx(ti + 2)
            t4 = self._tbl_idx(ti + 3)
            ti += 4

            buffer[0] = (buffer[0] ^ t1[buffer[0x0d]] ^ consts.index_mangle[round_idx]) & 0xFF
            buffer[1] = (buffer[1] ^ t2[buffer[0x0e]]) & 0xFF
            buffer[2] = (buffer[2] ^ t3[buffer[0x0f]]) & 0xFF
            buffer[3] = (buffer[3] ^ t4[buffer[0x0c]]) & 0xFF

            key_data[0] = struct.unpack('<I', buffer[0:4])[0]

            key_schedule[round_idx][1] = key_data[1]
            key_data[1] ^= key_data[0]
            key_data[1] &= 0xFFFFFFFF
            buffer[4:8] = struct.pack('<I', key_data[1])

            key_schedule[round_idx][2] = key_data[2]
            key_data[2] ^= key_data[1]
            key_data[2] &= 0xFFFFFFFF
            buffer[8:12] = struct.pack('<I', key_data[2])

            key_schedule[round_idx][3] = key_data[3]
            key_data[3] ^= key_data[2]
            key_data[3] &= 0xFFFFFFFF
            buffer[12:16] = struct.pack('<I', key_data[3])

    def generate_session_key(self, old_sap: bytes, message_in: bytes, session_key: bytearray) -> None:
        decrypted_message = bytearray(128)
        new_sap = bytearray(320)
        md5 = bytearray(16)

        self.decrypt_message(message_in, decrypted_message)

        new_sap[0:0x11] = consts.static_source_1[:0x11]
        new_sap[0x11:0x11+0x80] = decrypted_message[:0x80]
        new_sap[0x091:0x091+0x80] = old_sap[0x80:0x80+0x80]
        new_sap[0x111:0x111+0x2f] = consts.static_source_2[:0x2f]
        
        session_key[:16] = consts.initial_session_key[:16]

        for round_idx in range(5):
            base = new_sap[round_idx * 64 :]
            self._modified_md5.modified_md5(base, session_key, md5)
            self._sap_hash.sap_hash(base, session_key)
            
            s_ints = list(struct.unpack('<IIII', session_key))
            m_ints = list(struct.unpack('<IIII', md5))
            for i in range(4):
                s_ints[i] = (s_ints[i] + m_ints[i]) & 0xFFFFFFFF
            session_key[:16] = struct.pack('<IIII', *s_ints)

        # Swaps
        for i in range(0, 16, 4):
            tmp = session_key[i]
            session_key[i] = session_key[i + 3]
            session_key[i + 3] = tmp
            tmp = session_key[i + 1]
            session_key[i + 1] = session_key[i + 2]
            session_key[i + 2] = tmp

        # XOR 121
        for i in range(16):
            session_key[i] ^= 121

    def cycle(self, block: bytearray, key_schedule: list[list[int]]) -> None:
        b_ints = list(struct.unpack('<IIII', block))
        b_ints[0] = (b_ints[0] ^ key_schedule[10][0]) & 0xFFFFFFFF
        b_ints[1] = (b_ints[1] ^ key_schedule[10][1]) & 0xFFFFFFFF
        b_ints[2] = (b_ints[2] ^ key_schedule[10][2]) & 0xFFFFFFFF
        b_ints[3] = (b_ints[3] ^ key_schedule[10][3]) & 0xFFFFFFFF
        block[:16] = struct.pack('<IIII', *b_ints)

        self._permute_block_1(block)

        for round_idx in range(9):
            key = struct.pack('<IIII', *key_schedule[9 - round_idx])

            ptr1 = consts.table_s5[block[3] ^ key[3]]
            ptr2 = consts.table_s6[block[2] ^ key[2]]
            ptr3 = consts.table_s8[block[0] ^ key[0]]
            ptr4 = consts.table_s7[block[1] ^ key[1]]
            ab_0 = ptr1 ^ ptr2 ^ ptr3 ^ ptr4

            ptr2 = consts.table_s5[block[7] ^ key[7]]
            ptr1 = consts.table_s6[block[6] ^ key[6]]
            ptr4 = consts.table_s7[block[5] ^ key[5]]
            ptr3 = consts.table_s8[block[4] ^ key[4]]
            ab_1 = ptr1 ^ ptr2 ^ ptr3 ^ ptr4

            ab_2 = (consts.table_s5[block[11] ^ key[11]] ^
                    consts.table_s6[block[10] ^ key[10]] ^
                    consts.table_s7[block[9] ^ key[9]] ^
                    consts.table_s8[block[8] ^ key[8]])

            ab_3 = (consts.table_s5[block[15] ^ key[15]] ^
                    consts.table_s6[block[14] ^ key[14]] ^
                    consts.table_s7[block[13] ^ key[13]] ^
                    consts.table_s8[block[12] ^ key[12]])

            block[:16] = struct.pack('<IIII', ab_0, ab_1, ab_2, ab_3)
            self._permute_block_2(block, 8 - round_idx)

        b_ints = list(struct.unpack('<IIII', block))
        b_ints[0] = (b_ints[0] ^ key_schedule[0][0]) & 0xFFFFFFFF
        b_ints[1] = (b_ints[1] ^ key_schedule[0][1]) & 0xFFFFFFFF
        b_ints[2] = (b_ints[2] ^ key_schedule[0][2]) & 0xFFFFFFFF
        b_ints[3] = (b_ints[3] ^ key_schedule[0][3]) & 0xFFFFFFFF
        block[:16] = struct.pack('<IIII', *b_ints)

    def _xor_blocks(self, a: bytes, b: bytes, out: bytearray) -> None:
        for i in range(16):
            out[i] = a[i] ^ b[i]

    def _z_xor(self, in_bytes: bytes, out: bytearray, blocks: int) -> None:
        for j in range(blocks):
            for i in range(16):
                out[j * 16 + i] = in_bytes[j * 16 + i] ^ consts.z_key[i]

    def _x_xor(self, in_bytes: bytes, out: bytearray, blocks: int) -> None:
        for j in range(blocks):
            for i in range(16):
                out[j * 16 + i] = in_bytes[j * 16 + i] ^ consts.x_key[i]

    def _t_xor(self, in_bytes: bytes, out: bytearray) -> None:
        for i in range(16):
            out[i] = in_bytes[i] ^ consts.t_key[i]

    def _tbl_idx(self, i: int) -> bytes:
        idx = ((31 * i) % 0x28) << 8
        return consts.table_s1[idx:]

    def _msg_tbl_idx(self, i: int) -> bytes:
        idx = ((97 * i) % 144) << 8
        return consts.table_s2[idx:]

    def _permute_block_1(self, block: bytearray) -> None:
        b0 = consts.table_s3[block[0]]
        b4 = consts.table_s3[0x400 + block[4]]
        b8 = consts.table_s3[0x800 + block[8]]
        b12 = consts.table_s3[0xc00 + block[12]]

        tmp = block[13]
        b13 = consts.table_s3[0x100 + block[9]]
        b9 = consts.table_s3[0xd00 + block[5]]
        b5 = consts.table_s3[0x900 + block[1]]
        b1 = consts.table_s3[0x500 + tmp]

        tmp = block[2]
        b2 = consts.table_s3[0xa00 + block[10]]
        b10 = consts.table_s3[0x200 + tmp]
        
        tmp = block[6]
        b6 = consts.table_s3[0xe00 + block[14]]
        b14 = consts.table_s3[0x600 + tmp]

        tmp = block[3]
        b3 = consts.table_s3[0xf00 + block[7]]
        b7 = consts.table_s3[0x300 + block[11]]
        b11 = consts.table_s3[0x700 + block[15]]
        b15 = consts.table_s3[0xb00 + tmp]

        block[0] = b0
        block[1] = b1
        block[2] = b2
        block[3] = b3
        block[4] = b4
        block[5] = b5
        block[6] = b6
        block[7] = b7
        block[8] = b8
        block[9] = b9
        block[10] = b10
        block[11] = b11
        block[12] = b12
        block[13] = b13
        block[14] = b14
        block[15] = b15

    def _permute_tbl_2(self, i: int) -> bytes:
        idx = ((71 * i) % 144) << 8
        return consts.table_s4[idx:]

    def _permute_block_2(self, block: bytearray, round_idx: int) -> None:
        b0 = self._permute_tbl_2(round_idx * 16 + 0)[block[0]]
        b4 = self._permute_tbl_2(round_idx * 16 + 4)[block[4]]
        b8 = self._permute_tbl_2(round_idx * 16 + 8)[block[8]]
        b12 = self._permute_tbl_2(round_idx * 16 + 12)[block[12]]

        tmp = block[13]
        b13 = self._permute_tbl_2(round_idx * 16 + 13)[block[9]]
        b9 = self._permute_tbl_2(round_idx * 16 + 9)[block[5]]
        b5 = self._permute_tbl_2(round_idx * 16 + 5)[block[1]]
        b1 = self._permute_tbl_2(round_idx * 16 + 1)[tmp]

        tmp = block[2]
        b2 = self._permute_tbl_2(round_idx * 16 + 2)[block[10]]
        b10 = self._permute_tbl_2(round_idx * 16 + 10)[tmp]
        
        tmp = block[6]
        b6 = self._permute_tbl_2(round_idx * 16 + 6)[block[14]]
        b14 = self._permute_tbl_2(round_idx * 16 + 14)[tmp]

        tmp = block[3]
        b3 = self._permute_tbl_2(round_idx * 16 + 3)[block[7]]
        b7 = self._permute_tbl_2(round_idx * 16 + 7)[block[11]]
        b11 = self._permute_tbl_2(round_idx * 16 + 11)[block[15]]
        b15 = self._permute_tbl_2(round_idx * 16 + 15)[tmp]

        block[0] = b0
        block[1] = b1
        block[2] = b2
        block[3] = b3
        block[4] = b4
        block[5] = b5
        block[6] = b6
        block[7] = b7
        block[8] = b8
        block[9] = b9
        block[10] = b10
        block[11] = b11
        block[12] = b12
        block[13] = b13
        block[14] = b14
        block[15] = b15

