from pathlib import Path
import struct
import zlib

PREFIX1 = Path("prefix1.bin").read_bytes()
PREFIX2 = Path("prefix2.bin").read_bytes()

if len(PREFIX1) != len(PREFIX2):
    raise SystemExit("prefix files must have same length")

PREFIX_SIZE = len(PREFIX1)


def parse_prefix(data: bytes):
    cd = data.find(b"PK\x01\x02")

    if cd == -1:
        raise ValueError("central directory not found")

    crc32 = struct.unpack_from("<I", data, cd + 16)[0]
    comp_size = struct.unpack_from("<I", data, cd + 20)[0]
    uncomp_size = struct.unpack_from("<I", data, cd + 24)[0]
    fname_len = struct.unpack_from("<H", data, cd + 28)[0]
    local_offset = struct.unpack_from("<I", data, cd + 42)[0]

    filename = data[cd + 46 : cd + 46 + fname_len]

    return {
        "crc32": crc32,
        "comp_size": comp_size,
        "uncomp_size": uncomp_size,
        "local_offset": local_offset,
        "filename": filename,
    }


def make_local_header(filename: bytes, file_data: bytes, crc: int):
    return (
        b"PK\x03\x04"
        + struct.pack("<H", 10)                # version needed
        + struct.pack("<H", 0)                 # flags
        + struct.pack("<H", 0)                 # compression method: stored
        + struct.pack("<H", 0)                 # mod time
        + struct.pack("<H", 0)                 # mod date
        + struct.pack("<I", crc)
        + struct.pack("<I", len(file_data))    # compressed size
        + struct.pack("<I", len(file_data))    # uncompressed size
        + struct.pack("<H", len(filename))
        + struct.pack("<H", 0)                 # extra length
        + filename
        + file_data
    )


p1 = parse_prefix(PREFIX1)
p2 = parse_prefix(PREFIX2)

print("prefix1:", p1)
print("prefix2:", p2)
print("prefix size:", PREFIX_SIZE, hex(PREFIX_SIZE))

good = Path("main_good.py").read_bytes()
evil = Path("main_evil.py").read_bytes()

for label, data, prefix in [
    ("main_good.py", good, p1),
    ("main_evil.py", evil, p2),
]:
    if len(data) != prefix["uncomp_size"]:
        raise SystemExit(f"{label} wrong size")

    crc = zlib.crc32(data) & 0xFFFFFFFF

    if crc != prefix["crc32"]:
        raise SystemExit(
            f"{label} wrong CRC: got 0x{crc:08x}, expected 0x{prefix['crc32']:08x}"
        )

print(p1['filename'],'----------------',p2['filename'])
entries = [
    (
        p1["local_offset"],
        # make_local_header(p1["filename"], good, p1["crc32"]),
        make_local_header('zizo'.encode(), good, p1["crc32"]),
        "good payload",
    ),
    (
        p2["local_offset"],
        make_local_header('zizo'.encode(), evil, p2["crc32"]),
        "evil payload",
    ),
]

entries.sort()

suffix = bytearray()
current_offset = PREFIX_SIZE

for absolute_offset, blob, label in entries:
    print(f"placing {label} at 0x{absolute_offset:x}")

    if absolute_offset < current_offset:
        raise SystemExit(
            f"Cannot place {label}: current offset is 0x{current_offset:x}"
        )

    suffix += b"\x00" * (absolute_offset - current_offset)
    suffix += blob
    current_offset = absolute_offset + len(blob)

Path("suffix.bin").write_bytes(suffix)
Path("good.zip").write_bytes(PREFIX1 + suffix)
Path("evil.zip").write_bytes(PREFIX2 + suffix)

print("Created suffix.bin")
print("Created good.zip and evil.zip")