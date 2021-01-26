#include <hwut_unit.h>
#include <hwut_bitfield.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdint.h>
#include <assert.h>

typedef struct {
    uint8_t* byte_p;      /* pointer to current byte.                        */
    uint8_t* end;         /* pointer to first byte after the array.          */
    int      free_bit_n;  /* number of free bits in current byte.            */
} self_iterator_t;


/* Get a mask of 'N' bits: 2^bit_n - 1                                       */
#define     self_mask(BitN) ((BitN) == 32 ? 0xFFFFFFFF : (1<<(BitN)) - 1)

/* 'bit_n' must be of 'int' and not of 'size_t', because it must homogenously
 * fit with the terminating '-1' bit number of the variable argument lists.  */
static void self_iterator_init(self_iterator_t* me, size_t size, uint8_t* array);
static int  self_iterator_append(self_iterator_t* me, int bit_n, uint32_t value);
static int  self_iterator_append_small(self_iterator_t* me, int bit_n, uint8_t value);
static int  self_iterator_pop(self_iterator_t* me, int bit_n, uint32_t *value);
static int  self_iterator_pop_small(self_iterator_t* it, int bit_n, uint32_t* value);

static void self_print_calculate_offset(int* offset, int* bit_n);
static void self_print_value(int* offset, int bit_n, uint32_t value, int base);

int
hwut_bitfield_encode(uint8_t* array, size_t ArraySize, ...)
/* Encode a list of unsigned integer values on a variable argument list. The
 * argument list must consist of pairs 'bit_n, value' which means that 'value'
 * will occupy 'bit_n' bits. The values are written in the order that they
 * appear in the argument list. A final argument of '-1' for the bit_n 
 * determines the end of the list. 
 *
 * RETURNS: -1         -- Ok; all elements have been written into array.
 *          Index >= 0 -- Error; The element given at position 'Index' does 
 *                        not fit. (Either frame too small, or bit number is 
 *                        insufficient.)                                     */
{    
    va_list          argp;
    int              bit_n = 0;
    uint32_t         value = 0;
    self_iterator_t  it;
    int              arg_index = -1;
    
    /* The iterator append functions require to write on zeroed out bytes.   */
    memset((void*)&array[0], 0x0, ArraySize);
    self_iterator_init(&it, ArraySize, array);
    
    va_start(argp, ArraySize);
    while( 1 + 1 == 2 ) {
        bit_n = va_arg(argp, int);
        ++arg_index;
        if( bit_n < 0 ) {
            break;
        }
        value = va_arg(argp, uint32_t);    

        if( ! self_iterator_append(&it, bit_n, value) ) {
            va_end(argp);
            return arg_index;
        }
    }
    va_end(argp);
    
    return -1;
}

int
hwut_bitfield_decode(const uint8_t* ConstArray, size_t ArraySize, ...)
/* Decode a list of unsigned integer values on a variable argument list. The
 * argument list must consist of pairs 'bit_n, &value' which means that 'bit_n'
 * bits will be read on stored into '*value'. The values are accessed in the 
 * order that they appear in the argument list. A final argument of '-1' for 
 * the bit_n determines the end of the list. 
 *
 * RETURNS: -1         -- Ok; all elements have been read from array.
 *          Index >= 0 -- Error; The element given at position 'Index' could 
 *                        not be read.                                       */
{
    va_list          argp;
    int              bit_n = 0;
    uint32_t*        value_p;
    int              arg_index = 0;
    self_iterator_t  it;

    /* Currently, there is only one type of iterator taking a non-const array.
     * It is used for reading and writing. So, copy the constant to variable.*/
    uint8_t*         tmp_non_const_array = (uint8_t*)malloc(ArraySize);
    memcpy(tmp_non_const_array, ConstArray, ArraySize);

    self_iterator_init(&it, ArraySize, tmp_non_const_array);

    va_start(argp, ArraySize);
    while( 1 + 1 == 2 ) {
        bit_n = va_arg(argp, int);
        if( bit_n < 0 ) {
            arg_index = -1;
            break;
        }
        value_p = va_arg(argp, uint32_t*);
        if( ! self_iterator_pop(&it, bit_n, value_p) ) {
            break;
        }
    }
    va_end(argp);

    free(tmp_non_const_array);
    return arg_index;
}

static void
self_iterator_init(self_iterator_t* it, size_t size, uint8_t* array)
/* Initialize the iterator. Let '.byte_p' point to the beginning of the array. 
 * The '.end_p' is set to one after the last byte of the array. It is used to 
 * determine the end of the iteration. The free bit number is set to 8. This 
 * means, that in current first byte still 8 bits are available.             */
{
    it->byte_p     = &array[0];
    it->end        = &array[size];
    it->free_bit_n = 8;    
}

int
self_iterator_append(self_iterator_t* it, int bit_n, uint32_t value)
/* Append an unsigned integer value to the array using the iterator. The
 * given 'value' is placed on 'bit_n' bits.
 *
 * IMPORTANT: It is assumed that the place where the bits are to be put 
 *            is all zeroed out!
 * 
 * RETURNS: 1 -- if value has been written into whatsoever iterator points to.
 *               (iterator has been updated)
 *          0 -- write failed.
 *               (iterator has NOT been updated)
 *
 * EXPLANATION:
 *
 *         <-- bit_n > 8 -->
 *   [][][][][][]...[][][][][][]
 *
 *     left_bit_n = bit_n - free_bit_n
 *
 *            >> left_bit_n        
 *   [][][][][][]...[][][][][][]
 *    
 *     only header value is left and passed to function
 *      [][][][][][] => self_iterator_append_small(it, free_bit_n, header_value)
 *
 *           <-- value -->                <-- << left_bit -->
 *   [][][][][][]...[][][][][][]    XOR [][][][][][]...[][][][][][]    
 *
 *   --> remove the already written header                                   */
{
    const uint32_t  max          = self_mask(bit_n);
    uint32_t        header_value = 0x0;
    int             left_bit_n   = 0x0;
    assert(bit_n > 0);

    if( value > max ) {
        return 0;
    }

    while ( bit_n > it->free_bit_n ) {
        left_bit_n   = bit_n - it->free_bit_n;
        /* extract header value which is fits into free bits.                */
        header_value = (value >> (left_bit_n));    
        /* remove header, and shift.                                         */
        value       ^= (header_value << (left_bit_n));
        /* update bit number: subtract length of removed header              */
        bit_n        = left_bit_n;                        

        /* The header_value MUST fit the given bit_n! */
        if( ! self_iterator_append_small(it, it->free_bit_n, header_value) ) {
            return 0;
        }
    }
    if( bit_n == 0 ) {
        return 1;
    }
    return self_iterator_append_small(it, bit_n, value);
}

static int
self_iterator_pop(self_iterator_t* it, int bit_n, uint32_t* result)
/* Pop 'bit_n' from the array iterated through by 'it'. The result is written
 * to '*result'.
 *
 * RETURNS: 0 -- if there was an error.
 *          1 -- if the value has been read successfully.                    */
{
    uint32_t  tmp;
    *result = 0;

    while( bit_n > 8 ) {
        if( ! self_iterator_pop_small(it, 8, &tmp) ) {
            return 0;
        }
        bit_n   -= 8;
        *result |= (tmp << bit_n);
    }
    if( bit_n != 0 ) {
        if( ! self_iterator_pop_small(it, bit_n, &tmp) ) {
            return 0;
        }            
        *result |= tmp;
    }
    return 1;
}

static int
self_iterator_append_small(self_iterator_t* it, int bit_n, uint8_t value)
/* Append a value which takes 8 bit or less to the current bitfield using     
 * the iterator. 
 *
 * IMPORTANT: It is assumed that the place where the bits are to be put 
 *            is all zeroed out!
 * 
 * RETURNS: 1 -- if value has been written into whatsoever iterator points to.
 *               (iterator has been updated)
 *          0 -- write failed.
 *               (iterator has NOT been updated)                             
 *
 * EXPLANATION: Two cases:
 *
 *     (1) bit_n > free_bit_n:
 *        
 *                          |<----- bit_n ----->|
 *                        [ ][ ][ ][ ][ ][ ][ ][ ]
 *                            /  /  /   \  \  \  \
 *                           /  /  /     \  \  \  \
 *         |--- bit_p -->|  /  /  /       \  \  \  \
 *         [ ][ ][ ][ ][ ][ ][ ][ ]       [ ][ ][ ][ ][ ][ ][ ][ ]
 *                        |<- f ->|                   |<--- s ---|   
 *                 1st Byte                        2nd Byte
 *        
 *        
 *        
 *     (2) bit_n < free_bit_n:
 *        
 *                 |< bit_n >|
 *          [ ][ ][ ][ ][ ][ ][ ][ ]
 *                            /  /  
 *                           /  /  
 *         |--- bit_p -->|  /  /  
 *         [ ][ ][ ][ ][ ][ ][ ][ ]       [ ][ ][ ][ ][ ][ ][ ][ ]
 *                        |<- f ->|                   |<--- s ---|
 *                 1st Byte                        2nd Byte
 *                                                                           */
{
    /* Ensure, that the value does not exceed its borders.                   */
    assert(bit_n != 0);
    assert(bit_n <= 8);
    assert(value <= self_mask(bit_n));

    if( bit_n == it->free_bit_n ) {
        if( it->byte_p == it->end ) {                         /* space left? */
            return 0;
        }
        /* shift right: bit_n - f */
        it->byte_p[0] |= value;
        it->free_bit_n = 8; 
        ++(it->byte_p);
    }
    else if( bit_n < it->free_bit_n ) {
        if( it->byte_p == it->end ) {                         /* space left? */
            return 0;
        }
        it->byte_p[0] |= value << (it->free_bit_n - bit_n);                 
        it->free_bit_n -= bit_n;
    }
    else {
        if( it->byte_p >= it->end - 1 ) {                     /* space left? */
            return 0;
        }
        it->byte_p[0] |= (value >> (bit_n - it->free_bit_n));
        ++(it->byte_p);
        /* shift left:  8 - (bit_n - f) */
        it->free_bit_n = (8 - (bit_n - it->free_bit_n));
        it->byte_p[0] |= (value << it->free_bit_n);
    }
    return 1;
}

static int
self_iterator_pop_small(self_iterator_t* it, int bit_n, uint32_t* value)
/* Pop a 'small' value from the array. Small means that it occupies not more 
 * than 8 bit. Write the content into '*value'.
 *
 * RETURNS: 1 -- Oll korrekt.
 *          0 -- It was not possible to write a value of the given bit number 
 *               into the array.                                             */
{
    int      left_bit = 0;
    uint32_t mask = 0;
    uint32_t high = 0, low = 0;


    if( bit_n == it->free_bit_n ) {
        if( it->byte_p == it->end ) {              /* enough remaining bits? */
            return 0;
        }
        mask   = self_mask(bit_n);
        *value = (it->byte_p[0] & mask);
        it->free_bit_n = 8; 
        ++(it->byte_p);
    }
    else if( bit_n < it->free_bit_n ) {
        if( it->byte_p == it->end ) {              /* enough remaining bits? */
            return 0;
        }

        left_bit = it->free_bit_n - bit_n;
        *value   = (it->byte_p[0] >> left_bit);

        mask   = self_mask(bit_n);
        *value &= mask;

        it->free_bit_n = left_bit;
    }
    else {
        if( it->byte_p >= it->end - 1 ) {          /* enough remaining bits? */
            return 0;
        }

        mask   = self_mask(it->free_bit_n);
        high = it->byte_p[0] & mask;

        ++(it->byte_p);
        mask = 0xFF ^ self_mask(8 - (bit_n - it->free_bit_n));
        low  = it->byte_p[0] & mask;

        *value  = high << (bit_n - it->free_bit_n);
        *value |= low >> (8 - (bit_n - it->free_bit_n));

        it->free_bit_n = (8 - (bit_n - it->free_bit_n));
    }
    return 1;
}

void
hwut_bitfield_print_numeric(const uint8_t* ConstArray, size_t ArraySize, const int Base, ...)
/* Considers the 'array' of size 'ArraySize'. Elements of this array are 
 * interpreted as numbers of base 'Base'. 
 * argument list must end with a '-1' to indicate the end of the 
 * elements to be printed. 
 *
 * This function is to be called in conjunction with the functions as in the
 * example below:
 *
 *    hwut_bitfield_print_numeric(frame, FrameSize, 16, 8, 8, 16, 32, -1);
 *    hwut_bitfield_print_borders(frame, FrameSize,     8, 8, 16, 32, -1);
 *    hwut_bitfield_print_bytes(frame, 8);
 *
 * So that the frames binary content appears aligned with the interpreted
 * numeric content.
 *
 * Variable argument list: list of bit_n defining the size of each element.   */
{
    const int        BitN   = ArraySize << 3;
    int              bit_n;
    uint32_t         value;
    int              offset = 0;
    va_list          argp;
    self_iterator_t  it;

    /* Currently, there is only one type of iterator taking a non-const array.
     * It is used for reading and writing. So, copy the constant to variable.*/
    uint8_t*         tmp_non_const_array = (uint8_t*)malloc(ArraySize);
    memcpy(tmp_non_const_array, ConstArray, ArraySize);

    self_iterator_init(&it, ArraySize, tmp_non_const_array);

    va_start(argp, Base);
    while( 1 + 1 == 2 )
    {
        /* Assert hits => missing terminating '-1' in argument list?         */
        assert( offset < BitN ); 

        bit_n = va_arg(argp, int);
        if( bit_n < 0 ) {
            break;
        }

        if( ! self_iterator_pop(&it, bit_n, &value) ) {
            /* Assert hits => missing terminating '-1' in argument list?     */
            free(tmp_non_const_array);
            assert(0);
            return;
        }

        self_print_value(&offset, bit_n, value, Base);
    }
    va_end(argp);
    printf("\n");

    free(tmp_non_const_array);
}

void
hwut_bitfield_print_borders(const uint8_t* array, size_t ArraySize, ...)
{
    int       i;
    int       bit_n;
    int       offset = 0;
    va_list   argp;

    va_start(argp, ArraySize);
    while( 1 + 1 == 2 )
    {
        bit_n = va_arg(argp, int);
        if( bit_n < 0 ) {
            break;
        }

        self_print_calculate_offset(&offset, &bit_n);

        printf("|");
        for(i=1; i < bit_n; i++) {
            printf(" ");
        }
    }
    va_end(argp);
    printf("\n");
}

void  
hwut_bitfield_print_bytes(const uint8_t* array, size_t ArraySize)
{
    uint8_t bit;
    int     i;

    for(i = 0; i < ArraySize; ++i)
    {
        for(bit = 0x80; bit; bit>>=1) {
            if( array[i] & bit ) printf("1");
            else                 printf("0");
        }
        printf(".");
    }
}

static void
self_print_value(int* offset, int bit_n, uint32_t value, int base)
{
    int         i = 0;
    uint32_t    tmp;
    const char* format_str =   (base == 8)  ? "%o"
                             : (base == 10) ? "%d"
                             : (base == 16) ? "%x"
                             :                "%x";

    self_print_calculate_offset(offset, &bit_n);

    /* Reduce offset by the amount of digits of the value.                   */
    for(tmp = value; tmp > (base-1); tmp /= base) {
        --bit_n;
    }

    printf(format_str, value);
    for(i=1; i < bit_n; i++) {
        printf(" ");
    }
}

static void
self_print_calculate_offset(int* offset, int* bit_n)
/* Calculates the offset with the decimal points in mind                     */
{
    *offset += *bit_n;
    if( *offset >> 3 ) {                                       /* offset / 8 */
        *bit_n += (*offset >> 3);      
        *offset = 0 + (*offset & 7);                           /* offset % 8 */
    }
}

