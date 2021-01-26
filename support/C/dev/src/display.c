#include <support/C/hwut_graph.h>
#include <support/C/hwut_scanner.h>
#include <malloc.h>
#include <assert.h>

void
Data_construct(T_Data*  me, 
               const char*            Title, 
               const char*            DescriptionStr, 
               size_t                 ColumnN,
               const char             ColumnSeparator, 
               HWUT_DISPLAY_FUNCTION  display_function)
{
    size_t*  iterator = 0x0;

    me->title            = Title;
    me->title_length     = hwut_strlen(Title);
    me->description_str  = DescriptionStr;
    me->column_n         = ColumnN;
    me->column_width     = (size_t*)malloc(ColumnN*sizeof(size_t));
    for(iterator = me->column_width; iterator != me->column_width + ColumnN; ++iterator) 
        *iterator = 0;
    me->column_separator = ColumnSeparator;
    me->column_seperator_whitespace_framed_f = 1;

    me->y_size           = 2;
    me->x_size           = 0;

    me->display          = display_function;
}

void
Data_destruct(T_Data* me)
{
    me->title            = 0x0;
    me->description_str  = 0x0;
    me->column_n         = 0;
    free(me->column_width);
    me->column_width     = 0x0;
    me->column_separator = '\0';
    me->y_size           = 0;
    me->x_size           = 0;

    me->display          = 0x0;
}

void 
Data_make_header(char** iterator, const char* Title, size_t XSize)
{
    const char*  title_iterator = Title;
    const char*  start          = *iterator;

    hwut_append_string(iterator, " _(");

    while( *title_iterator != '\0' ) {
        *((*iterator)++) = *title_iterator++;
    }
    *((*iterator)++) = ')';
    /* Note: it follows from above:        *iterator - start > 2
     *       it follows from constraints:  XSize > 6               */
    assert(XSize > (*iterator - start) - 2);
    hwut_append_characters(iterator, XSize - (*iterator - start) - 2, '_');
    *((*iterator)++) = '_';
    *((*iterator)++) = ' ';
}

void   
Data_make_footer(T_Data* me, char** iterator, size_t TotalWidth)
{
    size_t*  column_iterator  = 0x0;
    size_t*  column_width_end = me->column_width + me->column_n;
    char*    start            = 0x0;

    if( me->column_n == 0 ) {
        hwut_append_string(iterator, "'--'");
        return;
    }
    start = *iterator;
    *(*iterator)++ = '\'';
    *(*iterator)++ = '-';
    for(column_iterator = me->column_width; column_iterator != column_width_end - 1; 
        ++column_iterator) {

        /* Add 2 for the framing ' ' around the cell content. */
        if( me->column_seperator_whitespace_framed_f ) { 
            hwut_append_characters(iterator, *column_iterator + 1, '-');
            *(*iterator)++ = '^';
            *(*iterator)++ = '-';
        }
        /* Add 1 for separator    */
        else { 
            hwut_append_characters(iterator, *column_iterator, '-');
            *(*iterator)++ = '^';
        }

    }
    if( (size_t)(*iterator - start) < TotalWidth ) {
        hwut_append_characters(iterator, TotalWidth - (size_t)(*iterator - start) - 1, '-');
    }
    *(*iterator)++ = '\'';
}

void
Data_frame(T_Data* me, T_Canvas* canvas, size_t X, size_t Y)
{
    size_t  Delta    = canvas->x_size; 
    size_t  YSize    = me->y_size + 2;              
    size_t  x_size   = me->x_size + 4;                /* framing '| ' and ' |' */
    char*   Begin    = canvas->surface + Y * Delta + X;
    char*   End      = Begin           + (YSize) * Delta;
    char*   iterator = Begin;
    char*   cell_iterator = 0x0;
    size_t* colum_width_iterator = 0x0;
    size_t  separator_space = me->column_seperator_whitespace_framed_f ? 3 : 1;

    assert(me->title_length <= x_size - 2);

    Data_make_header(&iterator, me->title, x_size);

    for(iterator = Begin + Delta; iterator != End - Delta; iterator += Delta) {
        *iterator = '|';
        if( me->column_n > 1 ) {
            cell_iterator = iterator;
            for(colum_width_iterator = me->column_width; 
                colum_width_iterator != me->column_width + me->column_n - 1; 
                ++colum_width_iterator) {
                cell_iterator += *colum_width_iterator + separator_space;
                *cell_iterator = me->column_separator;
            }
        }
        *(iterator + x_size - 1)= '|';
    }
    
    Data_make_footer(me, &iterator, x_size);
}

T_Data   data;

void  
Data_print(void  (*construct)(T_Data*, const char*, const char*), 
           const char* Title, const char* Str)
{
    construct(&data, Title, Str);
    Canvas_simple_print(&data);
}

