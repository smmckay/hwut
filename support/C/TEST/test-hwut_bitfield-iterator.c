/* PURPOSE:
 *
 * The bitfield encoders/decoders are built upon bitfield iterators. The tests
 * of this file check on the lowest level functions. They can only treat values
 * which are at max. 8 bit long
 *
 *                      self_iterator_append_small(...)
 *                      self_iterator_pop_small(...)
 *
 * The tests works on an array of N bytes. Before a test the iterator is 
 * setup to a certain bit offset in the array. Then a certain number of bits
 * are written. The tests iterate over all combinations of offset and number
 * of bytes. The CHOICES 1, 2, and 3 select the number of bytes to work on.  
 *
 * AUTHOR: Frank-Rene Schaefer. 
 * DATE:   2014                                                              */

#include "stdint.h"
#include <stdio.h> 
#include <hwut_unit.h> 
#include "../hwut_bitfield.c"

static uint32_t self_test_setup(self_iterator_t* it, 
                                int              BitOffset, 
                                int              ValueBitN,
                                uint8_t*         array, 
                                size_t           ByteN); 
static void     self_test_print_head();
static void     self_test_print(self_iterator_t* it, 
                                uint8_t          BitOffset, 
                                uint8_t          BitN, 
                                uint8_t*         array, 
                                uint8_t          ByteN, 
                                int              result);

#define ArraySize 10


int
main(int argc, char** argv)
{
    uint8_t          array[ArraySize];
    uint8_t          bit_offset;
    uint8_t          value_bit_n;
    uint8_t          byte_n;
    uint32_t         value = 0;
    self_iterator_t  it;
    uint32_t         value_back = 0;
    self_iterator_t  backup;
    int              result;
    int              count_pop_n = 0;

    hwut_info("hwut_bitfield: iterator append/pop small;\n"
              "CHOICES:  1, 2, 3;");

    hwut_if_choice("1") { byte_n = 1; }
    hwut_if_choice("2") { byte_n = 2; }
    hwut_if_choice("3") { byte_n = 3; }

    /* NOTE: We use 'light barriers'. That is, the array is set all to zeroes.
     *       Then, only the space from begin+1 to end-1 is used. After the 
     *       operation the begin and end is checked whether the changed.     */
    self_test_print_head();
    for(bit_offset=0; bit_offset <= byte_n * 8; ++bit_offset) {
        printf("\n");
        for(value_bit_n=1; value_bit_n < 9 ; ++value_bit_n) {
            value  = self_test_setup(&it, bit_offset, value_bit_n, 
                                     &array[0], byte_n);
            backup = it;

            result = self_iterator_append_small(&it, value_bit_n, value);     

            hwut_verify(array[0]        == 0);
            hwut_verify(array[byte_n+1] == 0); 

            self_test_print(&it, bit_offset, value_bit_n, array, byte_n, result);        

            if( result ) {
                it = backup;
                hwut_verify(self_iterator_pop_small(&it, value_bit_n, &value_back) == 1);     
                hwut_verify(value_back == value);
                ++count_pop_n;
            }
        }
    }

    printf("\nTerminated: (including %i pop-operations)\n", count_pop_n);

    return 0;
}


static void
self_test_print_head()
{
    printf("offset bit_n free_bit_n byte_p result  bitfield\n");
}

static void 
self_test_print(self_iterator_t* it, uint8_t BitOffset, uint8_t ValueBitN, uint8_t* array, uint8_t ByteN, int result)
/* Prints a row with information about the iterators initial status, the value
 * and the bitfield that results from writing.                               */
{    
    printf("%6i  %4i  %9i %6i  %5s  ", 
           (int)BitOffset, (int)ValueBitN, it->free_bit_n, 
           (int)(it->byte_p - &array[1]), result ? "true" : "false");
    hwut_bitfield_print_bytes(array, ByteN + 2);
    printf("\n");
}

uint32_t
self_test_setup(self_iterator_t* it, 
                int              BitOffset, 
                int              ValueBitN,
                uint8_t*         array, 
                size_t           ByteN) 
/* Sets up the iterator so that it points to the given BitOffset. 
 *
 * One byte before the first byte and one byte after the last byte is filled
 * with light barrier values. It can later be checked that those values are
 * not accidentally modified by the function under test.
 * 
 * RETURNS: A value that just fits the given bit number.                     */
{
    /* Setup:
     *             [L][ ][ ][ ][ ][ ][ ][ ][ ][L] 
     *                 '------ content -----'                                */
    memset((void*)array, 0x0,  ArraySize);

    self_iterator_init(it, ByteN, &array[1]);
    it->free_bit_n = 8 - (BitOffset % 8);
    it->byte_p     = array  + (BitOffset / 8) + 1;

    return (1 << ValueBitN) - 1;                   
}
