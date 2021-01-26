#include <stdio.h>

extern int some(void);

int
main(int argc, char** argv)
{
    printf("hello world!\n");  
    return some();
}
