#include <stdio.h>

extern int sesome(void);
extern int nothing(void);
extern int anonymous_integer;

int
main(int argc, char** argv)
{
    return nothing() + sesome() + anonymous_integer;
}
