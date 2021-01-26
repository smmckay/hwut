#include "letter.h"
/* Make sure that there is at least one include directory that is only used 
 * from this source directory, not from others.                              */
#include "only-in-numbers.h"
#include "string.h"

int nevercalled(void);
int undefined_function_so_crash_on_call(void);

int
number0()
{
    static int call_n = 0;
    static int dummy  = 4711;
    if( call_n++ > 10 ) return;                  /* Avoid infinit recursion. */

    /* Call 'memcpy' to see how standard lib functions are treated.          */
    memcpy(&call_n, &dummy, sizeof(int));
    return letter0() + letter1();
}

int
nevercalled(void)
{
    undefined_function_so_crash_on_call();
}
