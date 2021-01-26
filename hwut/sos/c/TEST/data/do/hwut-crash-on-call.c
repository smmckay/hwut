/*_____________________________________________________________________________
 *
 * Crash-on-Call Stubs: (HWUT - generated code)
 *
 * This module implements functions which are supposed to crash upon call.
 * Their function signature differs (most probably) from the original one,
 * but this is not an issue for the linker--IT WILL LINK ANYWAY!\N *
 * If the function call does not cause a crash, then the 'exit()' call ensures
 * that the program will exit. Crash-on-call stubs are ONLY to be used for
 * functions that are absolutely not related to the unit under test.
 *
 * Make sure that the test program makes a 'printf("<termination>
");' call
 * right before officially terminating. Otherwise, HWUT might not detect
 * premature terminations.
 *
 * To comply with some pedantics, prototypes are given before definitions.
 *___________________________________________________________________________*/
#include "stdlib.h"
#include "stdio.h"

/* Prototypes                                                                */
static void self_crash_on_call_print(const char* N);
void undefined_function_so_crash_on_call(void);

/* Definitions                                                               */
static void self_crash_on_call_print(const char* N) {
    printf("Unexpected call to '%s' -- abort!", N);
}
void undefined_function_so_crash_on_call(void) { self_crash_on_call_print("undefined_function_so_crash_on_call"); exit(-1); }
