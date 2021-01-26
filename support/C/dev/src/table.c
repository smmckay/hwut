
#include <support/C/hwut_graph.h>
#include <support/C/hwut_scanner.h>
#include <stdio.h>
#include <assert.h>

static void 
Table_display(T_Data* alter_ego, T_Canvas* canvas, size_t X, size_t Y);

static void
Table_get_format_informations(T_Data* me, const char* Str);

static size_t
Table_get_max_cell_n(const char* Str);

void 
Table_construct(T_Data* me, const char* Title, const char* Str)
{
    Data_construct(me, Title, Str, Table_get_max_cell_n(Str), ':', Table_display);
    Table_get_format_informations(me, Str);
}

void
Table_print(const char* Title, const char* Str)
{
    Data_print(Table_construct, Title, Str);
}

static size_t
Table_get_max_cell_n(const char* Str)
{
    const char*   iterator   = 0x0;
    size_t        cell_n     = 0;
    size_t        max_cell_n = 0;

    cell_n = 1;
    for(iterator = Str; *iterator != '\0' ; ++iterator) {
        if     ( *iterator == ',' ) ++cell_n; 
        else if( *iterator == ';' ) cell_n = 1; 
        if( cell_n > max_cell_n )   max_cell_n = cell_n;
    }

    return max_cell_n;
}

static void
Table_parse(const char** entry_begin, const char** entry_end)
{
    *entry_begin = *entry_end;
    *entry_end   = hwut_find(';', *entry_begin);
}

static size_t
Table_parse_cell(const char** cell_begin, const char** cell_end, const char* entry_end)
{
    *cell_begin = *cell_end;
    *cell_end   = hwut_find_before(',', *cell_begin, entry_end);

    return *cell_end - *cell_begin;
}


static void
Table_get_format_informations(T_Data* me, const char* Str)
{
    const char*   entry_begin   = 0x0;
    const char*   entry_end     = 0x0;
    const char*   cell_begin    = 0x0;
    const char*   cell_end      = 0x0;
    size_t*       column_width_iterator = 0x0;
    size_t        length        = 0;

    /* Assume that the array me->column_width[] is initialized to zero. */

    /* Find max. cell size */
    me->y_size = 0;
    entry_end  = Str;
    while( *entry_end != '\0' ) {
        Table_parse(&entry_begin, &entry_end);
        if( *entry_begin == '\0' ) break;
        me->x_size = 0;
        cell_end              = entry_begin;
        column_width_iterator = me->column_width;
        while( cell_end != entry_end ) {
            length = Table_parse_cell(&cell_begin, &cell_end, entry_end);
            if( length > *column_width_iterator ) *column_width_iterator = length;
            me->x_size += *column_width_iterator;

            ++column_width_iterator;

            /* skip the ',' */
            if( *cell_end == ',' ) ++cell_end;
        }
        ++(me->y_size);

        /* skip the ';' */
        ++entry_end;
    }
    /* First column does not need a separator */
    me->x_size += (me->column_n - 1) * 3;

    if( me->x_size < me->title_length + 2 ) me->x_size = me->title_length + 2;

    me->column_seperator_whitespace_framed_f = 1;
}

static void 
Table_display(T_Data* me, T_Canvas* canvas, size_t X, size_t Y)
{
    const char*  entry_begin   = 0x0;
    const char*  entry_end     = 0x0;
    const char*  cell_begin    = 0x0;
    const char*  cell_end      = 0x0;
    char*        iterator      = 0x0;
    char*        row_iterator  = 0x0;
    char*        out_begin     = 0x0;
    size_t*      column_width_iterator = 0x0;
    size_t       Delta          = canvas->x_size;
    size_t       length         = 0;

    out_begin = canvas->surface + (Y * Delta) + X;

    Data_frame(me, canvas, X, Y);

    /* Draw the content */
    row_iterator = out_begin + Delta;
    entry_end    = me->description_str;
    while( *entry_end != '\0' ) {
        Table_parse(&entry_begin, &entry_end);
        if( *entry_begin == '\0' ) break;

        iterator              = row_iterator + 2;
        cell_end              = entry_begin;
        column_width_iterator = me->column_width;
        while( cell_begin != cell_end ) {
            length = Table_parse_cell(&cell_begin, &cell_end, entry_end);

            hwut_memcpy(iterator, (void*)cell_begin, length * sizeof(char));
            iterator += *column_width_iterator + 3;
            ++column_width_iterator;

            /* skip the ',' */
            if( *cell_end == ',' ) ++cell_end;
        }
        row_iterator += Delta;

        /* skip the ';' */
        ++entry_end;
    }

    /* Underline the first line */
    for(iterator=out_begin + Delta + 1; iterator != out_begin + Delta + me->x_size + 3; ++iterator) {
        if( *iterator == ' ' ) *iterator = '_';
    }
}

