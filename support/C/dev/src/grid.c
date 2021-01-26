
#include <support/C/hwut_graph.h>
#include <support/C/hwut_scanner.h>
#include <stdio.h>
#include <assert.h>

static void 
Grid_display(T_Data* me, T_Canvas* canvas, size_t X, size_t Y);

static size_t 
Grid_parse(const char** entry_begin, const char** entry_end);

void
Grid_construct(T_Data* me, size_t MaxLineWidth, const char* Title, const char* Str)
    /* Determines the widths of each column, assumed that the 
     * entries in 'Str' are aligned on a grid.                          */
{
    const char*   entry_begin    = Str;
    const char*   entry_end      = 0x0;
    size_t  entry_length   =  0;
    /* If one cell is larger then the MaxLineWidth, it must be adapted. */
    size_t  min_cell_width = -1;
    size_t  min_line_width =  1;
    size_t  max_line_width =  0;
    size_t  line_width     =  0;
    size_t* column_width_iterator = 0x0;
    size_t* column_width_end      = 0x0;
    size_t  column_i       = 0;
    size_t  column_n       = 0;
    size_t  max_column_n   = 0;

    /* Determine:  min. line width, which is equal to the largest required cell.
     *                              In this case, there is only one cell per line.
     *
     *             max. column number, which is equal to the max. line width
     *                                 divided by the min. cell number.                */
    entry_end      = Str;
    min_line_width = 0;
    min_cell_width = HWUT_MAX_VALUE_SIZE_T;
    while( *entry_end != '\0' ) {
        entry_length = Grid_parse(&entry_begin, &entry_end);

        if( entry_length > min_line_width )                      { min_line_width = entry_length; }
        if( entry_length < min_cell_width && entry_length != 0 ) { min_cell_width = entry_length; }

        ++entry_end; /* skip ';' */
    } 
    max_line_width = (min_line_width > MaxLineWidth ) ? min_line_width : MaxLineWidth;
    max_column_n   = max_line_width / min_cell_width; 

    Data_construct(me, Title, Str, max_column_n, ' ', Grid_display);
    /* me->column_n == max_column_n */

    column_i   = 0;
    line_width = 0;
    me->y_size = 1;

    entry_end             = Str;
    column_width_iterator = me->column_width;
    column_width_end      = me->column_width + me->column_n;
    column_n              = me->column_n + 1; /* set '+1' to indicate 'undetermined' */

    while( *entry_end!= '\0' ) {
        entry_length = Grid_parse(&entry_begin, &entry_end);

        if( entry_length < *column_width_iterator ) entry_length = *column_width_iterator;
    
        if( line_width + entry_length <= max_line_width ) {
            /* (1) Cell fits line ________________________________________________________*/
            if( column_i == column_n ) {
                /* End of line reached => Newline, Back to first column */
                ++(me->y_size);
                column_i              = 0;
                line_width            = 0;
                column_width_iterator = me->column_width;
            }
            if( entry_length > *column_width_iterator ) *column_width_iterator = entry_length;
            line_width += *column_width_iterator;

            ++entry_end;             /* Skip ';' */
            ++column_width_iterator;
            ++column_i;
        }
        else { 
            /* (2) Cell does not fit line => Newline _________________________________*/
            /*       (line_width + *column_width_iterator > max_line_width)           */

            /* The number of possible columns per row must be adapted. We can now
             * only carry 'column_i' columns instead of 'column_n'.                   */
            if( column_i < column_n ) { 
                /* If this is not the initial setting of column_n, then
                 * unfortunately, we must start all over again.                       */
                if( column_n != me->column_n + 1 ) {
                    /* Start all over again                                           */
                    me->y_size = 1;
                    for(column_width_iterator = me->column_width; 
                        column_width_iterator != column_width_end; 
                        ++column_width_iterator) {
                        *column_width_iterator = 0;
                    }
                    entry_end = Str;
                } else { 
                    /* Treat the same entry again, now, for the next line.            */
                    entry_end = entry_begin;
                }
                column_n = column_i;
            } else { 
                /* Treat the same entry again, now, for the next line.                */
                entry_end = entry_begin;
            }
            /* End of line reached => Newline, Back to first column                   */
            ++(me->y_size);
            column_i              = 0;
            line_width            = 0;
            column_width_iterator = me->column_width;
        } 
    } 

    if( column_n == me->column_n + 1 ) me->column_n = column_i;
    else                               me->column_n = column_n;

    me->x_size = 0;
    for(column_width_iterator = me->column_width; 
        column_width_iterator != column_width_end; 
        ++column_width_iterator) {
        me->x_size += *column_width_iterator;
    }
    me->x_size += 3 * (me->column_n - 1); /* separators ' | ' */

    if( me->x_size < me->title_length + 2 ) me->x_size = me->title_length + 2;

    /* Last line number increment was done right before the end. */
    if( column_i == column_n ) --(me->y_size);
}

void
Grid_print(size_t MaxLineWidth, const char* Title, const char* Str)
{
    T_Data  data;

    Grid_construct(&data, MaxLineWidth, Title, Str);
    Canvas_simple_print(&data);
}

static size_t 
Grid_parse(const char** entry_begin, const char** entry_end)
{
    *entry_begin = *entry_end;
    *entry_end   = hwut_find(';', *entry_begin);
    return *entry_end - *entry_begin;
}

static void 
Grid_display(T_Data* me, T_Canvas* canvas, size_t X, size_t Y)
{
    const char*    entry_begin    = 0x0;
    const char*    entry_end      = 0x0;
    size_t   entry_length   = 0;
    char*    out_iterator   = 0x0;
    char*    out_begin      = 0x0;
    char*    out_row_offset = 0x0;
    char*    out_end        = 0x0;
    size_t   column_i       = 0;
    size_t   max_column_i   = 0;
    size_t*  column_width_iterator = 0x0;
    size_t   Delta          = canvas->x_size;
    size_t   YSize          = me->y_size + 2;

    Data_frame(me, canvas, X, Y);

    out_begin = canvas->surface + (Y * Delta) + X;
    out_end   = out_begin       + YSize * Delta; 

    out_row_offset        = out_begin + Delta + 2;     /* + 2 = skip '| '        */
    column_width_iterator = me->column_width;
    column_i              = 0;
    max_column_i          = me->column_n - 1;

    entry_begin  = 0x0;
    entry_end    = me->description_str;
    out_iterator = out_row_offset;
    while( *entry_end != '\0' ) {
        /* Input: Scan description string until delimiter. */
        entry_length = Grid_parse(&entry_begin, &entry_end);

        /* Output: Display content, adapt iterators. */
        hwut_append(&out_iterator, entry_begin, entry_length);
        hwut_append_characters(&out_iterator, *column_width_iterator - entry_length, ' ');

        if( column_i != max_column_i ) {
            ++column_i;
            ++column_width_iterator;
            out_iterator += 3;     /* Skip the cell separator + whitespace */
        } else { 
            column_i               = 0;
            column_width_iterator  = me->column_width;
            out_row_offset        += Delta;
            out_iterator           = out_row_offset;
        }
        
        ++entry_end; /* Skip the semi-colon */
    }
}


