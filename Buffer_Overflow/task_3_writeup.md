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
