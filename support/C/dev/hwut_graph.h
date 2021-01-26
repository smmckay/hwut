#ifndef __HWUT_INCLUDE_GUARD__SUPPORT_HWUT_GRAPH_H
#define __HWUT_INCLUDE_GUARD__SUPPORT_HWUT_GRAPH_H

#include <stddef.h>

#define HWUT_MAX_VALUE_SIZE_T   (65536)

struct T_Data_tag;
struct T_Canvas_tag;

typedef void (*HWUT_DISPLAY_FUNCTION)(struct T_Data_tag*, struct T_Canvas_tag*, size_t, size_t);

typedef struct T_Data_tag {
    const char*   title;
    size_t        title_length;
    const char*   description_str;

    size_t*   column_width;
    size_t    column_n;
    char      column_separator;
    char      column_seperator_whitespace_framed_f;

    size_t    x_size;
    size_t    y_size;

    HWUT_DISPLAY_FUNCTION   display;
} T_Data;

extern void  Data_frame(T_Data* me, struct T_Canvas_tag* canvas, size_t X, size_t Y);
extern void  Data_construct(T_Data*                 me, 
                            const char*             Title,   
                            const char*             DescriptionStr, 
                            size_t                  ColumnN,
                            const char              ColumnSeparator,
                            HWUT_DISPLAY_FUNCTION   display);
extern void  Data_print(void  (*construct)(T_Data*, const char*, const char*), 
                        const char* Title, const char* Str);

extern void  Table_construct(T_Data* me, const char* Title, const char* Str);
extern void  Table_print(const char* Title, const char* Str);

extern void  Grid_construct(T_Data* me, size_t MaxLineWidth, const char* Title, const char* Str);
extern void  Grid_print(size_t MaxLineWidth, const char* Title, const char* Str);

extern void  Object_construct(T_Data* me, const char* Title, const char* Str);
extern void  Object_print(const char* Title, const char* Str);

typedef struct { 
    T_Data    base;

    void*     value_p;
    size_t    value_byte_n;
} T_BitField;

extern void  BitField_construct(T_BitField* me, const char* Title, void* ValueP, size_t ByteN, const char* Str);
extern void  BitField_print(const char* Title, void* ValueP, size_t ByteN, const char* Str);

extern void  BitFieldList_construct(T_BitField* me, const char* Title, void* ValueP, size_t ByteN, const char* Str);
extern void  BitFieldList_print(const char* Title, void* ValueP, size_t ByteN, const char* Str);

typedef struct T_Canvas_tag {
    char*     surface;

    size_t    x_size;
    size_t    y_size;
} T_Canvas;

extern void Canvas_construct(T_Canvas* me, size_t XSize, size_t YSize);
extern void Canvas_destruct(T_Canvas* me);

extern void Canvas_display(T_Canvas* me);
extern void Canvas_display_minimal(T_Canvas*);

extern void Canvas_draw_vertical_line(T_Canvas* me, char* StartP, size_t N);
extern void Canvas_draw_labeled_value(T_Canvas* me, char* StartP, 
                                      const char* NameBegin, const char* NameEnd, 
                                      long Value);
extern void Canvas_simple_print(T_Data*);

#endif /* __HWUT_INCLUDE_GUARD__SUPPORT_HWUT_GRAPH_H */
