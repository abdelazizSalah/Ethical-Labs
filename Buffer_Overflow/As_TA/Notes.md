## Getting started
- What is the difference between gcc and g++ ? 
  - gcc for compiling c codes.
  - g++ for compiling c++ codes. 
- gdb is for debugging c and assembly code. 
- hexedit and bless are used for viewing and editing binary files. 

## What is ASLR ? 
- Address space layout randomization
- This is mainly used to randomaize the starting address of the heap and the stack. 
- This makes it difficult to determine the exact memory address of code in each running instance of the program. 
- To disable the ASLR there are two possible ways:
    1. Disable it globally using these commands: 
        > sudo -s (Switch to root)
        > sysctl -w kernel.randomize_va_space=0 
            
        - sysctl is a utility for viewing and modifying kernel parameters. 
        - -w is write or change the parameter
        - kernel.randomize_va_space the ASLR settings. 
        - =0 disable the ASLR. 
    2. For specific programs we have 2 ways
       1. Using GDB, it will automatically be closed.
       2. Using this command:
          > setarch $(uname-m) --addr-no-randomize (program)(arguments)  
          - uname -m prints the machine architecture (This may not be necassary)
          - setarch runs a program with modified execution personality flags 
            - It says run the given program but with some modified parameters
          - --adr-no-randomize: disables ASLR for the launched process and its children.
- Canary
  - This is another name for the Stackguard
  - It is a mechanism that helps in detecting stack overflow attacks before they overwrite the function return address.
  - The canary is a placed value before the return address, so if the user modified it, the compiler detect that it has been modified, then it detects the attack, and returns falut. 
    - ![Canary](Canary.png)
  - To disable it, we can use this command: 
     > g++ -fno-stack-protector example.c
- Non-Executable Stack (NX)
  - Executable attacks nowadays are not allowed by default.
  - So if a program wants to activate this feature, it must do that explicitly. 
    - > g++ -z execstack -o example.exe example.c
      - -z execstack tells the linker to mark the stack as executable. 
    - To reverse it, we need to use 
      - g++ -z noexecstack -o example.exe example.c
- Fortify source
  - Modern compilers optimize the code written by developers during the compilation step
  - This allows the compiler to replace common code snippts corresponds to bad programming practices, and optimize the overall performance of the program. 
  - To prevent this we use the following command:
    - > g++ -U_FORTIFY_SOURCE -o example.exe example.c
  - To activate it back:
    - > g++ -D_FORTIFY_SOURCE=1 -o example.exe example.c
- Position Independent Code
  - Programs are compiled so they can run correctly regardless of where they are loaded in memory. 
  - This is important for shared libraries and ASLR. 
  - However, because code and libraries can be loaded at different addresses each run
    -  debugging and exploit analysis become more difficult
    - Without PIE:
      - Starting address of main will always be 0x401156
    - With PIE
      - each run it will have a different address   
    -  Thus, for this case we are going to turn it off using this command:
       -  g++ -no-pie -o exmaple.exe example.c
-  How is PIE different from ASLR? 
   -  ASLR: This is the OS mechanism for randomizing memory addresses. 
   -  PIE: A way of compiling a program so that ASLR can randomize the program's code section.
   -  Example: 
      -  Without PIE
         -  if ASLR is enabled:
            -  Stack -> randomized
            -  Heap -> randomized
            -  Libraries -> randomized
            -  Program -> fixed address
               -  So the main address always start from the same location 0x401165
               -  but everything else is randomized due to ASLR
         -  But with PIE, everytime, we will have a new starting memory address location
            -  main -> 0x405325
            -  main -> 0x405535
            -  main -> 0x135645
-  