#include <support/C/hwut_graph.h>
#include <support/C/hwut_scanner.h>
#include <stdio.h>
#include <assert.h>


static void 
Object_display(T_Data* me, T_Canvas* canvas, size_t X, size_t Y);

static void
Object_parse(const char** entry_begin, const char** entry_end);

void 
Object_construct(T_Data* me, const char* Title, const char* Str)
{
    /* Determines sizes of columns */
    const char*    entry_begin   = 0x0;
    const char*    entry_end     = 0x0;
    const char*    separator_p   = 0x0;
    size_t   name_length      = 0;
    size_t   name_length_max  = 0;
    size_t   value_length     = 0;
    size_t   value_length_max = 0;
    size_t   x_size_max       = 0;
    size_t   y_size           = 0;

    /* Find max. cell size */
    y_size = 0;
    entry_end  = Str;
    while( *entry_end != '\0' ) {
        Object_parse(&entry_begin, &entry_end);
        if( *entry_begin == '\0' ) break;

        separator_p = hwut_find_before('=', entry_begin, entry_end);

        if( separator_p != entry_end ) {
            value_length = entry_end - (separator_p + 1); /* Skip the '=' sign */
            if( value_length > value_length_max ) value_length_max = value_length;
            name_length = separator_p - entry_begin;
            if( name_length > name_length_max ) name_length_max = name_length;
        } else {
            if( x_size_max < entry_end - entry_begin ) 
                x_size_max = entry_end - entry_begin;
        }
        ++(y_size);

        /* skip the ';' */
        ++entry_end;
    }
    /* First column does not need a separator */
    if( x_size_max < name_length_max + value_length_max )
        x_size_max = name_length_max + value_length_max;

    if( value_length_max != 0 ) x_size_max += 3; 

    Data_construct(me, Title, Str, (value_length_max != 0) ? 2 : 1, '=', Object_display);

    me->column_seperator_whitespace_framed_f = 1;
    me->column_width[0] = name_length_max;
    if( value_length_max != 0 ) me->column_width[1] = value_length_max;

    me->x_size = x_size_max;
    if( me->x_size < me->title_length + 2 ) me->x_size = me->title_length + 2;

    me->y_size = y_size;
}

void
Object_print(const char* Title, const char* Str)
{
    Data_print(Object_construct, Title, Str);
}

static void 
Object_display(T_Data* me, T_Canvas* canvas, size_t X, size_t Y)
{
    const char*    entry_begin   = 0x0;
    const char*    entry_end     = 0x0;
    const char*    separator_p   = 0x0;
    char*    iterator      = 0x0;
    char*    row_iterator  = 0x0;
    char*    out_begin     = 0x0;
    size_t   Delta         = canvas->x_size;
    size_t   value_length  = 0;

    out_begin = canvas->surface + (Y * Delta) + X;

    Data_frame(me, canvas, X, Y);

    row_iterator = out_begin + Delta;
    entry_end    = me->description_str;
    while( *entry_end != '\0' ) {
        Object_parse(&entry_begin, &entry_end);
        if( *entry_begin == '\0' ) break;

        separator_p = hwut_find_before('=', entry_begin, entry_end);

        iterator = row_iterator + 2;
        hwut_memcpy(iterator, (void*)entry_begin, (separator_p - entry_begin) * sizeof(char));

        if( separator_p != entry_end ) {
            value_length = entry_end - (separator_p + 1); /* Skip the '=' sign */

            iterator = row_iterator + me->column_width[0] + 2 + 3;
            hwut_memcpy(iterator, (void*)(separator_p + 1), value_length * sizeof(char));
        } 
        row_iterator += Delta;

        /* skip the ';' */
        ++entry_end;
    }
}

static void
Object_parse(const char** entry_begin, const char** entry_end)
{
    *entry_begin = *entry_end;
    *entry_end   = hwut_find(';', *entry_begin);
}


