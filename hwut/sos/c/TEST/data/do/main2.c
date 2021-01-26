#include "stdio.h"
#include "number.h" /* --> #include "letter.h" */
int number0();
int letter0();

int
main(int argv, char** argc)
{
    printf("Have more fun!\n");
    return letter0() - number0();
}
