#include <stdio.h>
#include <stdlib.h>

int main () { 
    char * shell = (char*) getenv("MYSHELL"); 

    if (shell) { 
        printf(" Value:  %s\n", shell); 
        printf(" Address: 0x%x\n", (unsigned int) shell);
    }

    return 1; 
}