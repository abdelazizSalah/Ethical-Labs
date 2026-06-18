from pathlib import Path
import zlib
import py_compile

TARGET_CRC = 0x87F14BAC
SIZE = 256
CONTROL_BYTES = 64


def crc32(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def solve_crc_with_comment(payload: bytes, output_name: str):
    if not payload.endswith(b"\n"):
        payload += b"\n"

    # Final line is a comment with 64 controllable bytes.
    # Each controllable byte is either space 0x20 or ! 0x21.
    # Both are safe inside a Python comment.
    filler_len = SIZE - len(payload) - 1 - 2 - CONTROL_BYTES

    if filler_len < 0:
        raise ValueError(f"{output_name}: payload too large")

    base = bytearray(
        payload
        + b"#" * filler_len
        + b"\n# "
        + b" " * CONTROL_BYTES
    )

    control_positions = list(range(SIZE - CONTROL_BYTES, SIZE))

    base_crc = crc32(base)
    wanted_delta = base_crc ^ TARGET_CRC

    deltas = []

    for pos in control_positions:
        test = bytearray(base)
        test[pos] ^= 1  # space -> !
        deltas.append(crc32(test) ^ base_crc)

    # Gaussian elimination over GF(2)
    basis = {}

    for i, delta in enumerate(deltas):
        v = delta
        mask = 1 << i

        for bit in range(31, -1, -1):
            if not (v >> bit) & 1:
                continue

            if bit not in basis:
                basis[bit] = (v, mask)
                break

            v ^= basis[bit][0]
            mask ^= basis[bit][1]

    v = wanted_delta
    solution_mask = 0

    for bit in range(31, -1, -1):
        if not (v >> bit) & 1:
            continue

        if bit not in basis:
            raise RuntimeError("Could not solve CRC adjustment")

        v ^= basis[bit][0]
        solution_mask ^= basis[bit][1]

    if v != 0:
        raise RuntimeError("CRC solve failed")

    result = bytearray(base)

    for i, pos in enumerate(control_positions):
        if (solution_mask >> i) & 1:
            result[pos] ^= 1

    assert len(result) == SIZE
    assert crc32(result) == TARGET_CRC

    Path(output_name).write_bytes(result)

    print(f"{output_name}:")
    print(f"  size  = {len(result)}")
    print(f"  crc32 = 0x{crc32(result):08x}")


good_payload = b'''
print("GOOD VERSION")
'''

evil_payload = b'''
print(open('flag.txt', 'r').read()) 
'''

solve_crc_with_comment(good_payload, "main_good.py")
solve_crc_with_comment(evil_payload, "main_evil.py")

py_compile.compile("main_good.py", doraise=True)
py_compile.compile("main_evil.py", doraise=True)

print("Both Python files compile successfully.")