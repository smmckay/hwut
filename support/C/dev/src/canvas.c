#include <support/C/hwut_graph.h>
#include <support/C/hwut_scanner.h>

#include <malloc.h>
#include <assert.h>

static void
__Canvas_display_core(char* Begin, char* End, size_t XSize);

void
Canvas_construct(T_Canvas* me, size_t XSize, size_t YSize)
{
    size_t surface_size = 0;
    char*  iterator     = 0x0;

    me->x_size   = XSize; 
    me->y_size   = YSize;
    surface_size = (size_t)((me->x_size)*(me->y_size));
    me->surface  = (char*)malloc(surface_size);
    for(iterator = me->surface; iterator != me->surface + surface_size; ++iterator) 
        *iterator = ' ';
}

void
Canvas_destruct(T_Canvas* me)
{
    size_t surface_size = 0;

    me->x_size   = 0; 
    me->y_size   = 0;
    surface_size = 0;
    free(me->surface);
}


#include <stdio.h>
void
Canvas_display(T_Canvas* me)
{
    __Canvas_display_core(me->surface, 
                          me->surface + (me->x_size) * (me->y_size),
                          me->x_size);
}

void 
Canvas_display_minimal(T_Canvas* me)
{
    /* Find first and last non-empty line */
    char* line_begin = me->surface;
    char* line_end   = 0x0;
    char* iterator   = 0x0;
    char* begin      = me->surface;
    char* end        = me->surface + (me->x_size) * (me->y_size);
    int   found_f    = 0;

    found_f = 0;
    for(line_begin = me->surface; line_begin != end; line_begin = line_end) {
        line_end   = line_begin + me->x_size;
        for(iterator = line_begin; iterator != line_end; ++iterator) {
            if( *iterator != ' ' ) { found_f = 1; break; }
        }
        if( found_f ) break;
    }
    begin = line_begin;

    found_f = 0;
    for(line_end = end; line_end != begin; line_end = line_begin) {
        line_begin   = line_end - me->x_size;
        for(iterator = line_begin; iterator != line_end; ++iterator) { 
            if( *iterator != ' ' ) { found_f = 1; break; }
        }
        if( found_f ) break;
    }
    end = line_end;

    __Canvas_display_core(begin, end, me->x_size);
}

static void
__Canvas_display_core(char* Begin, char* End, size_t XSize)
{
    char* line_begin = 0x0;
    char* line_end   = 0x0;
    char* iterator   = 0x0;

    /* Size of memory chunk is a multiple of XSize. */
    assert((End - Begin) % XSize == 0);

    for(line_begin = Begin; line_begin != End; line_begin = line_end) {
        line_end   = line_begin + XSize;
        for(iterator = line_begin; iterator != line_end; ++iterator) 
            fputc(*iterator, stdout);
        // fputc('$', stdout);
        fputc('\n', stdout);
    }
}

void 
Canvas_simple_print(T_Data* data)
{
    T_Canvas    canvas;

    Canvas_construct(&canvas, data->x_size + 4, data->y_size + 2);
    data->display(data, &canvas, 0, 0);
    Canvas_display(&canvas);
    Canvas_destruct(&canvas);
}

void
Canvas_draw_vertical_line(T_Canvas* me, char* StartP, size_t N)
{
    int   i = 0;
    char* iterator = StartP;
    for(i = 0; i < N; ++i) {
        iterator += me->x_size;
        *iterator = ':';
    }
}

void
Canvas_draw_labeled_value(T_Canvas* me, char* StartP, const char* NameBegin, const char* NameEnd, long Value)
{
    char*  iterator = StartP;
    int    digit_n = 0;
    long   tmp     = 1;

    /* Draw the name label */
    *iterator++ = ',';
    hwut_append(&iterator, NameBegin, NameEnd - NameBegin);
    *iterator++ = ':';

    if( Value == 0 ) { 
        *iterator++ = '0';
        return;
    }
    /* Determine DigitN */
    while( tmp <= Value ) { 
        tmp <<= 4; 
        ++digit_n; 
    }

    /* Draw the hex value */
    hwut_append_hex(&iterator, Value, digit_n);
}


