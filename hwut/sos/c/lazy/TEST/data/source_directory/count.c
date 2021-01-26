#include "stdio.h"
#include "count.h"

static void count(void);

void print_hello(void)
{
    printf("hello world!\n");
}

static void count(void)
{
    printf("%i\n", one());
    printf("%i\n", two());
    printf("%i\n", three());
}
