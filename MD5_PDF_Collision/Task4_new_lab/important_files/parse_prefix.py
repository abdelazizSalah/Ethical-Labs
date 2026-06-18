import struct
from pathlib import Path

CD_SIG = b"PK\x01\x02"
EOCD_SIG = b"PK\x05\x06"

for name in ["prefix1.bin", "prefix2.bin"]:
    data = Path(name).read_bytes()

    cd = data.find(CD_SIG)
    eocd = data.find(EOCD_SIG)

    print(f"\n===== {name} =====")
    print(f"size: {len(data)} / 0x{len(data):x}")
    print(f"central directory offset: {cd} / 0x{cd:x}")
    print(f"EOCD offset: {eocd} / 0x{eocd:x}")

    if cd == -1:
        print("No central directory found")
        continue

    crc32 = struct.unpack_from("<I", data, cd + 16)[0]
    comp_size = struct.unpack_from("<I", data, cd + 20)[0]
    uncomp_size = struct.unpack_from("<I", data, cd + 24)[0]
    fname_len = struct.unpack_from("<H", data, cd + 28)[0]
    extra_len = struct.unpack_from("<H", data, cd + 30)[0]
    comment_len = struct.unpack_from("<H", data, cd + 32)[0]
    local_offset = struct.unpack_from("<I", data, cd + 42)[0]

    filename = data[cd + 46 : cd + 46 + fname_len]

    print(f"filename: {filename!r}")
    print(f"crc32: 0x{crc32:08x}")
    print(f"compressed size: {comp_size}")
    print(f"uncompressed size: {uncomp_size}")
    print(f"filename length: {fname_len}")
    print(f"extra length: {extra_len}")
    print(f"comment length: {comment_len}")
    print(f"local header offset: {local_offset} / 0x{local_offset:x}")