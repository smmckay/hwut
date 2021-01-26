
/* PURPOSE: 
 *
 *    Test template for function: count.c/count
 *
 * This file contains an auto-generated template by the HWUT Unit Test Tool.
 * It is advised to answer the following questions in the initial comment.
 *
 *              WHAT DOES THE count?
 *              WHAT ARE INPUTS, OUTPUTS, HISTORY DEPENDENCIES?
 *              WHY IS THIS TEST CONSIDERED TO BE SUFFICIENT?
 *
 * Also, it is good to mentione references to research or requirement docs.
 *
 * AUTHOR: Name and/or Email
 * ORGANIZATION
 * DATE or HISTORY
 *___________________________________________________________________________*/

#include "hwut_unit.h"
#include "stdio.h"

#include "count.h"
#include "source_directory/count.c"


/* It is good style to build the sets on a set of functions for the following
 * tasks:                                                                    */

static void setup(void); /* A function that makes the test independent from 
                          * any history or external influences.              */
static void print(void); /* A function that prints the unit under test or the 
                          * functions input/output.                          */
static void test(int);   /* A function which executes the test. That is, it
                          * sets it up, applies inputs, and prints output.   */

int
main(int argc, char** argv)
{
    /* Refer to the function name, so that it is recognized as an
     * unresolved symbol and the code generator will try to resolve it.      */
    void*  dummy = count;

    hwut_info("count.c: count;\n"
              "CHOICES: One, Two, Three;\n");

    hwut_if_choice("One") {
        test(1);
    }
    hwut_if_choice("Two") {
        test(2);
    }
    hwut_if_choice("Three") {
        test(3);
    }
}

static void
test(int N)
{
    (void)N;
    setup();

    /* Test count */

    print();
}

static void 
setup(void)
{
}

static void 
print(void)
{
}
