#!/usr/bin/env python3


"""
Directly compute a suffix that forces a file to a target ZIP CRC‑32.

The calculation of CRC-32 is based on mathematical principles (namely, the CRC is the remainder when
dividing the data polynomial by a certain fix generator polynomial - each polynomial defined in
GF(2)).

The script exploits the linearity of these operations to find the required 4-byte suffix instantly
and without brute force. Namely, the operations can be represented by a matrix operation, which can
be inverted. Knowing the "difference" we need to add to the final CRC digest to fit it to our
target, we can propagate said difference backwards with the inverted matrix to learn the bytes that
need to be appended to the data.

Additional requirements on the suffix can be specified (e.g. only printable or only letter
characters). In this case, the suffix will be very slightly longer, with some random attempts to break
up cases where the required 4-byte suffix does not match the requirements.

NOTE: This script focuses on the ZIP CRC-32 algorithm. There are different standards, such as for
Ethernet or POSIX, which use different polynomials, initialization states, and may or may not add
the file size into the calculation (in the case of POSIX). The same principles can be utilized on
these algorithms (although more difficulty arises from appending bytes when the file size also plays
a role).

Supports:
  - ZIP CRC (default, polynomial 0xEDB88320) – used in ZIP, BZIP2, Python's binascii.crc32.
  - Restrictions: none (--restrict NONE, arbitrary bytes), printable ASCII (PRINTABLE),
    or letters only (LETTERS).

Usage examples:
  python crc_clash.py main.py 0x87F14BAC
  python crc_clash.py main.py 0x87F14BAC -r LETTERS -o main-letters.py
"""

import argparse
import binascii
import random
import struct
import sys
from pathlib import Path


###########################
## CRC ALGORITHM LIBRARY ##
##############################################################################################
def _raw_crc_update_zip(state: int, byte: int) -> int:
    """Reflected CRC‑32 update (polynomial 0xEDB88320)."""
    state ^= byte

    for _ in range(8):
        if state & 1:
            state = (state >> 1) ^ 0xEDB88320
        else:
            state >>= 1

    return state


def _raw_crc_block_zip(state: int, data: bytes) -> int:
    for b in data:
        state = _raw_crc_update_zip(state, b)

    return state


###########################
## MATRIX PRECOMPUTATION ##
##############################################################################################
# This step pre-computes the linear matrix for the CRC operation
# importing this library.
_INV_ZIP = None


def _build_inverse(raw_block_func, pack_fmt):
    """Build the inverse matrix for a given CRC variant.

    Args:
        raw_block_func: function(state, data) -> state (uses raw_update_func)
        pack_fmt: struct format for the 4‑byte patch ('<I' for ZIP)

    Returns:
        List of 32 integers representing the rows of the inverse matrix.
    """
    cols = []
    for j in range(32):
        patch_int = 1 << j
        patch = struct.pack(pack_fmt, patch_int)
        state = raw_block_func(0, patch)
        cols.append(state)

    # Build rows
    mat = [0] * 32
    for i in range(32):
        row = 0
        for j in range(32):
            if (cols[j] >> i) & 1:
                row |= 1 << j
        mat[i] = row

    # Gaussian elimination
    inv = [1 << i for i in range(32)]
    for col in range(32):
        mask = 1 << col
        pivot = None
        for row in range(col, 32):
            if mat[row] & mask:
                pivot = row
                break
        if pivot is None:
            raise RuntimeError("Matrix is singular")
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            inv[col], inv[pivot] = inv[pivot], inv[col]
        for row in range(32):
            if row != col and (mat[row] & mask):
                mat[row] ^= mat[col]
                inv[row] ^= inv[col]

    return inv


def _get_inv_zip():
    global _INV_ZIP

    if _INV_ZIP is None:
        _INV_ZIP = _build_inverse(_raw_crc_block_zip, "<I")

    return _INV_ZIP


################################
## 4-BYTE CRC PATCH CALCULATION ##
##############################################################################################
def patch_4_bytes(crc_before: int, target_crc: int) -> bytes:
    """
    Returns the 4‑byte suffix that makes CRC(data+suffix)==target_crc.

    Args:
        crc_before: CRC of the data so far (as computed by the full algorithm).
        target_crc: Desired final CRC.
    """
    # ZIP variant
    crc_zero = binascii.crc32(b"\x00\x00\x00\x00", crc_before) & 0xFFFFFFFF
    diff = target_crc ^ crc_zero
    inv = _get_inv_zip()

    # Apply inverse (little‑endian patch)
    patch_bits = 0
    for i in range(32):
        if bin(inv[i] & diff).count("1") % 2:
            patch_bits |= 1 << i

    return struct.pack("<I", patch_bits)


def compute_crc(data: bytes) -> int:
    return binascii.crc32(data, 0) & 0xFFFFFFFF


################################
## RESTRICTED SEARCH ROUTINES ##
##############################################################################################
ALL_BYTES = bytes(range(0, 256))
PRINTABLE = bytes(range(32, 127))
LETTERS = bytes(list(range(65, 91)) + list(range(97, 123)))


def get_allowed_set(restriction: str) -> bytes:
    if restriction == "PRINTABLE":
        return PRINTABLE
    elif restriction == "LETTERS":
        return LETTERS
    elif restriction == "NONE":
        return ALL_BYTES
    else:
        raise ValueError(f"Unknown restriction: {restriction}")


def check_all_allowed(suffix_bytes: bytes, allowed: bytes) -> bool:
    return all(b in allowed for b in suffix_bytes)


def find_restricted_suffix(
    original_data: bytes,
    target_crc: int,
    allowed: bytes,
    max_extra=100,
    max_attempts_per_len=2000,
) -> bytes:
    """
    Finds a suffix of up to max_extra characters within the given allowed set of bytes so that the
    original_data+suffix leads to the target_crc.

    Args:
        original_data: The data to calculate the suffix on
        target_crc: The target CRC to reach using the suffix
        allowed: Set of allowed bytes for the calculation.
        max_extra: How many characters to append in the suffix at most (default: 100)
        max_attempts_per_len: The search will perform several random attempts per attempted suffix
                              length. This controls how many attempts are made each (default: 2000)

    Returns:
        The calculated suffix (bytes)
    """
    for random_pre_len in range(0, max_extra - 4 + 1):
        for _ in range(max_attempts_per_len):
            random_pre_bytes = bytes(random.choice(allowed) for _ in range(random_pre_len))
            crc_pre = compute_crc(original_data + random_pre_bytes)
            patch = patch_4_bytes(crc_pre, target_crc)

            if check_all_allowed(patch, allowed):
                suffix = random_pre_bytes + patch

                # Should work perfectly now
                # TODO: Can remove?
                if compute_crc(original_data + suffix) == target_crc:
                    return suffix

    raise RuntimeError(f"Could not find a valid suffix within {max_extra} extra bytes.")


############################
## COMMAND LINE INTERFACE ##
##############################################################################################
def parse_int_or_hex(raw: str) -> int:
    """Parses data in the form of an integer, or hexadecimal (0xDEADBEEF)"""
    raw = raw.strip()
    if raw.lower().startswith("0x"):
        return int(raw, 16) & 0xFFFFFFFF

    return int(raw) & 0xFFFFFFFF


class DefaultOutfileAction(argparse.Action):
    """
    Custom argparse action to automatically set a default value of some file path argument (e.g. an
    output path) based on the file name value of the argument it is run on (e.g. an input
    path). Can configure the output extension. File is always saved in current working
    directory.
    """

    def __init__(self, option_strings, dest, *, action_dest="outfile", **kwargs):
        """
        Constructor for argparse actions. Extended by the additional arguments
        "action_dest", to be given as keyword arguments in the
        add_argument call in which this action is supplied.

        Additional Args:
            action_dest: What destination in the parsed args namespace the default should
                         be stored in (default: "outfile")
        """
        super().__init__(option_strings, dest, **kwargs)
        self.action_dest = action_dest

    def __call__(self, _parser, namespace, values, _option_string=None):
        # Set the given file path value into the args namespace (might be none if not given)
        setattr(namespace, self.dest, values)

        # If the value is none, provide the default (basename of file, given extension,
        # saved in current working directory)
        if getattr(namespace, self.action_dest, None) is None:
            infile_path = Path(values)
            ext = "".join(infile_path.suffixes)
            name_no_ext = values[: -len(ext)] if ext else infile_path.name
            setattr(namespace, self.action_dest, f"{name_no_ext}_crc-coll{ext}")


def main():
    ## Argument Parsing
    parser = argparse.ArgumentParser(
        description="Force a file to a target CRC‑32 by appending collision bytes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        help="Input file to conform to a certain CRC-32.",
        action=DefaultOutfileAction,
        action_dest="outfile",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        help="Where to write the colliding output file to. (Default: If input file is 'main.py', output file will be 'main_crc-coll.py')",
    )
    parser.add_argument("target_crc", help="Target CRC‑32 (<decimal> or 0x<hex>).")
    parser.add_argument(
        "-r",
        "--restrict",
        choices=["NONE", "PRINTABLE", "LETTERS"],
        default="NONE",
        help="Character restriction for added bytes (default NONE).",
    )
    parser.add_argument(
        "-s",
        "--same-line",
        action="store_true",
        help="If true, ensures the suffix is added to the last line by removing a trailing newline character if needed (default False)",
    )
    parser.add_argument(
        "--max-extra",
        type=int,
        default=80,
        help="Max extra bytes allowed to append (relevant for restricted modes only) (default 80).",
    )
    parser.add_argument(
        "--attempts-per-length",
        type=int,
        default=2000,
        help="Random attempts per tested prefix length (relevant for restricted modes only) (default 2000).",
    )
    args = parser.parse_args(
        args=None if sys.argv[1:] else ["--help"]
    )  # Print help if called without args

    ## Reading Data
    target = parse_int_or_hex(args.target_crc)
    file_path = Path(args.file)

    try:
        with open(file_path, "rb") as f:
            data = f.read()
            if args.same_line:
                # If there's a newline at the end, remove it - some editors save files such that every
                # line ends with a newline. But that's not what we want, we want our suffix to be
                # added on the last line in text files
                if data[-1] == 10:
                    data = data[:-1]
    except OSError as e:
        sys.exit(f"Error reading file: {e}")

    ## Initial Info
    crc_orig = compute_crc(data)
    print(f"Original ZIP CRC‑32: 0x{crc_orig:08X}")
    print(f"Target   ZIP CRC‑32: 0x{target:08X}")

    if args.restrict == "NONE":
        # Unrestricted: compute exact 4‑byte patch
        print("\tComputing 4‑byte patch...", end="", flush=True)
        suffix = patch_4_bytes(crc_orig, target)
        print(" done.")

        # Verify before writing
        if compute_crc(data + suffix) != target:
            sys.exit("Internal error: computed file does not match target CRC.")
    else:
        allowed = get_allowed_set(args.restrict)
        print(f"\tSearching for restricted ({args.restrict}) suffix...", end="", flush=True)
        try:
            suffix = find_restricted_suffix(
                data,
                target,
                allowed,
                max_extra=args.max_extra,
                max_attempts_per_len=args.attempts_per_length,
            )
        except RuntimeError as e:
            sys.exit(f"\nError: {e}")

        print(f" done ({len(suffix)} bytes).")

        # Just to be sure, even though the search function already verified by necessity
        if compute_crc(data + suffix) != target:
            sys.exit("Internal error: computed file does not match target CRC.")

    print(f"\tSuffix (hex): {suffix.hex()}")

    ## Write Output
    with open(args.outfile, "wb") as f:
        f.write(data + suffix)

    if args.restrict in ("PRINTABLE", "LETTERS"):
        print(f"Suffix (repr): {suffix!r}")
    print(f"Matching CRC file written to: {args.outfile}")


if __name__ == "__main__":
    main()
