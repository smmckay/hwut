#include "hwut_graph.h"
#include "hwut_scanner.h"
#include <stdio.h>
#include <assert.h>

static void 
BitFieldList_display(T_Data* me, T_Canvas* canvas, size_t X, size_t Y);

static void 
BitField_parse_entry(const char** entry_begin, const char** entry_end, 
                     const char** name_begin, const char** name_end, 
                     size_t* bit_n);

void 
BitFieldList_construct(T_BitField* me, const char* Title, void* ValueP, size_t ByteN, const char* Str)
{
    const char*   entry_begin   = 0x0;
    const char*   entry_end     = 0x0;
    const char*   name_begin    = 0;
    const char*   name_end      = 0x0;
    size_t        bit_n         = 0;
    size_t        line_n        = 0;
    size_t        name_length   = 0;
    size_t        number_length = 0;

    Data_construct(&me->base, Title, Str, 3, ':', BitFieldList_display);

    me->value_p           = ValueP;
    me->value_byte_n      = ByteN;

    line_n         = 0;

    entry_end   = Str;
    entry_begin = 0x0;
    /* me->base.column_width[i] == 0 by constructor */
    while( *entry_end != '\0' ) {
        /* Input: Scan description string until delimiter. */
        BitField_parse_entry(&entry_begin, &entry_end, &name_begin, &name_end, &bit_n);

        name_length = name_end - name_begin;
        /* Number of hex digits required to represent N bits: N / 4. Since only integer
         * number of digits are possible use the formulat below.                        */
        number_length = (int)((bit_n + 3) / 4);

        if( name_length   > me->base.column_width[0] ) me->base.column_width[0] = name_length;
        if( bit_n         > me->base.column_width[1] ) me->base.column_width[1] = bit_n;
        if( number_length > me->base.column_width[2] ) me->base.column_width[2] = number_length;

        ++line_n;
        ++entry_end; /* skip ';' */
    } 
    me->base.column_seperator_whitespace_framed_f = 1;
    me->base.y_size = line_n;
    me->base.x_size =   me->base.column_width[0] + 3 
                      + me->base.column_width[1] + 3 
                      + me->base.column_width[2];
}

void 
BitFieldList_print(const char* Title, void* ValueP, size_t ByteN, const char* Str)
{
    T_BitField  data;

    BitFieldList_construct(&data, Title, ValueP, ByteN, Str);
    Canvas_simple_print(&data.base);
}

static void 
BitField_parse_entry(const char** entry_begin, const char** entry_end, 
                     const char** name_begin, const char** name_end, 
                     size_t* bit_n)
{
    *entry_begin = *entry_end;
    *entry_end   = hwut_find(';', *entry_begin);
    *bit_n       = hwut_scan_integer(entry_begin);
    *name_begin  = hwut_find_before(',', *entry_begin, *entry_end);
    if( *name_begin != *entry_end ) ++(*name_begin);

    *name_end = *entry_end;
    hwut_skip_whitespace(name_begin);
    hwut_skip_whitespace_backwards(name_end, *name_begin);
}

static void 
BitFieldList_display(T_Data* alter_ego, T_Canvas* canvas, size_t X, size_t Y)
{
    T_BitField*    me = (T_BitField*)alter_ego;
    const char*    entry_begin    = 0x0;
    const char*    entry_end      = 0x0;
    const char*    name_begin     = 0x0;
    const char*    name_end       = 0x0;
    char*          row_iterator   = 0x0;
    char*          iterator       = 0x0;
    size_t         Delta          = canvas->x_size;
    size_t         number_length  = 0;
    size_t         bit_i          = 0;
    size_t         bit_n          = 0;
    long           value          = 0;

    Data_frame(&me->base, canvas, X, Y);

    bit_i     = (me->value_byte_n * 8) - 1;

    row_iterator = canvas->surface + ((Y + 1) * canvas->x_size) + X;
    entry_end    = me->base.description_str;
    while( *entry_end != '\0' ) {
        /* Input: Scan description string until delimiter. */
        BitField_parse_entry(&entry_begin, &entry_end, &name_begin, &name_end, &bit_n);
        if( *entry_begin == '\0' ) break;

        if( bit_n < 1 ) {
            hwut_error("User provided bit structure exceeds value array limits.");
        }

        value = hwut_get_bit_range(me->value_p, me->value_byte_n, bit_i - bit_n + 1, bit_i);

        iterator = row_iterator + 2;
        hwut_memcpy(iterator, (void*)name_begin, (name_end - name_begin) * sizeof(char));

        iterator = row_iterator + 2 + me->base.column_width[0] + 3;
        hwut_append_binary(&iterator, value, bit_n);

        number_length = (size_t)((int)((bit_n + 3)/4));

        iterator = row_iterator + 2 + me->base.column_width[0] + 3 + me->base.column_width[1] + 3 
                   + (me->base.column_width[2] - number_length);
        hwut_append_hex(&iterator, value, number_length);

        row_iterator += Delta;
        bit_i -= bit_n;

        /* skip the ';' */
        ++entry_end;
    }
}


