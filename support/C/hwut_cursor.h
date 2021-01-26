#ifndef INCLUDE_GUARD_HWUT_CURSOR_H
#define INCLUDE_GUARD_HWUT_CURSOR_H
/* vim:setlocal ft=c: 
 *
 * This file implements a n-dimensional space 'cursor' in C. The setting 
 * of the me represents a parameter setting. Provided are functions to 
 * initialize and increment the multi-dimensional me. Additionally, 
 * functions to map from and to a numeric key are provided. 
 *
 * To map from a cursor to a setting, a specific setting_map is required. 
 * E.g. a setting map for a 3-dimensional space:
 *
 *                 0: "otto", "fritz", "frank", "marvin"
 *                 1: 1.25,   2.5
 *                 2: 3.14,   0.815 
 *
 * interprets the me [ [3] [1] [0] ] as the element 3 from '0', and the
 * element 1 from '1' and element 0 from '2'. The resulting setting is
 *
 *                 0: "marvin"  (element 3 of '0')
 *                 1: 2.5       (element 1 of '1')
 *                 2: 3.14      (element 0 of '2')
 * 
 * Thus, walking through the cursor's space means walking through all permu-
 * tations of the given settings map. The set of possible settings can be 
 * associated with an grid of equi-distant points in an n-dimensional space. 
 * The number of points in one dimension is the same of any combination. The
 * setting_map represents an orthogonal space. That is, for any given 
 * combination there is only one cursor setting, and vice versa.
 *
 * (C) Frank-Rene Schaefer.                                                  */
#include "assert.h"

typedef long hwut_cursor_index_t;
typedef long hwut_cursor_key_t;

typedef struct {
    /* A cursor consisting of indices of multiple dimensions. The setting of
     *
     *                        index[i] = k 
     * 
     * tells that the parameter 'i' has to be set to its k's value. A setting
     *
     *                        index_dim[i] = q          
     *
     * tells that the index for parameter 'i' (the 'k' from above) can only be
     * lesser than 'q'. 'q' is the dimension of parameter 'i'.               */
    hwut_cursor_index_t*       index;
    const hwut_cursor_index_t* index_dim;
    int                        index_n;
} hwut_cursor_t;

void              hwut_cursor_init(hwut_cursor_t*             me, 
                                   int                        N, 
                                   hwut_cursor_index_t*       indexArray, 
                                   const hwut_cursor_index_t* indexDimArray);
int               hwut_cursor_next(hwut_cursor_t* me);
hwut_cursor_key_t hwut_cursor_iteration_number(hwut_cursor_t* me);
hwut_cursor_key_t hwut_cursor_to_key(hwut_cursor_t* me);
int               hwut_cursor_from_key(hwut_cursor_t*    me, 
                                       hwut_cursor_key_t key);

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
#include "stdio.h"
void              hwut_cursor_print(hwut_cursor_t* me);
void              hwut_cursor_print_dimensions(hwut_cursor_t* me);
#endif

#define hwut_IARRAY_print(X, Suffix) \
        do {                                     \
            printf("{ ");                        \
            for(i=0; i<X->length; ++i) {         \
               printf("%i, ", (int)X->data[i]);  \
            }                                    \
            printf("}%s", Suffix);               \
        } while(0)

#define hwut_FARRAY_print(X, Suffix) \
        do {                                       \
            printf("{ ");                          \
            for(i=0; i<X->length; ++i) {           \
               printf("%f, ", (float)X->data[i]);  \
            }                                      \
            printf("}%s", Suffix);                 \
        } while(0)


#endif                                         /* INCLUDE_GUARD_HWUT_CURSOR_H */
