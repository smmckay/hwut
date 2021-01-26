#include "number.h"

int
number1()
{
    static int call_n = 0;
    if( call_n++ > 10 ) return; /* Avoid infinit recursion. */
    return number0();
}
