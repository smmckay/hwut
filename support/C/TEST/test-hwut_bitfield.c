/* PURPOSE:
 *
 * This tests check on the high level interface for bitfield encoding and 
 * decoding. That is they work on the two functions:
 *
 *                      hwut_bitfield_encode(...)
 *                      hwut_bitfield_decode(...)
 *
 * Those two functions receive an array to be filled and a variable argument
 * list that contains pairs of (bit_n, value). When a bit_n of '-1' is detected
 * the argument list is considered terminated. 
 *
 * The tests of this file consider a number of 1, 2, and 3 values to be encoded.
 * The array is of size 4byte. A value to be coded is either all ones or all 
 * zeroes. Two successive values are never of the same 'type'. A bitfield print
 * therefore, shows nicely what values are written at what place. 
 *
 * Every value to be encoded appears in all possible bit numbers and 'types'.
 *
 * AUTHOR: Frank-Rene Schaefer. 
 * DATE:   2014                                                              */

#if 0
<<hwut-iterator:    One>>
-----------------------------------------------------------------------------------------------------------------
#include <stdint.h>
-----------------------------------------------------------------------------------------------------------------
uint32_t bit_n1;    
         |1:32|;   
-----------------------------------------------------------------------------------------------------------------

<<hwut-iterator:    Two>>
-----------------------------------------------------------------------------------------------------------------
#include <stdint.h>
-----------------------------------------------------------------------------------------------------------------
uint32_t bit_n1;   uint32_t bit_n2;    
         |1:32|;            |1:32|;    
-----------------------------------------------------------------------------------------------------------------

<<hwut-iterator:    Three>>
-----------------------------------------------------------------------------------------------------------------
#include <stdint.h>
-----------------------------------------------------------------------------------------------------------------
uint32_t bit_n1;   uint32_t bit_n2;   uint32_t bit_n3;
         |1:32|;            |1:32|;            |1:32|;
-----------------------------------------------------------------------------------------------------------------

<<hwut-iterator:    Error>>
-----------------------------------------------------------------------------------------------------------------
#include <stdint.h>
-----------------------------------------------------------------------------------------------------------------
uint32_t bit_n1; uint32_t bits1; uint32_t bit_n2; uint32_t bits2;  uint32_t bit_n3; uint32_t bits3;
              8;            256;              16;          65535;               24;       16777215;
              8;            255;              16;          65536;               24;       16777215;
              8;            255;              16;          65535;               24;       16777216;
-----------------------------------------------------------------------------------------------------------------

#endif

#include <stdio.h> 
#include <hwut_unit.h> 
#include <hwut_bitfield.h>
#include "BitFieldIterator.h"

#define ArraySize    4 /* = 32 bit. */
struct { 
    uint8_t  array[ArraySize];
    uint32_t in[ArraySize];
    uint32_t out[ArraySize];
    int      test_count;
} self;

static void one();
static void one_print(One_t* it);
static void two();
static void two_print(Two_t* it);
static void three();
static void three_print(Three_t* it);
static void error_cases();

/* Get a mask of 'N' bits: 2^bit_n - 1                                       */
#define     self_mask(BitN) ((BitN) == 32 ? 0xFFFFFFFF : (1<<(BitN)) - 1)

int main(int argc, char** argv)
{
    hwut_info("hwut_bitfield: bitfield encode / decode;\n"
              "CHOICES: 1, 2, 3, error;");

    self.test_count = 0;

    hwut_if_choice("1")     { one(); }
    hwut_if_choice("2")     { two(); }
    hwut_if_choice("3")     { three(); }
    hwut_if_choice("error") { error_cases(); }

    printf("Terminated: %i checks completed.\n", self.test_count);
    return 0;
};

static void 
one()
{
    One_t it;
    One_init(&it);

    while( One_next(&it) )
    {	
        /* Generate max value for number of bits                             */
        self.in[0] = self_mask(it.bit_n1);

        /* Poisson array => Check if 'encode/decode' start properly.         */
        memset((void*)self.array, 0x5A, ArraySize);

        hwut_verify_it(&it,
            -1 == hwut_bitfield_encode(self.array, ArraySize, 
                                       it.bit_n1, self.in[0], 
                                       -1)
        );

        one_print(&it);

        hwut_verify_it(&it, 
            -1 == hwut_bitfield_decode(self.array, ArraySize, it.bit_n1, &self.out[0], -1)
        );
        hwut_verify_it(&it, self.in[0] == self.out[0]);

        ++self.test_count;
    }
}

static void
one_print(One_t* it)
{
    hwut_bitfield_print_numeric(self.array, ArraySize, 16,
                                it->bit_n1, -1);
    hwut_bitfield_print_borders(self.array, ArraySize, 
                                it->bit_n1, 
                                -1);
    hwut_bitfield_print_bytes(self.array, ArraySize);
    printf("\n");
}

static void 
two()
{
    Two_t it;
    int   i = 0;

    for(i=0; i<2; ++i) {
        Two_init(&it);

        while(Two_next(&it)) {

            if( 32 != (it.bit_n1 + it.bit_n2) ) {
                continue;
            }

            /* Poisson array => Check if 'encode/decode' start properly.     */
            memset((void*)self.array, 0x5A, ArraySize);

            /* One value all ones; the next one only zeroes.                 */
            self.in[0] = (i == 0) ? self_mask(it.bit_n1) : 0x00;
            self.in[1] = (i != 0) ? self_mask(it.bit_n2) : 0x00;

            hwut_verify_it(&it,
                    -1 == hwut_bitfield_encode(self.array, ArraySize,
                        it.bit_n1,  self.in[0], 
                        it.bit_n2,  self.in[1],
                        -1)
                    );

            two_print(&it);

            hwut_verify_it(&it,
                    -1 == hwut_bitfield_decode(self.array, ArraySize,   
                        it.bit_n1,  &self.out[0], 
                        it.bit_n2,  &self.out[1], 
                        -1)
                    );

            hwut_verify_it(&it, self.in[0] == self.out[0]); 
            hwut_verify_it(&it, self.in[1] == self.out[1]);

            ++self.test_count;
        }
    }
}

static void 
two_print(Two_t* it)
{
    hwut_bitfield_print_bytes(self.array, ArraySize);
    printf("\n");
}

static void 
three()
{
    Three_t it;
    int     i = 0;

    for(i=0; i<2; ++i) {
        Three_init(&it);

        while(Three_next(&it)) {
            if( 32 != (it.bit_n1 + it.bit_n2 + it.bit_n3)) {
                continue;
            }

            /* Poisson array => Check if 'encode/decode' start properly.     */
            memset((void*)self.array, 0x5A, ArraySize);

            /* generate max value for number of bits                         */
            self.in[0] = (i == 0) ? self_mask(it.bit_n1) : 0x00;
            self.in[1] = (i != 0) ? self_mask(it.bit_n2) : 0x00;
            self.in[2] = (i == 0) ? self_mask(it.bit_n3) : 0x00;

            hwut_verify_it(&it, 
                    -1 == hwut_bitfield_encode(self.array, ArraySize, 
                        it.bit_n1, self.in[0], 
                        it.bit_n2, self.in[1], 
                        it.bit_n3, self.in[2], 
                        -1)
                    );

            three_print(&it);

            hwut_verify_it(&it, 
                    -1 == hwut_bitfield_decode(self.array, ArraySize, 
                        it.bit_n1, &self.out[0], 
                        it.bit_n2, &self.out[1], 
                        it.bit_n3, &self.out[2], 
                        -1)
                    );
            hwut_verify_it(&it, self.in[0] == self.out[0]);
            hwut_verify_it(&it, self.in[1] == self.out[1]);
            hwut_verify_it(&it, self.in[2] == self.out[2]);

            ++self.test_count;
        }
    }
}

static void 
three_print(Three_t* it)
{
    hwut_bitfield_print_bytes(self.array, ArraySize);
    printf("\n");
}


static void 
error_cases()
{
    Error_t it;
    Error_init(&it);

    while(Error_next(&it))
    {
        Error_print_table_line(stdout, &it, ",");
        /* Poisson array => Check if 'encode/decode' start properly.         */
        memset((void*)self.array, 0x5A, ArraySize);

        hwut_verify_it(&it, 
            0 <= hwut_bitfield_encode(self.array, ArraySize, it.bit_n1, it.bits1, it.bit_n2, it.bits2, it.bit_n3, it.bits3, -1)
        );

        hwut_bitfield_decode(self.array, ArraySize, it.bit_n1, &self.out[0], it.bit_n2, &self.out[1], -1);

        ++self.test_count;
    }
}
