#include "hwut_cursor.h"

void              
hwut_cursor_init(hwut_cursor_t*             me, 
                 int                        N, 
                 hwut_cursor_index_t*       indexArray, 
                 const hwut_cursor_index_t* indexDimArray)
{
    int i = 0;
    assert(N > 0);

	me->index_n   = N;
	me->index     = indexArray;
	me->index_dim = indexDimArray;

    for(i=0; i < N ; ++i) {
        me->index[i] = 0;
        assert(me->index_dim[i] != 0);
    }
}

int 
hwut_cursor_next(hwut_cursor_t* me)
/* Increments the setting of the 'me'. 
 *
 * RETURNS: 1 if the found setting is valid. 
 *          0 if the end of the possible setting has been found.             */
{
    int i = me->index_n - 1;
    while( 1 + 1 == 2 ) {
        me->index[i] += 1;
        if( me->index[i] < me->index_dim[i]) {
            return 1;          /* Found permutation.                         */
        }
        else if( i == 0 ) {
            return 0;          /* No further permunation available.          */
        }
        me->index[i] = 0;
        i -= 1;
    }
    return 1;                      
}

hwut_cursor_key_t
hwut_cursor_to_key(hwut_cursor_t* me) 
/* RETURNS: A numeric value, i.e. a 'key' which represents a particular setting.
 *          The 'setting' is represented by the 'index[]' array of the me.
 *                                                                           
 * This function is the inverse of 'hwut_cursor_from_key()'.                 */
{
    long   result = 0;
    int    i      = 0;

    for(i=0; ;) {
        result += me->index[i];
        ++i;
        if( i == me->index_n ) {
            break;
        }
        result *= me->index_dim[i];
    }
    return result;
}

int
hwut_cursor_from_key(hwut_cursor_t* me, hwut_cursor_key_t key) 
/* Sets the me's indicies corresponding a numeric 'key'. 
 * RETURNS: 1 -- if this was possible.        
 *          0 -- if this was not possible.
 * This function is the inverse of 'hwut_cursor_to_key()'.                   */
{
    long   remainder = 1;
    int    i         = 0;

    for(i=me->index_n - 1; i >=0 ; --i) {
        remainder    = key % me->index_dim[i];
        me->index[i] = remainder; 
        key          = (key - remainder) / me->index_dim[i];
    }
    return key;
}


#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void
hwut_cursor_print(hwut_cursor_t* me)
{
	int i=0;
	for(i=0; i < me->index_n; ++i) {
		printf("[%i]", (int)me->index[i]);
	}
}

void
hwut_cursor_print_dimensions(hwut_cursor_t* me)
{
	int i=0;
	for(i=0; i < me->index_n; ++i) {
         printf("[%i]", (int)me->index_dim[i]);
    }
}
#endif
