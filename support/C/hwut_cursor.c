/*  SPDX license identifier: LGPL-2.1
 * 
 *  Copyright (C) Frank-Rene Schaefer, private.
 *  Copyright (C) Frank-Rene Schaefer, 
 *                Visteon Innovation&Technology GmbH, 
 *                Kerpen, Germany.
 * 
 *  This file is part of "HWUT -- The hello worldler's unit test".
 * 
 *                   http://hwut.sourceforge.net
 * 
 *  This file is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License, or (at your option) any later version.
 * 
 *  This file is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 *  Lesser General Public License for more details.
 * 
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this file; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor,
 *  Boston, MA 02110-1301 USA
 * 
 * --------------------------------------------------------------------------*/
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
hwut_cursor_iteration_number(hwut_cursor_t* me)
/* RETURNS: The total number of iterations.                                  */
{
    long                       result = 0;
    const hwut_cursor_index_t* dim_p  = &me->index_dim[0];
    const hwut_cursor_index_t* End    = &me->index_dim[(int)me->index_n];

    for(; dim_p != End ; ++dim_p) {
        result *= *dim_p;
    }
    return result;
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
