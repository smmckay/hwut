
#include <support/C/hwut_graph.h>
#include <support/C/hwut_scanner.h>
#include <stdio.h>
#include <assert.h>

static void 
BitField_display(T_Data* me, T_Canvas* canvas, size_t X, size_t Y);

static void 
BitField_parse_entry(const char** entry_begin, const char** entry_end, 
                     const char** name_begin, const char** name_end, 
                     size_t* bit_n);

void 
BitField_construct(T_BitField* me, const char* Title, void* ValueP, size_t ByteN, const char* Str)
{
    const char*   entry_begin = 0x0;
    const char*   entry_end   = 0x0;
    const char*   name_begin  = 0;
    const char*   name_end    = 0x0;
    size_t        center_of_bit_range = 0x0;
    size_t        bit_n       = 0;
    size_t*       column_width_iterator = 0x0;
    size_t        extend      = 0;
    size_t        total_bit_n = 0;
    size_t        range_n     = 0;
    size_t        x_offset    = 0;

    me->base.title        = Title;
    me->base.title_length = hwut_strlen(Title);
    me->value_p           = ValueP;
    me->value_byte_n      = ByteN;

    total_bit_n = 0; 
    range_n     = 0;

    entry_end   = Str;
    entry_begin = 0x0;
    while( *entry_end != '\0' ) {
        /* Input: Scan description string until delimiter. */
        BitField_parse_entry(&entry_begin, &entry_end, &name_begin, &name_end, &bit_n);
        total_bit_n += bit_n;
        ++range_n;
        ++entry_end; /* skip ';' */
    } 

    Data_construct(&me->base, Title, Str, range_n, ' ', BitField_display);
    me->base.column_seperator_whitespace_framed_f = 0;
    me->base.y_size = range_n + 2;
    if( range_n ) me->base.x_size = total_bit_n + 1 * (range_n - 1);  /* Each separator '.' */
    else          me->base.x_size = 0;

    x_offset     = 2;
    column_width_iterator = me->base.column_width;
    entry_end    = Str;
    entry_begin  = 0x0;
    while( *entry_end != '\0' ) {
        /* Input: Scan description string until delimiter. */
        BitField_parse_entry(&entry_begin, &entry_end, &name_begin, &name_end, &bit_n);

        center_of_bit_range = x_offset + (bit_n >> 1);
        extend              = center_of_bit_range + 1 + (name_end - name_begin);
        if( extend > me->base.x_size ) me->base.x_size = extend;

        *column_width_iterator++  = bit_n;
        x_offset                 += bit_n + 1; /* Add 1 for separator */
        ++entry_end; /* skip ';' */
    } 
    if( me->base.x_size < me->base.title_length + 2 ) me->base.x_size = me->base.title_length + 2;
}

void 
BitField_print(const char* Title, void* ValueP, size_t ByteN, const char* Str)
{
    T_BitField  data;

    BitField_construct(&data, Title, ValueP, ByteN, Str);
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
    *name_begin  = hwut_find_before(' ', *entry_begin, *entry_end);
    if( *name_begin != *entry_end ) ++(*name_begin);

    *name_end = *entry_end;
    hwut_skip_whitespace(name_begin);
    hwut_skip_whitespace_backwards(name_end, *name_begin);
}

static void 
BitField_display(T_Data* alter_ego, T_Canvas* canvas, size_t X, size_t Y)
{
    T_BitField* me = (T_BitField*)alter_ego;
    const char*    entry_begin    = 0x0;
    const char*    entry_end      = 0x0;
    const char*    name_begin     = 0x0;
    const char*    name_end       = 0x0;
    char*    out_begin      = 0x0;
    char*    bit_iterator   = 0x0;
    char*    row_iterator   = 0x0;
    size_t   Delta          = canvas->x_size;
    size_t   YSize          = me->base.y_size + 1;
    size_t   bit_i          = 0;
    size_t   bit_n          = 0;
    size_t   line_n         = 0;
    long     value          = 0;
    size_t   center_of_bit_range = 0x0;
    size_t   x_offset       = 0;

    Data_frame(&me->base, canvas, X, Y);

    out_begin = canvas->surface + (Y * Delta) + X;

    line_n    = 0;
    bit_i     = (me->value_byte_n * 8) - 1;
    x_offset  = 2;
    entry_end    = me->base.description_str;
    row_iterator = out_begin + Delta;
    bit_iterator = out_begin + Delta * (YSize - 1) + 2;
    while( *entry_end != '\0' ) {
        /* Input: Scan description string until delimiter. */
        BitField_parse_entry(&entry_begin, &entry_end, &name_begin, &name_end, &bit_n);

        if( bit_n < 1 ) {
            hwut_error("User provided bit structure exceeds value array limits.");
        }

        /* center of current bit range: */
        center_of_bit_range = x_offset + (bit_n >> 1);

        value = hwut_get_bit_range(me->value_p, me->value_byte_n, bit_i - bit_n + 1, bit_i);

        Canvas_draw_labeled_value(canvas, 
                                  row_iterator + center_of_bit_range, 
                                  name_begin, name_end, 
                                  value);


        Canvas_draw_vertical_line(canvas, 
                                  row_iterator + center_of_bit_range, 
                                  me->base.y_size - 1 - line_n);
        bit_i -= bit_n;
        ++line_n;
        row_iterator += Delta;

        hwut_append_binary(&bit_iterator, value, bit_n);
        ++bit_iterator;  /* skip the separator */

        x_offset += bit_n + 1;
        ++entry_end; /* skip ';' */
    }
}


