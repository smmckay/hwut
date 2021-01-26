#include <support/C/hwut_graph.h>
#include <assert.h>

void   
hwut_append_characters(char** iterator, size_t N, char C)
{
    size_t i = 0;
    for(i=0; i<N; ++i) { *((*iterator)++) = C; }
}

void   
hwut_append_underlined(char** iterator, const char* read_iterator, size_t Size)
{
    const char*     End = *iterator + Size;
    unsigned char   tmp = 0;
    while( *iterator != End ) {
        tmp = *(read_iterator++);
        if( tmp == ' ' ) tmp = '_';
        *((*iterator)++) = tmp;
    }
}

void   
hwut_append(char** iterator, const char* read_iterator, size_t Size)
{
    const char* End = *iterator + Size;
    while( *iterator != End ) *((*iterator)++) = *(read_iterator++);
}

void   
hwut_append_string(char** iterator, const char* read_iterator)
{
    while( *read_iterator ) *((*iterator)++) = *(read_iterator++);
}

void
hwut_append_binary(char** iterator, long Value, size_t BitN)
{
    char*  riterator = *iterator + BitN;

    if( BitN == 0 ) return;

    while( riterator != *iterator ) {
        --riterator;
        *riterator = (Value & 0x1) ? '1' : '0';
        Value = (Value >> 1);
    } 

    (*iterator) += BitN;
}

void
hwut_append_hex(char** iterator, long value, size_t DigitN)
{
    char*   riterator = *iterator + DigitN;
    long    digit     = 0;

    if( DigitN == 0 ) return;

    while( riterator != *iterator ) {
        --riterator;
        digit = value & 0xF;
        if( digit < 0xA ) *riterator = digit + '0';
        else              *riterator = digit - 0xA + 'A';
        value = (value >> 4);
    } 

    (*iterator) += DigitN;
}

void
hwut_append_decimal(char** iterator, long value, size_t DigitN)
{
    char*   riterator = *iterator + DigitN;
    long    digit     = 0;

    if( DigitN == 0 ) return;

    while( riterator != *iterator ) {
        --riterator;
        digit      = value % 10;
        *riterator = '0' + digit;
        value      = (value - digit) / 10;
    } 

    (*iterator) += DigitN;
}


long
OLD_hwut_get_bit_range(void* value_p, size_t BitBegin, size_t BitEnd)
{
    /* "X >> 3" means "integer division of X by 8" */
    void*   begin_byte_p   = value_p + (size_t)(BitBegin >> 3);
    void*   end_byte_p     = value_p + (size_t)(BitEnd >> 3);
    void*   byte_p         = 0x0;
    /* "X & 0x7" means "remainder of division of X by 8" */
    size_t  BeginBitOffset = BitBegin & 0x7; /* BitN where value starts in '*begin_byte_p' */ 
    size_t  EndBitOffset   = BitEnd   & 0x7; /* BitN where value ends in '*end_byte_p'     */ 

    long          result       = 0;
    unsigned char mask         = 0;
    unsigned char bit_position = 0;

    assert(BitEnd >= BitBegin);

    /* First Copy */
    byte_p       = begin_byte_p;
    bit_position = BeginBitOffset;
    result       = (*((unsigned char*)byte_p)) >> bit_position;

    if( byte_p == end_byte_p || (byte_p == (end_byte_p - 1) && EndBitOffset == 0) ) {
        /* Mask the Remainder:  '(1 << N) - 1' generates a mask of N times 1.
         *                      Examples: N=3 --> 0000.0111; N=5 --> 0001.1111  */
        mask   = (1 << (BitEnd - BitBegin)) - 1;
        result &= mask;
    }
    else { 
        bit_position += 8;

        /* Whole Byte Copies */
        while( byte_p != end_byte_p - 1 ) {
            ++byte_p;
            result |= ((long)(*(unsigned char*)byte_p)) << (bit_position - 8);
            bit_position += 8;
        }

        /* Last Copy */
        /* Mask the Remainder:  '(1 << N) - 1' generates a mask of N times 1.
         *                      Examples: N=3 --> 0000.0111; N=5 --> 0001.1111  */
        mask   = (1 << EndBitOffset) - 1;
        result |= (*((unsigned char*)end_byte_p) & mask) << (bit_position - 8);
    }
    return result;
}
long
hwut_get_bit_range(void* value_p, size_t ByteN, size_t Front, size_t Back)
    /*
     *   Byte0       Byte1       Byte2
     *  [0110.1010] [1110.0110] [0001.0010]
     *        |                    |
     *        Back                 Front
     *
     *        <---------------------------|
     *       bits count from right to left 
     *
     *  NOTE: The terminology 'front/back' implies that 'back'
     *        points to the last bit which is element of the 
     *        concerned range.                                    
     *                                                              */
{
    void*   last_byte_p        = value_p + ByteN - 1;
    /* NOTE: The 'Back' is located in the 'byte_range_front_p' and 
     *       'Front' is located in 'byte_range_back_p'. This is so, 
     *       since bytes are counted from right to left.            */
    /* "X >> 3" means "integer division of X by 8"                  */
    void*   byte_range_front_p = last_byte_p - (size_t)(Back >> 3);
    void*   byte_range_back_p  = last_byte_p - (size_t)(Front >> 3);
    void*   byte_p             = 0x0;
    /* "X & 0x7" means "remainder of division of X by 8"            */
    size_t  FrontBitOffset     = Front & 0x7; /* BitN where value starts in '*byte_range_back_p' */ 
    size_t  BackBitOffset      = Back  & 0x7; /* BitN where value ends in '*byte_range_front_p'  */ 

    long          result       = 0;
    unsigned char mask         = 0;

    assert(Back >= Front);

    /* First Copy */
    byte_p  = byte_range_front_p;
    /* Mask the Remainder:  '(1 << N) - 1' generates a mask of N times 1.
     *                      Examples: N=3 --> 0000.0111; N=5 --> 0001.1111  */
    mask    = (1 << (BackBitOffset+1)) - 1;
    result  = (*((unsigned char*)byte_p)) & mask;

    if( byte_p == byte_range_back_p ) {
        /* Mask the Remainder:  '(1 << N) - 1' generates a mask of N times 1.
         *                      Examples: N=3 --> 0000.0111; N=5 --> 0001.1111  */
        mask   = ((1 << FrontBitOffset) - 1) ^ 0xFF;
        result &= mask;
        result >>= FrontBitOffset;
    }
    else { 
        /* Whole Byte Copies */
        while( 1 + 1 == 2 ) {
            ++byte_p;
            if( byte_p == byte_range_back_p ) break;
            result <<= 8;
            result |= ((long)(*(unsigned char*)byte_p));
        }

        /* Last Copy */
        /* Mask the Remainder:  '(1 << N) - 1' generates a mask of N times 1.
         *                      Examples: N=3 --> 0000.0111; N=5 --> 0001.1111  */
        result = result << (8 - FrontBitOffset);
        mask   = ((1 << FrontBitOffset) - 1) ^ 0xFF;
        result |= ((*((unsigned char*)byte_range_back_p) & mask) >> FrontBitOffset);
    }
    return result;
}

