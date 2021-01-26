#include "hwut_unit.h"
#include "hwut_cursor.h"
#include "hwut_cursor.c"

#include "stdio.h"
#include "stdarg.h"

static void test(int N, ...);

int
main(int argc, char** argv) 
{
	hwut_info("Generator: Iterator's cursor API;\n");

    /* 1 parameter */
    test(1, 1); 
    test(1, 2); 
    test(1, 3); 

    /* 2 parameters */
    test(2, 1, 1); 
    test(2, 1, 2); 
    test(2, 1, 3); 
    test(2, 2, 1); 
    test(2, 2, 2); 
    test(2, 2, 3); 

    /* 3 parameters 
     * These tests are not strategically selected. Rather take some
     * subset of possible settings for verification.                      */
    test(3, 1, 1, 1); 
    test(3, 2, 2, 2); 
    test(3, 1, 2, 3); 
    test(3, 1, 3, 2); 
    test(3, 2, 1, 3); 
    test(3, 2, 3, 1); 
    test(3, 3, 2, 1); 
    test(3, 3, 1, 2); 
    
    if( 0 ) {
        (void)hwut_cursor_to_key((void*)0);
        (void)hwut_cursor_from_key((void*)0, (hwut_cursor_key_t)0);
    }

    return 0;
}

static void
test(int N, ...)
/* Use the 'next' function to iterate over all permutations of the 
 * cursor. For every permutation compute the 'key' and from the 'key'
 * compute the setting backwards.                                            */
{
	va_list              arg_p;
	hwut_cursor_t        this;
	hwut_cursor_t        that;
    hwut_cursor_key_t    key;
	long                 i;
	hwut_cursor_index_t  this_indexArray[N];
	hwut_cursor_index_t  that_indexArray[N];
	hwut_cursor_index_t  indexDimArray[N]; 
	printf("_____________________________________________________________ \n\n");

	/* Determine the max-values for each index.                              */
	va_start(arg_p, N);
	for(i=0; i < N; ++i) indexDimArray[i] = va_arg(arg_p, int);
    va_end(arg_p);

	/* Initialize the cursor object.                                         */
	hwut_cursor_init(&this, N, this_indexArray, indexDimArray);

	printf("%i Dimension(s): ", N);
    hwut_cursor_print_dimensions(&this); printf("\n");
    printf("\n");

	/* Iterate over all permutations.                                        */
	for(i=0; i < 77777 ; ++i) {
		printf("    "); hwut_cursor_print(&this); 
        
        /* cursor_to_key()   */
        key = hwut_cursor_to_key(&this);
        printf("<=> key: %06i <=>", (int)key);

        /* cursor_from_key() */
        hwut_cursor_init(&that, N, that_indexArray, indexDimArray);
        hwut_cursor_from_key(&that, key);
		hwut_cursor_print(&that); 
#if 0
#endif

        printf("\n");
        /* next()            */
        if( ! hwut_cursor_next(&this) ) break;
	}
    printf("\n");
}
