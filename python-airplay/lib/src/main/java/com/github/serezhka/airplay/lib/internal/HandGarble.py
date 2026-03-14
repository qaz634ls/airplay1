"""
Python rewrite of HandGarble.java
"""

def truncate32(val):
    return val & 0xFFFFFFFF

class HandGarble:
    def garble(self, buffer0: bytearray, buffer1: bytearray, buffer2: bytearray, buffer3: bytearray, buffer4: bytearray) -> None:
        buffer2[12] = ((0x14 + ((((buffer1[64] & 0xff) & 92) | (((buffer1[99] & 0xff) // 3) & 35)) & (buffer4[self._rol8x((buffer4[((buffer1[206] & 0xff) % 21)] & 0xff), 4) % 21] & 0xff)))) & 0xFF
        buffer1[4] = ((((buffer1[99] & 0xff) // 5) * ((buffer1[99] & 0xff) // 5) * 2)) & 0xFF
        buffer2[34] = (0xb8) & 0xFF
        buffer1[153] = (buffer1[153] ^ ((buffer2[(buffer1[203] & 0xff) % 35] * buffer2[(buffer1[203] & 0xff) % 35] * (buffer1[190] & 0xff)))) & 0xFF
        buffer0[3] = (buffer0[3] - ((((buffer4[(buffer1[205] & 0xff) % 21] >> 1) & 80) | 0xe6440))) & 0xFF
        buffer0[16] = (0x93) & 0xFF
        buffer0[13] = (0x62) & 0xFF
        buffer1[33] = (buffer1[33] - ((buffer4[(buffer1[36] & 0xff) % 21] & 0xf6))) & 0xFF
        tmp2 = (buffer2[(buffer1[67] & 0xff) % 35]) & 0xFFFFFFFF
        buffer2[12] = (0x07) & 0xFF
        tmp = (buffer0[(buffer1[181] & 0xff) % 20]) & 0xFFFFFFFF
        buffer1[2] = (buffer1[2] - (3136)) & 0xFF
        buffer0[19] = (buffer4[(buffer1[58] & 0xff) % 21]) & 0xFF
        buffer3[0] = ((92 - buffer2[(buffer1[32] & 0xff) % 35])) & 0xFF
        buffer3[4] = (((buffer2[(buffer1[15] & 0xff) % 35] & 0xff) + 0x9e)) & 0xFF
        buffer1[34] = (buffer1[34] + (((buffer4[(((buffer2[(buffer1[15] & 0xff) % 35] & 0xff) + 0x9e) & 0xff) % 21] & 0xff) // 5))) & 0xFF
        buffer0[19] = (((buffer0[19] & 0xff) + 0xfffffee6 - (((buffer0[(buffer3[4] & 0xff) % 20] & 0xff) >> 1) & 102))) & 0xFF
        buffer1[15] = (((3 * ((((buffer1[72] & 0xff) >> ((buffer4[(buffer1[190] & 0xff) % 21] & 0xff) & 7)) ^ ((buffer1[72] & 0xff) << ((7 - ((buffer4[(buffer1[190] & 0xff) % 21] & 0xff) - 1) & 7)))) - (3 * buffer4[(buffer1[126] & 0xff) % 21]))) ^ buffer1[15])) & 0xFF
        buffer0[15] = (buffer0[15] ^ ((buffer2[(buffer1[181] & 0xff) % 35] & 0xff) * (buffer2[(buffer1[181] & 0xff) % 35] & 0xff) * (buffer2[(buffer1[181] & 0xff) % 35] & 0xff))) & 0xFF
        buffer2[4] = (buffer2[4] ^ ((buffer1[202] & 0xff) // 3)) & 0xFF
        A = (92 - (buffer0[(buffer3[0] & 0xff) % 20] & 0xff)) & 0xFFFFFFFF
        E = ((A & 0xc6) | ((~(buffer1[105] & 0xff) & 0xFFFFFFFF) & 0xc6) | (A & ((~(buffer1[105] & 0xff) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        buffer2[1] = (buffer2[1] + ((E * E * E))) & 0xFF
        buffer0[19] = (buffer0[19] ^ (((224 | ((buffer4[(buffer1[92] & 0xff) % 21] & 0xff) & 27)) * (buffer2[(buffer1[41] & 0xff) % 35] & 0xff)) // 3)) & 0xFF
        buffer1[140] = (buffer1[140] + (self._weird_ror8( 92, (buffer1[5] & 0xff) & 7))) & 0xFF
        buffer2[12] = (buffer2[12] + ((((((~(buffer1[4] & 0xff) & 0xFFFFFFFF)) ^ (buffer2[(buffer1[12] & 0xff) % 35] & 0xff)) | (buffer1[182] & 0xff)) & 192) | ((((~(buffer1[4] & 0xff) & 0xFFFFFFFF)) ^ (buffer2[(buffer1[12] & 0xff) % 35] & 0xff)) & (buffer1[182] & 0xff)))) & 0xFF
        buffer1[36] = (buffer1[36] + (125)) & 0xFF
        buffer1[124] = (self._rol8x(((((74 & (buffer1[138] & 0xff)) | ((74 | (buffer1[138] & 0xff)) & (buffer0[15] & 0xff))) & (buffer0[(buffer1[43] & 0xff) % 20] & 0xff)) | (((74 & (buffer1[138] & 0xff)) | ((74 | (buffer1[138] & 0xff)) & (buffer0[15] & 0xff)) | (buffer0[(buffer1[43] & 0xff) % 20] & 0xff)) & 95)), 4)) & 0xFF
        buffer3[8] = (((((((buffer0[(buffer3[4] & 0xff) % 20] & 0xff) & 95)) & (((buffer4[(buffer1[68] & 0xff) % 21] & 0xff) & 46) << 1)) | 16) ^ 92)) & 0xFF
        A = ((buffer1[177] & 0xff) + (buffer4[(buffer1[79] & 0xff) % 21] & 0xff)) & 0xFFFFFFFF
        D = ((((A >> 1) | ((3 * (buffer1[148] & 0xff)) // 5)) & (buffer2[1] & 0xff)) | ((A >> 1) & ((3 * (buffer1[148] & 0xff)) // 5))) & 0xFFFFFFFF
        buffer3[12] = ((-34 - D)) & 0xFF
        A = (8 - (((buffer2[22] & 0xff) & 7))) & 0xFFFFFFFF
        B = (((buffer1[33] & 0xff) >> (A & 7))) & 0xFFFFFFFF
        C = ((buffer1[33] & 0xff) << ((buffer2[22] & 0xff) & 7)) & 0xFFFFFFFF
        buffer2[16] = (buffer2[16] + ((((buffer2[(buffer3[0] & 0xff) % 35] & 0xff) & 159) | (buffer0[(buffer3[4] & 0xff) % 20] & 0xff) | 8) - ((B ^ C) | 128))) & 0xFF
        buffer0[14] = (buffer0[14] ^ ((buffer2[(buffer3[12] & 0xff) % 35] & 0xff))) & 0xFF
        A = (self._weird_rol8((buffer4[(buffer0[(buffer1[201] & 0xff) % 20] & 0xff) % 21] & 0xff), (((buffer2[(buffer1[112] & 0xff) % 35] & 0xff) << 1) & 7))) & 0xFFFFFFFF
        D = ((buffer0[(buffer1[208] & 0xff) % 20] & 131) | ((buffer0[(buffer1[164] & 0xff) % 20] & 0xff) & 124)) & 0xFFFFFFFF
        buffer1[19] = (buffer1[19] + ((A & (D // 5)) | ((A | (D // 5)) & 37))) & 0xFF
        buffer2[8] = ((self._weird_ror8(140, (((buffer4[(buffer1[45] & 0xff) % 21] & 0xff) + 92) * ((buffer4[(buffer1[45] & 0xff) % 21] & 0xff) + 92)) & 7) & 0xff)) & 0xFF
        buffer1[190] = (56) & 0xFF
        buffer2[8] = (buffer2[8] ^ ((buffer3[0] & 0xff))) & 0xFF
        buffer1[53] = ((~(((buffer0[(buffer1[83] & 0xff) % 20] & 0xff) | 204) // 5)) & 0xFFFFFFFF) & 0xFF
        buffer0[13] = (buffer0[13] + ((buffer0[(buffer1[41] & 0xff) % 20] & 0xff))) & 0xFF
        buffer0[10] = (((((buffer2[(buffer3[0] & 0xff) % 35] & 0xff) & (buffer1[2] & 0xff)) | (((buffer2[(buffer3[0] & 0xff) % 35] & 0xff) | (buffer1[2] & 0xff)) & (buffer3[12] & 0xff))) // 15)) & 0xFF
        A = ((((56 | ((buffer4[(buffer1[2] & 0xff) % 21] & 0xff) & 68)) | (buffer2[(buffer3[8] & 0xff) % 35] & 0xff)) & 42) | ((((buffer4[(buffer1[2] & 0xff) % 21] & 0xff) & 68) | 56) & (buffer2[(buffer3[8] & 0xff) % 35] & 0xff))) & 0xFFFFFFFF
        buffer3[16] = (((A * A) + 110)) & 0xFF
        buffer3[20] = ((202 - (buffer3[16] & 0xff))) & 0xFF
        buffer3[24] = (buffer1[151]) & 0xFF
        buffer2[13] = (buffer2[13] ^ (buffer4[(buffer3[0] & 0xff) % 21])) & 0xFF
        B = ((((buffer2[(buffer1[179] & 0xff) % 35] & 0xff) - 38) & 177) | ((buffer3[12] & 0xff) & 177)) & 0xFFFFFFFF
        C = ((((buffer2[(buffer1[179] & 0xff) % 35] & 0xff) - 38)) & (buffer3[12] & 0xff)) & 0xFFFFFFFF
        buffer3[28] = ((30 + ((B | C) * (B | C)))) & 0xFF
        buffer3[32] = ((buffer3[28] + 62)) & 0xFF
        A = ((((buffer3[20] & 0xff) + ((buffer3[0] & 0xff) & 74)) | (~(buffer4[(buffer3[0] & 0xff) % 21] & 0xff) & 0xFFFFFFFF)) & 121) & 0xFFFFFFFF
        B = ((((buffer3[20] & 0xff) + ((buffer3[0] & 0xff) & 74)) & (~(buffer4[(buffer3[0] & 0xff) % 21] & 0xff) & 0xFFFFFFFF))) & 0xFFFFFFFF
        tmp3 = ((A | B)) & 0xFFFFFFFF
        C = (((((A | B) ^ 0xffffffa6) | (buffer3[0] & 0xff)) & 4) | (((A | B) ^ 0xffffffa6) & (buffer3[0] & 0xff))) & 0xFFFFFFFF
        buffer1[47] = ((((buffer2[(buffer1[89] & 0xff) % 35] & 0xff) + C) ^ (buffer1[47] & 0xff))) & 0xFF
        buffer3[36] = ((((self._rol8( ((tmp & 179) + 68), 2) & (buffer0[3] & 0xff)) | (tmp2 & (~(buffer0[3] & 0xff) & 0xFFFFFFFF))) - 15)) & 0xFF
        buffer1[123] = (buffer1[123] ^ (221)) & 0xFF
        A = ((((buffer4[(buffer3[0] & 0xff) % 21]) & 0xff) // 3) - (buffer2[(buffer3[4] & 0xff) % 35] & 0xff)) & 0xFFFFFFFF
        C = ((((buffer3[0] & 163) + 92) & 246) | (buffer3[0] & 92)) & 0xFFFFFFFF
        E = (((C | buffer3[24]) & 54) | (C & buffer3[24])) & 0xFFFFFFFF
        buffer3[40] = ((A - E)) & 0xFF
        buffer3[44] = ((tmp3 ^ 81 ^ ((((buffer3[0] & 0xff) >> 1) & 101) + 26))) & 0xFF
        buffer3[48] = (((buffer2[(buffer3[4] & 0xff) % 35] & 0xff) & 27)) & 0xFF
        buffer3[52] = (27) & 0xFF
        buffer3[56] = (199) & 0xFF
        buffer3[64] = (((buffer3[4] & 0xff) + ((((((((buffer3[40] & 0xff) | (buffer3[24] & 0xff)) & 177) | ((buffer3[40] & 0xff) & (buffer3[24] & 0xff))) & (((((buffer4[(buffer3[0] & 0xff) % 20] & 0xff) & 177) | 176)) | (((buffer4[(buffer3[0] & 0xff) % 21] & 0xff)) & (~3 & 0xFFFFFFFF)))) | (((((buffer3[40] & 0xff) & (buffer3[24] & 0xff)) | (((buffer3[40] & 0xff) | (buffer3[24] & 0xff)) & 177)) & 199) | ((((((buffer4[(buffer3[0] & 0xff) % 21] & 0xff) & 1) & 0xff) + 176) | ((buffer4[(buffer3[0] & 0xff) % 21] & 0xff) & (~3 & 0xFFFFFFFF))) & (buffer3[56] & 0xff)))) & ((~(buffer3[52] & 0xff) & 0xFFFFFFFF))) | (buffer3[48] & 0xff)))) & 0xFF
        buffer2[33] = (buffer2[33] ^ (buffer1[26])) & 0xFF
        buffer1[106] = (buffer1[106] ^ (buffer3[20] ^ 133)) & 0xFF
        buffer2[30] = (((((buffer3[64] & 0xff) // 3) - (275 | ((buffer3[0] & 0xff) & 247))) ^ (buffer0[(buffer1[122] & 0xff) % 20] & 0xff))) & 0xFF
        buffer1[22] = ((((buffer2[(buffer1[90] & 0xff) % 35] & 0xff) & 95) | 68)) & 0xFF
        A = (((buffer4[(buffer3[36] & 0xff) % 21] & 0xff) & 184) | ((buffer2[(buffer3[44] & 0xff) % 35] & 0xff) & (~184 & 0xFFFFFFFF))) & 0xFFFFFFFF
        buffer2[18] = (buffer2[18] + (((A * A * A) >> 1))) & 0xFF
        buffer2[5] = (buffer2[5] - ((buffer4[(buffer1[92] & 0xff) % 21] & 0xff))) & 0xFF
        A = (((((buffer1[41] & 0xff) & (~24 & 0xFFFFFFFF)) | ((buffer2[(buffer1[183] & 0xff) % 35] & 0xff) & 24)) & ((buffer3[16] & 0xff) + 53)) | (buffer3[20] & (buffer2[(buffer3[20] & 0xff) % 35] & 0xff))) & 0xFFFFFFFF
        B = (((buffer1[17] & 0xff) & ((~(buffer3[44] & 0xff) & 0xFFFFFFFF))) | ((buffer0[(buffer1[59] & 0xff) % 20] & 0xff) & (buffer3[44] & 0xff))) & 0xFFFFFFFF
        buffer2[18] = (buffer2[18] ^ ((A * B))) & 0xFF
        A = (self._weird_ror8((buffer1[11] & 0xff), (buffer2[(buffer1[28] & 0xff) % 35] & 0xff) & 7) & 7) & 0xFFFFFFFF
        B = (((((buffer0[(buffer1[93] & 0xff) % 20] & 0xff) & (~(buffer0[14] & 0xff) & 0xFFFFFFFF)) | ((buffer0[14] & 0xff) & 150)) & (~28 & 0xFFFFFFFF)) | ((buffer1[7] & 0xff) & 28)) & 0xFFFFFFFF
        buffer2[22] = ((((((B | self._weird_rol8((buffer2[(buffer3[0] & 0xff) % 35] & 0xff), A)) & (buffer2[33] & 0xff)) | (B & self._weird_rol8((buffer2[(buffer3[0] & 0xff) % 35] & 0xff), A))) + 74) & 0xff)) & 0xFF
        A = (buffer4[((buffer0[(buffer1[39] & 0xff) % 20] & 0xff) ^ 217) % 21] & 0xff) & 0xFFFFFFFF
        buffer0[15] = (buffer0[15] - ((((((buffer3[20] & 0xff) | (buffer3[0] & 0xff)) & 214) | ((buffer3[20] & 0xff) & (buffer3[0] & 0xff))) & A) | (((((buffer3[20] & 0xff) | (buffer3[0] & 0xff)) & 214) | ((buffer3[20] & 0xff) & (buffer3[0] & 0xff)) | A) & (buffer3[32] & 0xff)))) & 0xFF
        B = ((((buffer2[(buffer1[57] & 0xff) % 35] & buffer0[(buffer3[64] & 0xff) % 20]) | ((buffer0[(buffer3[64] & 0xff) % 20] | buffer2[(buffer1[57] & 0xff) % 35]) & 95) | (buffer3[64] & 45) | 82) & 32)) & 0xFFFFFFFF
        C = (((buffer2[(buffer1[57] & 0xff) % 35] & buffer0[(buffer3[64] & 0xff) % 20]) | ((buffer2[(buffer1[57] & 0xff) % 35] | buffer0[(buffer3[64] & 0xff) % 20]) & 95)) & ((buffer3[64] & 45) | 82)) & 0xFFFFFFFF
        D = ((((((buffer3[0] & 0xff) // 3) - ((buffer3[64] & 0xff) | (buffer1[22] & 0xff)))) ^ ((buffer3[28] & 0xff) + 62) ^ ((B | C)))) & 0xFFFFFFFF
        T = ((buffer0[(D & 0xff) % 20] & 0xff)) & 0xFFFFFFFF
        buffer3[68] = ((((buffer0[(buffer1[99] & 0xff) % 20] & 0xff) * (buffer0[(buffer1[99] & 0xff) % 20] & 0xff) * (buffer0[(buffer1[99] & 0xff) % 20] & 0xff) * (buffer0[(buffer1[99] & 0xff) % 20] & 0xff)) | (buffer2[(buffer3[64] & 0xff) % 35] & 0xff))) & 0xFF
        U = (buffer0[(buffer1[50] & 0xff) % 20] & 0xff) & 0xFFFFFFFF
        W = (buffer2[(buffer1[138] & 0xff) % 35] & 0xff) & 0xFFFFFFFF
        X = (buffer4[(buffer1[39] & 0xff) % 21] & 0xff) & 0xFFFFFFFF
        Y = (buffer0[(buffer1[4] & 0xff) % 20] & 0xff) & 0xFFFFFFFF
        Z = (buffer4[(buffer1[202] & 0xff) % 21] & 0xff) & 0xFFFFFFFF
        V = (buffer0[(buffer1[151] & 0xff) % 20] & 0xff) & 0xFFFFFFFF
        S = (buffer2[(buffer1[14] & 0xff) % 35] & 0xff) & 0xFFFFFFFF
        R = (buffer0[(buffer1[145] & 0xff) % 20] & 0xff) & 0xFFFFFFFF
        A = (((buffer2[(buffer3[68] & 0xff) % 35] & 0xff) & (buffer0[(buffer1[209] & 0xff) % 20] & 0xff)) | (((buffer2[(buffer3[68] & 0xff) % 35] & 0xff) | (buffer0[(buffer1[209] & 0xff) % 20] & 0xff)) & 24)) & 0xFFFFFFFF
        B = (self._weird_rol8((buffer4[(buffer1[127] & 0xff) % 21] & 0xff), (buffer2[(buffer3[68] & 0xff) % 35] & 0xff) & 7)) & 0xFFFFFFFF
        C = ((A & (buffer0[10] & 0xff)) | (B & (~(buffer0[10] & 0xff) & 0xFFFFFFFF))) & 0xFFFFFFFF
        D = (7 ^ ((buffer4[(buffer2[(buffer3[36] & 0xff) % 35] & 0xff) % 21] & 0xff) << 1)) & 0xFFFFFFFF
        buffer3[72] = (((C & 71) | (D & (~71 & 0xFFFFFFFF)))) & 0xFF
        buffer2[2] = (buffer2[2] + (((((buffer0[(buffer3[20] & 0xff) % 20] & 0xff) << 1) & 159) | ((buffer4[(buffer1[190] & 0xff) % 21] & 0xff) & (~159 & 0xFFFFFFFF))) & (((((buffer4[(buffer3[64] & 0xff) % 21] & 0xff) & 110) | ((buffer0[(buffer1[25] & 0xff) % 20] & 0xff) & (~110 & 0xFFFFFFFF))) & (~150 & 0xFFFFFFFF)) | ((buffer1[25] & 0xff) & 150)))) & 0xFF
        buffer2[14] = (buffer2[14] - ((((buffer2[(buffer3[20] & 0xff) % 35] & 0xff) & ((buffer3[72] & 0xff) ^ (buffer2[(buffer1[100] & 0xff) % 35] & 0xff))) & (~34 & 0xFFFFFFFF)) | ((buffer1[97] & 0xff) & 34))) & 0xFF
        buffer0[17] = (115) & 0xFF
        buffer1[23] = (buffer1[23] ^ ((((((((buffer4[(buffer1[17] & 0xff) % 21] & 0xff) | (buffer0[(buffer3[20] & 0xff) % 20] & 0xff)) & (buffer3[72] & 0xff)) | ((buffer4[(buffer1[17] & 0xff) % 21] & 0xff) & (buffer0[(buffer3[20] & 0xff) % 20] & 0xff))) & ((buffer1[50] & 0xff) // 3)) | (((((buffer4[(buffer1[17] & 0xff) % 21] & 0xff) | (buffer0[(buffer3[20] & 0xff) % 20] & 0xff)) & (buffer3[72] & 0xff)) | ((buffer4[(buffer1[17] & 0xff) % 21] & 0xff) & buffer0[(buffer3[20] & 0xff) % 20]) | ((buffer1[50] & 0xff) // 3)) & 246)) << 1))) & 0xFF
        buffer0[13] = ((((((((buffer0[(buffer3[40] & 0xff) % 20] & 0xff) | (buffer1[10] & 0xff)) & 82) | ((buffer0[(buffer3[40] & 0xff) % 20] & 0xff) & (buffer1[10] & 0xff))) & 209) | (((buffer0[(buffer1[39] & 0xff) % 20] & 0xff) << 1) & 46)) >> 1)) & 0xFF
        buffer2[33] = (buffer2[33] - (buffer1[113] & 9)) & 0xFF
        buffer2[28] = (buffer2[28] - (((((2 | (buffer1[110] & 222)) >> 1) & (~223 & 0xFFFFFFFF)) | (buffer3[20] & 223)))) & 0xFF
        J = (self._weird_rol8((V | Z), (U & 7))) & 0xFFFFFFFF
        A = (((buffer2[16] & 0xff) & T) | (W & ((~(buffer2[16] & 0xff) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        B = (((buffer1[33] & 0xff) & 17) | (X & (~17 & 0xFFFFFFFF))) & 0xFFFFFFFF
        E = (((Y | ((A + B) // 5)) & 147) | (Y & ((A + B) // 5))) & 0xFFFFFFFF
        M = (((buffer3[40] & 0xff) & (buffer4[(((buffer3[8] & 0xff) + J + E) & 0xff) % 21] & 0xff)) | (((buffer3[40] & 0xff) | (buffer4[(((buffer3[8] & 0xff) + J + E) & 0xff) % 21] & 0xff)) & (buffer2[23] & 0xff))) & 0xFFFFFFFF
        buffer0[15] = ((((((buffer4[(buffer3[20] & 0xff) % 21] & 0xff) - 48) & ((~(buffer1[184] & 0xff) & 0xFFFFFFFF))) | (((buffer4[(buffer3[20] & 0xff) % 21] & 0xff) - 48) & 189) | (189 & (~(buffer1[184] & 0xff) & 0xFFFFFFFF))) & (M * M * M))) & 0xFF
        buffer2[22] = (buffer2[22] + (buffer1[183])) & 0xFF
        buffer3[76] = (((3 * buffer4[(buffer1[1] & 0xff) % 21]) ^ buffer3[0])) & 0xFF
        A = (buffer2[(((buffer3[8] & 0xff) + (J + E)) & 0xff) % 35] & 0xff) & 0xFFFFFFFF
        F = (((((buffer4[(buffer1[178] & 0xff) % 21] & 0xff) & A) | (((buffer4[(buffer1[178] & 0xff) % 21] & 0xff) | A) & 209)) * (buffer0[(buffer1[13] & 0xff) % 20] & 0xff)) * ((buffer4[(buffer1[26] & 0xff) % 21] & 0xff) >> 1)) & 0xFFFFFFFF
        G = ((F + 0x733ffff9) * 198 - (((F + 0x733ffff9) * 396 + 212) & 212) + 85) & 0xFFFFFFFF
        buffer3[80] = (((buffer3[36] & 0xff) + (G ^ 148) + ((G ^ 107) << 1) - 127)) & 0xFF
        buffer3[84] = (((((buffer2[(buffer3[64] & 0xff) % 35] & 0xff)) & 245) | ((buffer2[(buffer3[20] & 0xff) % 35] & 0xff) & 10))) & 0xFF
        A = ((buffer0[(buffer3[68] & 0xff) % 20] & 0xff) | 81) & 0xFFFFFFFF
        buffer2[18] = (buffer2[18] - (((A * A * A) & (~buffer0[15] & 0xFFFFFFFF)) | (((buffer3[80] & 0xff) // 15) & (buffer0[15] & 0xff)))) & 0xFF
        buffer3[88] = (((buffer3[8] & 0xff) + J + E - (buffer0[(buffer1[160] & 0xff) % 20] & 0xff) + ((buffer4[(buffer0[((buffer3[8] + J + E) & 255) % 20] & 0xff) % 21] & 0xff) // 3))) & 0xFF
        B = (((R ^ (buffer3[72] & 0xff)) & (~198 & 0xFFFFFFFF)) | ((S * S) & 198)) & 0xFFFFFFFF
        F = (((buffer4[(buffer1[69] & 0xff) % 21] & 0xff) & (buffer1[172] & 0xff)) | (((buffer4[(buffer1[69] & 0xff) % 21] & 0xff) | (buffer1[172] & 0xff)) & (((buffer3[12] & 0xff) - B) + 77))) & 0xFFFFFFFF
        buffer0[16] = ((147 - (((buffer3[72] & 0xff) & ((F & 251) | 1)) | (((F & 250) | (buffer3[72] & 0xff)) & 198)))) & 0xFF
        C = (((buffer4[(buffer1[168] & 0xff) % 21] & 0xff) & buffer0[(buffer1[29] & 0xff) % 20] & 7) | ((buffer4[(buffer1[168] & 0xff) % 21] | buffer0[(buffer1[29] & 0xff) % 20]) & 6)) & 0xFFFFFFFF
        F = (((buffer4[(buffer1[155] & 0xff) % 21] & 0xff) & (buffer1[105] & 0xff)) | (((buffer4[(buffer1[155] & 0xff) % 21] & 0xff) | (buffer1[105] & 0xff)) & 141)) & 0xFFFFFFFF
        buffer0[3] = (buffer0[3] - (buffer4[self._weird_rol32(F, C) % 21])) & 0xFF
        buffer1[5] = ((self._weird_ror8((buffer0[12] & 0xff), (((buffer0[(buffer1[61] & 0xff) % 20] & 0xff) // 5) & 7)) ^ ((((~buffer2[(buffer3[84] & 0xff) % 35]) & 0xFFFFFFFF) // 5)))) & 0xFF
        buffer1[198] = (buffer1[198] + (buffer1[3])) & 0xFF
        A = ((162 | (buffer2[(buffer3[64] & 0xff) % 35] & 0xff))) & 0xFFFFFFFF
        buffer1[164] = (buffer1[164] + (((A * A) // 5))) & 0xFF
        G = (self._weird_ror8(139, ((buffer3[80] & 0xff) & 7))) & 0xFFFFFFFF
        C = ((((buffer4[(buffer3[64] & 0xff) % 21] & 0xff) * (buffer4[(buffer3[64] & 0xff) % 21] & 0xff) * (buffer4[(buffer3[64] & 0xff) % 21] & 0xff)) & 95) | ((buffer0[(buffer3[40] & 0xff) % 20] & 0xff) & (~95 & 0xFFFFFFFF))) & 0xFFFFFFFF
        buffer3[92] = (((G & 12) | ((buffer0[(buffer3[20] & 0xff) % 20] & 0xff) & 12) | (G & (buffer0[(buffer3[20] & 0xff) % 20] & 0xff)) | C)) & 0xFF
        buffer2[12] = (buffer2[12] + ((((buffer1[103] & 0xff) & 32) | ((buffer3[92] & 0xff) & (((buffer1[103] & 0xff) | 60))) | 16) // 3)) & 0xFF
        buffer3[96] = (buffer1[143]) & 0xFF
        buffer3[100] = (27) & 0xFF
        buffer3[104] = ((((((buffer3[40] & 0xff) & (~(buffer2[8] & 0xff) & 0xFFFFFFFF)) | ((buffer1[35] & 0xff) & (buffer2[8] & 0xff))) & (buffer3[64] & 0xff)) ^ 119)) & 0xFF
        buffer3[108] = ((238 & (((((buffer3[40] & 0xff) & (~(buffer2[8] & 0xff) & 0xFFFFFFFF)) | ((buffer1[35] & 0xff) & (buffer2[8] & 0xff))) & (buffer3[64] & 0xff)) << 1))) & 0xFF
        buffer3[112] = ((((~(buffer3[64] & 0xff) & 0xFFFFFFFF) & ((buffer3[84] & 0xff) // 3)) ^ 49)) & 0xFF
        buffer3[116] = ((98 & (((~(buffer3[64] & 0xff) & 0xFFFFFFFF) & ((buffer3[84] & 0xff) // 3)) << 1))) & 0xFF
        A = (((buffer1[35] & 0xff) & (buffer2[8] & 0xff)) | ((buffer3[40] & 0xff) & (~(buffer2[8] & 0xff) & 0xFFFFFFFF))) & 0xFFFFFFFF
        B = ((A & buffer3[64]) | ((((buffer3[84] & 0xff) // 3) & (~(buffer3[64] & 0xff) & 0xFFFFFFFF)))) & 0xFFFFFFFF
        buffer1[143] = (((buffer3[96] & 0xff) - ((B & (86 + (((buffer1[172] & 0xff) & 64) >> 1))) | ((((((buffer1[172] & 0xff) & 65) >> 1) ^ 86) | (((~(buffer3[64] & 0xff) & 0xFFFFFFFF) & ((buffer3[84] & 0xff) // 3)) | ((((buffer3[40] & 0xff) & (~(buffer2[8] & 0xff) & 0xFFFFFFFF)) | ((buffer1[35] & 0xff) & (buffer2[8] & 0xff))) & (buffer3[64] & 0xff)))) & (buffer3[100] & 0xff))))) & 0xFF
        buffer2[29] = (162) & 0xFF
        A = ((((((buffer4[(buffer3[88] & 0xff) % 21] & 0xff)) & 160) | ((buffer0[(buffer1[125] & 0xff) % 20] & 0xff) & 95)) >> 1)) & 0xFFFFFFFF
        B = ((buffer2[(buffer1[149] & 0xff) % 35] & 0xff) ^ ((buffer1[43] & 0xff) * (buffer1[43] & 0xff))) & 0xFFFFFFFF
        buffer0[15] = (buffer0[15] + ((B & A) | ((A | B) & 115))) & 0xFF
        buffer3[120] = (((buffer3[64] & 0xff) - (buffer0[(buffer3[40] & 0xff) % 20] & 0xff))) & 0xFF
        buffer1[95] = (buffer4[(buffer3[20] & 0xff) % 21]) & 0xFF
        A = (self._weird_ror8((buffer2[(buffer3[80] & 0xff) % 35] & 0xff), ((buffer2[(buffer1[17] & 0xff) % 35] & 0xff) * (buffer2[(buffer1[17] & 0xff) % 35] & 0xff) * (buffer2[(buffer1[17] & 0xff) % 35] & 0xff)) & 7)) & 0xFFFFFFFF
        buffer0[7] = (buffer0[7] - (((A * A)))) & 0xFF
        buffer2[8] = (((buffer2[8] & 0xff) - (buffer1[184] & 0xff) + ((buffer4[(buffer1[202] & 0xff) % 21] & 0xff) * (buffer4[(buffer1[202] & 0xff) % 21] & 0xff) * (buffer4[(buffer1[202] & 0xff) % 21] & 0xff)))) & 0xFF
        buffer0[16] = ((((buffer2[(buffer1[102] & 0xff) % 35] & 0xff) << 1) & 132)) & 0xFF
        buffer3[124] = ((((buffer4[(buffer3[40] & 0xff) % 21] & 0xff) >> 1) ^ (buffer3[68] & 0xff))) & 0xFF
        buffer0[7] = (buffer0[7] - (((buffer0[(buffer1[191] & 0xff) % 20] & 0xff) - ((((buffer4[(buffer1[80] & 0xff) % 21] & 0xff) << 1) & (~177 & 0xFFFFFFFF)) | ((buffer4[(buffer4[(buffer3[88] & 0xff) % 21] & 0xff) % 21] & 0xff) & 177))))) & 0xFF
        buffer0[6] = (buffer0[(buffer1[119] & 0xff) % 20]) & 0xFF
        A = ((buffer4[(buffer1[190] & 0xff) % 21] & (~209 & 0xFFFFFFFF)) | (buffer1[118] & 209)) & 0xFFFFFFFF
        B = (buffer0[(buffer3[120] & 0xff) % 20] * buffer0[(buffer3[120] & 0xff) % 20]) & 0xFFFFFFFF
        buffer0[12] = (((buffer0[(buffer3[84] & 0xff) % 20] ^ (buffer2[(buffer1[71] & 0xff) % 35] + buffer2[(buffer1[15] & 0xff) % 35])) & ((A & B) | ((A | B) & 27)))) & 0xFF
        B = (((buffer1[32] & 0xff) & (buffer2[(buffer3[88] & 0xff) % 35] & 0xff)) | (((buffer1[32] & 0xff) | (buffer2[(buffer3[88] & 0xff) % 35] & 0xff)) & 23)) & 0xFFFFFFFF
        D = (((((buffer4[(buffer1[57] & 0xff) % 21] & 0xff) * 231) & 169) | (B & 86))) & 0xFFFFFFFF
        F = (((((buffer0[(buffer1[82] & 0xff) % 20] & 0xff) & (~29 & 0xFFFFFFFF)) | ((buffer4[(buffer3[124] & 0xff) % 21] & 0xff) & 29)) & 190) | ((buffer4[(D // 5) % 21] & 0xff) & (~190 & 0xFFFFFFFF))) & 0xFFFFFFFF
        H = ((buffer0[(buffer3[40] & 0xff) % 20] & 0xff) * (buffer0[(buffer3[40] & 0xff) % 20] & 0xff) * (buffer0[(buffer3[40] & 0xff) % 20] & 0xff)) & 0xFFFFFFFF
        K = ((H & (buffer1[82] & 0xff)) | (H & 92) | ((buffer1[82] & 0xff) & 92)) & 0xFFFFFFFF
        buffer3[128] = ((((F & K) | ((F | K) & 192)) ^ (D // 5))) & 0xFF
        buffer2[25] = (buffer2[25] ^ ((((buffer0[(buffer3[120] & 0xff) % 20] & 0xff) << 1) * (buffer1[5] & 0xff)) - (self._weird_rol8((buffer3[76] & 0xff), ((buffer4[(buffer3[124] & 0xff) % 21] & 0xff) & 7)) & ((buffer3[20] & 0xff) + 110)))) & 0xFF

    def _rol8(self, input_val: int, count: int) -> int:
        input_val &= 0xFF
        count &= 7
        return ((input_val << count) & 0xFF) | (input_val >> (8 - count))

    def _rol8x(self, input_val: int, count: int) -> int:
        input_val = truncate32(input_val)
        return truncate32((input_val << count) | (input_val >> (8 - count)))

    def _weird_ror8(self, input_val: int, count: int) -> int:
        input_val = truncate32(input_val)
        if count == 0:
            return 0
        return truncate32(((input_val >> count) & 0xFF) | ((input_val & 0xFF) << (8 - count)))

    def _weird_rol8(self, input_val: int, count: int) -> int:
        input_val = truncate32(input_val)
        if count == 0:
            return 0
        return truncate32(((input_val << count) & 0xFF) | ((input_val & 0xFF) >> (8 - count)))

    def _weird_rol32(self, input_val: int, count: int) -> int:
        input_val = truncate32(input_val)
        if count == 0:
            return 0
        return truncate32((input_val << count) ^ (input_val >> (8 - count)))
