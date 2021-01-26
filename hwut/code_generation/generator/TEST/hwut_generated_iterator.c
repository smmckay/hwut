#include "hwut_generated_iterator.h"

extern void   myGen4_0_init(myGen4_t* it);
extern int    myGen4_0_implement(myGen4_t* it);
extern int    myGen4_0_is_admissible(myGen4_t* it);
extern void   myGen4_1_init(myGen4_t* it);
extern int    myGen4_1_implement(myGen4_t* it);
extern int    myGen4_1_is_admissible(myGen4_t* it);
extern void   myGen4_2_init(myGen4_t* it);
extern int    myGen4_2_implement(myGen4_t* it);
extern int    myGen4_2_is_admissible(myGen4_t* it);
extern void   myGen4_3_init(myGen4_t* it);
extern int    myGen4_3_implement(myGen4_t* it);
extern int    myGen4_3_is_admissible(myGen4_t* it);
extern void   myGen4_4_init(myGen4_t* it);
extern int    myGen4_4_implement(myGen4_t* it);
extern int    myGen4_4_is_admissible(myGen4_t* it);


static const myGen4_section_t  myGen4_section_array[5] = { 
    { 0, myGen4_0_init, myGen4_0_implement, myGen4_0_is_admissible },
    { 3, myGen4_1_init, myGen4_1_implement, myGen4_1_is_admissible },
    { 10, myGen4_2_init, myGen4_2_implement, myGen4_2_is_admissible },
    { 11, myGen4_3_init, myGen4_3_implement, myGen4_3_is_admissible },
    { 19, myGen4_4_init, myGen4_4_implement, myGen4_4_is_admissible },
 
};
static const myGen4_section_t* myGen4_section_array_begin = &myGen4_section_array[0];
static const myGen4_section_t* myGen4_section_array_end   = &myGen4_section_array[5];



void
myGen4_init(myGen4_t* it)
/* Use provided memory to construct an object of type myGen4_t.
 *                                                                           */
{
    it->hwut.print   = myGen4_print;
    it->hwut.section = (void*)0;
}

static int
myGen4_intern_next(myGen4_t* it)
{
    if( it->hwut.section == (void*)0 ) {
        /* The very first 'next'.                                            */
        it->hwut.section = myGen4_section_array_begin;
        if( it->hwut.section == myGen4_section_array_end ) {
            return 0;
        }
        it->hwut.section->init(it);
        return 1;
    }
    else if( hwut_cursor_next(&it->hwut.cursor) ) { 
        return 1;
    }
    /* Try to step into the next generator section.                          */
    ++(it->hwut.section);
    if( it->hwut.section == myGen4_section_array_end ) {
        return 0;
    }
    it->hwut.section->init(it);
    return 1;
}

int
myGen4_next(myGen4_t* it)
/* Set iterator to next admissible setting. The internal cursor will point 
 * to the next setting (which is not necessarily admissible).
 *
 * RETURNS: 0 if no further iterator is present.
 *          1 if the found setting is the next and valid.                    */
{
    if( it->hwut.section == myGen4_section_array_end ) {
        return 0;
    }

    /* Increment the iterator until something admissible is found.           */
    while( 1 + 1 == 2 ) {
        if( ! myGen4_intern_next(it) ) {
            return 0;
        }
        /* 'implement' returns 0, if implementation impossible.              */
        if( it->hwut.section->implement(it) ) {
            /* Check additional constraints.                                 */
            if( it->hwut.section->is_admissible(it) ) {
                break;
            }
        }
    }

    return 1;
}

hwut_cursor_key_t 
myGen4_key_get(myGen4_t* it)
/* This function is the inverse of 'myGen4_set(key)'.                 
 *
 * RETURNS: A numeric value, i.e. a 'key' which represents the iterator.     */
{
    return   it->hwut.section->key_offset 
           + hwut_cursor_to_key(&it->hwut.cursor);
}

void              
myGen4_key_set(myGen4_t* it, hwut_cursor_key_t key)
/* This function is the inverse of 'myGen4_get()'.                 
 *
 * Sets the iterator corresponding a numeric 'key'. In contrary to 'next'
 * it is possible to set inadmissible iterator settings using this function. 
 * If unsure about admissibility, use myGen4_is_admissible()
 * to double check.                                                          */            
{
    const myGen4_section_t* section_p = myGen4_section_array_begin;
    
    /* Find the section to which the key belongs.                            */
    while( section_p->key_offset > key && section_p != myGen4_section_array_end ) {
        ++section_p;
    }

    if( section_p != myGen4_section_array_begin ) {
        --section_p;
    } 

    if( section_p != it->hwut.section ) {
        it->hwut.section = section_p;
        it->hwut.section->init(it);
    }

    /* Cursor's key = key - key offset of current section.                     
     *
     * NOTE: Constant line iteration is a special case where the cursor has 
     *       only one dimension of the size = setting number.                */
    hwut_cursor_from_key(&it->hwut.cursor, 
                         key - it->hwut.section->key_offset);
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void              
myGen4_print(FILE* fh, myGen4_t* it)
{
    int i;
    (void)i;
    fprintf(fh, "    key: %li;\n", (long)myGen4_key_get(it));
    fprintf(fh, "    x:   "); fprintf(fh, "%i%s", (int)it->x, "\n");
    fprintf(fh, "    y:   "); fprintf(fh, "%f%s", (float)it->y, "\n");

}

void              
myGen4_print_table_header(FILE* fh, const char* Separator)
{
    fprintf(fh, "# key%s x%s y%s \n", Separator, Separator, Separator);
}

void              
myGen4_print_table_line(FILE* fh, myGen4_t* it, const char* Separator)
{
    int i;
    (void)i;
    fprintf(fh, "%li%s", (long)myGen4_key_get(it), Separator);
    it->hwut.section->implement(it);
    fprintf(fh, "%i%s", (int)it->x, Separator);
    fprintf(fh, "%f%s", (float)it->y, Separator);
    fprintf(fh, "\n");
}

void              
myGen4_print_table(FILE* fh, const char* Separator)
{
    myGen4_t it;

    myGen4_init(&it);

    myGen4_print_table_header(fh, Separator);

    while( myGen4_next(&it) ) {
        myGen4_print_table_line(fh, &it, Separator);
    }
}
#else
void              
myGen4_print(FILE* fh, myGen4_t* it)
{ (void)it; (void)fh; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen4_print_table_header(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen4_print_table_line(FILE* fh, myGen4_t* it, const char* Separator)
{ (void)it; (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen4_print_table(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }
#endif


void 
myGen4_0_init(myGen4_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 1, 3,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen4_0_implement(myGen4_t* it)
{
    it->x = (int)1000;
    {
        int primary_front = (it->x - 1);
        int primary_back  = (it->x + 1);
        float step_size     = (float)1;
        float index         = (float)(it->hwut.cursor.index[1]);
        float delta         = index * step_size;
        float value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->y = (float)value;
    }

    return 1;
}                      

int  
myGen4_0_is_admissible(myGen4_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

void 
myGen4_1_init(myGen4_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 1, 7,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen4_1_implement(myGen4_t* it)
{
    it->x = (int)100;
    {
        int primary_front = (it->x - 3);
        int primary_back  = (it->x + 3);
        float step_size     = (float)1;
        float index         = (float)(it->hwut.cursor.index[1]);
        float delta         = index * step_size;
        float value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->y = (float)value;
    }

    return 1;
}                      

int  
myGen4_1_is_admissible(myGen4_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

void 
myGen4_2_init(myGen4_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 1, 1,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen4_2_implement(myGen4_t* it)
{
    it->x = (int)99;
    {
        float value         = (float)it->x;
        it->y = (float)value;
    }

    return 1;
}                      

int  
myGen4_2_is_admissible(myGen4_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

void 
myGen4_3_init(myGen4_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 1, 8,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen4_3_implement(myGen4_t* it)
{
    it->x = (int)10;
    {
        int primary_front = (it->x - 0.5);
        int primary_back  = (it->x + 1.25);
        float step_size     = (float)0.25;
        float index         = (float)(it->hwut.cursor.index[1]);
        float delta         = index * step_size;
        float value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->y = (float)value;
    }

    return 1;
}                      

int  
myGen4_3_is_admissible(myGen4_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

void 
myGen4_4_init(myGen4_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 1, 4,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen4_4_implement(myGen4_t* it)
{
    it->x = (int)0;
    {
        float cut_front     = (float)-1.5;
        float cut_back      = (float)2;
        int primary_front = (it->x - 3);
        int primary_back  = (it->x + 1.5);
        float step_size     = (float)1.5;
        float index         = (float)(it->hwut.cursor.index[1]);
        float delta         = index * step_size;
        float value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        if     ( value < cut_front )     return 0; /* impossible */
        else if( value > cut_back )      return 0; /* impossible */
        it->y = (float)value;
    }

    return 1;
}                      

int  
myGen4_4_is_admissible(myGen4_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

#include "hwut_generated_iterator.h"

extern void   myGen2_0_init(myGen2_t* it);
extern int    myGen2_0_implement(myGen2_t* it);
extern int    myGen2_0_is_admissible(myGen2_t* it);
extern void   myGen2_1_init(myGen2_t* it);
extern int    myGen2_1_implement(myGen2_t* it);
extern int    myGen2_1_is_admissible(myGen2_t* it);
extern void   myGen2_2_init(myGen2_t* it);
extern int    myGen2_2_implement(myGen2_t* it);
extern int    myGen2_2_is_admissible(myGen2_t* it);
extern void   myGen2_3_init(myGen2_t* it);
extern int    myGen2_3_implement(myGen2_t* it);
extern int    myGen2_3_is_admissible(myGen2_t* it);
extern void   myGen2_4_init(myGen2_t* it);
extern int    myGen2_4_implement(myGen2_t* it);
extern int    myGen2_4_is_admissible(myGen2_t* it);


static const myGen2_section_t  myGen2_section_array[5] = { 
    { 0, myGen2_0_init, myGen2_0_implement, myGen2_0_is_admissible },
    { 2, myGen2_1_init, myGen2_1_implement, myGen2_1_is_admissible },
    { 4, myGen2_2_init, myGen2_2_implement, myGen2_2_is_admissible },
    { 6, myGen2_3_init, myGen2_3_implement, myGen2_3_is_admissible },
    { 8, myGen2_4_init, myGen2_4_implement, myGen2_4_is_admissible },
 
};
static const myGen2_section_t* myGen2_section_array_begin = &myGen2_section_array[0];
static const myGen2_section_t* myGen2_section_array_end   = &myGen2_section_array[5];

static const myGen2_array_array_t myGen2_array_array_0 = { 2, {  1,  2, 0, 0,  } };
static const myGen2_array_array_t myGen2_array_array_1 = { 3, {  1,  2,  3, 0,  } };
static const myGen2_array_array_t myGen2_array_array_2 = { 4, {  1,  2,  3,  4,  } };
static const myGen2_array_array_t myGen2_array_array_3 = { 2, {  5,  6, 0, 0,  } };
static const myGen2_array_array_t myGen2_array_array_4 = { 2, {  7,  8, 0, 0,  } };
static const myGen2_array_array_t myGen2_array_array_5 = { 1, {  1, 0, 0, 0,  } };
static const myGen2_array_farray_t myGen2_array_farray_0 = { 1, {  1.500000, 0.0,  } };
static const myGen2_array_farray_t myGen2_array_farray_1 = { 2, {  6.000000,  6.100000,  } };
static const myGen2_array_farray_t myGen2_array_farray_2 = { 2, {  7.000000,  7.100000,  } };


void
myGen2_init(myGen2_t* it)
/* Use provided memory to construct an object of type myGen2_t.
 *                                                                           */
{
    it->hwut.print   = myGen2_print;
    it->hwut.section = (void*)0;
}

static int
myGen2_intern_next(myGen2_t* it)
{
    if( it->hwut.section == (void*)0 ) {
        /* The very first 'next'.                                            */
        it->hwut.section = myGen2_section_array_begin;
        if( it->hwut.section == myGen2_section_array_end ) {
            return 0;
        }
        it->hwut.section->init(it);
        return 1;
    }
    else if( hwut_cursor_next(&it->hwut.cursor) ) { 
        return 1;
    }
    /* Try to step into the next generator section.                          */
    ++(it->hwut.section);
    if( it->hwut.section == myGen2_section_array_end ) {
        return 0;
    }
    it->hwut.section->init(it);
    return 1;
}

int
myGen2_next(myGen2_t* it)
/* Set iterator to next admissible setting. The internal cursor will point 
 * to the next setting (which is not necessarily admissible).
 *
 * RETURNS: 0 if no further iterator is present.
 *          1 if the found setting is the next and valid.                    */
{
    if( it->hwut.section == myGen2_section_array_end ) {
        return 0;
    }

    /* Increment the iterator until something admissible is found.           */
    while( 1 + 1 == 2 ) {
        if( ! myGen2_intern_next(it) ) {
            return 0;
        }
        /* 'implement' returns 0, if implementation impossible.              */
        if( it->hwut.section->implement(it) ) {
            /* Check additional constraints.                                 */
            if( it->hwut.section->is_admissible(it) ) {
                break;
            }
        }
    }

    return 1;
}

hwut_cursor_key_t 
myGen2_key_get(myGen2_t* it)
/* This function is the inverse of 'myGen2_set(key)'.                 
 *
 * RETURNS: A numeric value, i.e. a 'key' which represents the iterator.     */
{
    return   it->hwut.section->key_offset 
           + hwut_cursor_to_key(&it->hwut.cursor);
}

void              
myGen2_key_set(myGen2_t* it, hwut_cursor_key_t key)
/* This function is the inverse of 'myGen2_get()'.                 
 *
 * Sets the iterator corresponding a numeric 'key'. In contrary to 'next'
 * it is possible to set inadmissible iterator settings using this function. 
 * If unsure about admissibility, use myGen2_is_admissible()
 * to double check.                                                          */            
{
    const myGen2_section_t* section_p = myGen2_section_array_begin;
    
    /* Find the section to which the key belongs.                            */
    while( section_p->key_offset > key && section_p != myGen2_section_array_end ) {
        ++section_p;
    }

    if( section_p != myGen2_section_array_begin ) {
        --section_p;
    } 

    if( section_p != it->hwut.section ) {
        it->hwut.section = section_p;
        it->hwut.section->init(it);
    }

    /* Cursor's key = key - key offset of current section.                     
     *
     * NOTE: Constant line iteration is a special case where the cursor has 
     *       only one dimension of the size = setting number.                */
    hwut_cursor_from_key(&it->hwut.cursor, 
                         key - it->hwut.section->key_offset);
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void              
myGen2_print(FILE* fh, myGen2_t* it)
{
    int i;
    (void)i;
    fprintf(fh, "    key:    %li;\n", (long)myGen2_key_get(it));
    fprintf(fh, "    x:      "); fprintf(fh, "%i%s", (int)it->x, "\n");
    fprintf(fh, "    y:      "); fprintf(fh, "%f%s", (float)it->y, "\n");
    fprintf(fh, "    str:    "); fprintf(fh, "\"%s\"%s", (const char*)it->str, "\n");
    fprintf(fh, "    array:  "); hwut_IARRAY_print(it->array, "\n");
    fprintf(fh, "    farray: "); hwut_FARRAY_print(it->farray, "\n");

}

void              
myGen2_print_table_header(FILE* fh, const char* Separator)
{
    fprintf(fh, "# key%s x%s y%s str%s array%s farray%s \n", Separator, Separator, Separator, Separator, Separator, Separator);
}

void              
myGen2_print_table_line(FILE* fh, myGen2_t* it, const char* Separator)
{
    int i;
    (void)i;
    fprintf(fh, "%li%s", (long)myGen2_key_get(it), Separator);
    it->hwut.section->implement(it);
    fprintf(fh, "%i%s", (int)it->x, Separator);
    fprintf(fh, "%f%s", (float)it->y, Separator);
    fprintf(fh, "\"%s\"%s", (const char*)it->str, Separator);
    hwut_IARRAY_print(it->array, Separator);
    hwut_FARRAY_print(it->farray, Separator);
    fprintf(fh, "\n");
}

void              
myGen2_print_table(FILE* fh, const char* Separator)
{
    myGen2_t it;

    myGen2_init(&it);

    myGen2_print_table_header(fh, Separator);

    while( myGen2_next(&it) ) {
        myGen2_print_table_line(fh, &it, Separator);
    }
}
#else
void              
myGen2_print(FILE* fh, myGen2_t* it)
{ (void)it; (void)fh; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen2_print_table_header(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen2_print_table_line(FILE* fh, myGen2_t* it, const char* Separator)
{ (void)it; (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen2_print_table(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }
#endif


void 
myGen2_0_init(myGen2_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[5] = { 2, 1, 1, 1, 1,  };

    hwut_cursor_init(&it->hwut.cursor, 5, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen2_0_implement(myGen2_t* it)
{
    switch( it->hwut.cursor.index[0] ) {
        case 0: it->x = (int)0; break;
        case 1: it->x = (int)1; break;
    }
    it->y = 2.4;
    it->str = "e";
    it->array = &myGen2_array_array_0;
    it->farray = &myGen2_array_farray_0;

    return 1;
}                      

int  
myGen2_0_is_admissible(myGen2_t* it)
{
    /* Make setting parameters available under original name. */
#   define x      (it->x)
#   define y      (it->y)
#   define str    (it->str)
#   define array  (*(it->array))
#   define farray (*(it->farray))
    /* General constraints.   */
#   undef x
#   undef y
#   undef str
#   undef array
#   undef farray

    return 1;
}                      

void 
myGen2_1_init(myGen2_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[5] = { 1, 2, 1, 1, 1,  };

    hwut_cursor_init(&it->hwut.cursor, 5, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen2_1_implement(myGen2_t* it)
{
    it->x = (int)5;
    switch( it->hwut.cursor.index[1] ) {
        case 0: it->y = 7.1; break;
        case 1: it->y = 7.2; break;
    }
    it->str = "f";
    it->array = &myGen2_array_array_1;
    it->farray = &myGen2_array_farray_0;

    return 1;
}                      

int  
myGen2_1_is_admissible(myGen2_t* it)
{
    /* Make setting parameters available under original name. */
#   define x      (it->x)
#   define y      (it->y)
#   define str    (it->str)
#   define array  (*(it->array))
#   define farray (*(it->farray))
    /* General constraints.   */
#   undef x
#   undef y
#   undef str
#   undef array
#   undef farray

    return 1;
}                      

void 
myGen2_2_init(myGen2_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[5] = { 1, 1, 2, 1, 1,  };

    hwut_cursor_init(&it->hwut.cursor, 5, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen2_2_implement(myGen2_t* it)
{
    it->x = (int)6;
    it->y = 2.5;
    switch( it->hwut.cursor.index[2] ) {
        case 0: it->str = "X"; break;
        case 1: it->str = "Y"; break;
    }
    it->array = &myGen2_array_array_2;
    it->farray = &myGen2_array_farray_0;

    return 1;
}                      

int  
myGen2_2_is_admissible(myGen2_t* it)
{
    /* Make setting parameters available under original name. */
#   define x      (it->x)
#   define y      (it->y)
#   define str    (it->str)
#   define array  (*(it->array))
#   define farray (*(it->farray))
    /* General constraints.   */
#   undef x
#   undef y
#   undef str
#   undef array
#   undef farray

    return 1;
}                      

void 
myGen2_3_init(myGen2_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[5] = { 1, 1, 1, 2, 1,  };

    hwut_cursor_init(&it->hwut.cursor, 5, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen2_3_implement(myGen2_t* it)
{
    it->x = (int)7;
    it->y = 2.6;
    it->str = "i";
    switch( it->hwut.cursor.index[3] ) {
        case 0: it->array = &myGen2_array_array_3; break;
        case 1: it->array = &myGen2_array_array_4; break;
    }
    it->farray = &myGen2_array_farray_0;

    return 1;
}                      

int  
myGen2_3_is_admissible(myGen2_t* it)
{
    /* Make setting parameters available under original name. */
#   define x      (it->x)
#   define y      (it->y)
#   define str    (it->str)
#   define array  (*(it->array))
#   define farray (*(it->farray))
    /* General constraints.   */
#   undef x
#   undef y
#   undef str
#   undef array
#   undef farray

    return 1;
}                      

void 
myGen2_4_init(myGen2_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[5] = { 1, 1, 1, 1, 2,  };

    hwut_cursor_init(&it->hwut.cursor, 5, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen2_4_implement(myGen2_t* it)
{
    it->x = (int)8;
    it->y = 2.7;
    it->str = "j";
    it->array = &myGen2_array_array_5;
    switch( it->hwut.cursor.index[4] ) {
        case 0: it->farray = &myGen2_array_farray_1; break;
        case 1: it->farray = &myGen2_array_farray_2; break;
    }

    return 1;
}                      

int  
myGen2_4_is_admissible(myGen2_t* it)
{
    /* Make setting parameters available under original name. */
#   define x      (it->x)
#   define y      (it->y)
#   define str    (it->str)
#   define array  (*(it->array))
#   define farray (*(it->farray))
    /* General constraints.   */
#   undef x
#   undef y
#   undef str
#   undef array
#   undef farray

    return 1;
}                      

#include "hwut_generated_iterator.h"

extern void   myGen3_0_init(myGen3_t* it);
extern int    myGen3_0_implement(myGen3_t* it);
extern int    myGen3_0_is_admissible(myGen3_t* it);
extern void   myGen3_1_init(myGen3_t* it);
extern int    myGen3_1_implement(myGen3_t* it);
extern int    myGen3_1_is_admissible(myGen3_t* it);
extern void   myGen3_2_init(myGen3_t* it);
extern int    myGen3_2_implement(myGen3_t* it);
extern int    myGen3_2_is_admissible(myGen3_t* it);
extern void   myGen3_3_init(myGen3_t* it);
extern int    myGen3_3_implement(myGen3_t* it);
extern int    myGen3_3_is_admissible(myGen3_t* it);


static const myGen3_section_t  myGen3_section_array[4] = { 
    { 0, myGen3_0_init, myGen3_0_implement, myGen3_0_is_admissible },
    { 6, myGen3_1_init, myGen3_1_implement, myGen3_1_is_admissible },
    { 10, myGen3_2_init, myGen3_2_implement, myGen3_2_is_admissible },
    { 16, myGen3_3_init, myGen3_3_implement, myGen3_3_is_admissible },
 
};
static const myGen3_section_t* myGen3_section_array_begin = &myGen3_section_array[0];
static const myGen3_section_t* myGen3_section_array_end   = &myGen3_section_array[4];



void
myGen3_init(myGen3_t* it)
/* Use provided memory to construct an object of type myGen3_t.
 *                                                                           */
{
    it->hwut.print   = myGen3_print;
    it->hwut.section = (void*)0;
}

static int
myGen3_intern_next(myGen3_t* it)
{
    if( it->hwut.section == (void*)0 ) {
        /* The very first 'next'.                                            */
        it->hwut.section = myGen3_section_array_begin;
        if( it->hwut.section == myGen3_section_array_end ) {
            return 0;
        }
        it->hwut.section->init(it);
        return 1;
    }
    else if( hwut_cursor_next(&it->hwut.cursor) ) { 
        return 1;
    }
    /* Try to step into the next generator section.                          */
    ++(it->hwut.section);
    if( it->hwut.section == myGen3_section_array_end ) {
        return 0;
    }
    it->hwut.section->init(it);
    return 1;
}

int
myGen3_next(myGen3_t* it)
/* Set iterator to next admissible setting. The internal cursor will point 
 * to the next setting (which is not necessarily admissible).
 *
 * RETURNS: 0 if no further iterator is present.
 *          1 if the found setting is the next and valid.                    */
{
    if( it->hwut.section == myGen3_section_array_end ) {
        return 0;
    }

    /* Increment the iterator until something admissible is found.           */
    while( 1 + 1 == 2 ) {
        if( ! myGen3_intern_next(it) ) {
            return 0;
        }
        /* 'implement' returns 0, if implementation impossible.              */
        if( it->hwut.section->implement(it) ) {
            /* Check additional constraints.                                 */
            if( it->hwut.section->is_admissible(it) ) {
                break;
            }
        }
    }

    return 1;
}

hwut_cursor_key_t 
myGen3_key_get(myGen3_t* it)
/* This function is the inverse of 'myGen3_set(key)'.                 
 *
 * RETURNS: A numeric value, i.e. a 'key' which represents the iterator.     */
{
    return   it->hwut.section->key_offset 
           + hwut_cursor_to_key(&it->hwut.cursor);
}

void              
myGen3_key_set(myGen3_t* it, hwut_cursor_key_t key)
/* This function is the inverse of 'myGen3_get()'.                 
 *
 * Sets the iterator corresponding a numeric 'key'. In contrary to 'next'
 * it is possible to set inadmissible iterator settings using this function. 
 * If unsure about admissibility, use myGen3_is_admissible()
 * to double check.                                                          */            
{
    const myGen3_section_t* section_p = myGen3_section_array_begin;
    
    /* Find the section to which the key belongs.                            */
    while( section_p->key_offset > key && section_p != myGen3_section_array_end ) {
        ++section_p;
    }

    if( section_p != myGen3_section_array_begin ) {
        --section_p;
    } 

    if( section_p != it->hwut.section ) {
        it->hwut.section = section_p;
        it->hwut.section->init(it);
    }

    /* Cursor's key = key - key offset of current section.                     
     *
     * NOTE: Constant line iteration is a special case where the cursor has 
     *       only one dimension of the size = setting number.                */
    hwut_cursor_from_key(&it->hwut.cursor, 
                         key - it->hwut.section->key_offset);
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void              
myGen3_print(FILE* fh, myGen3_t* it)
{
    int i;
    (void)i;
    fprintf(fh, "    key: %li;\n", (long)myGen3_key_get(it));
    fprintf(fh, "    x:   "); fprintf(fh, "%i%s", (int)it->x, "\n");
    fprintf(fh, "    y:   "); fprintf(fh, "%f%s", (float)it->y, "\n");

}

void              
myGen3_print_table_header(FILE* fh, const char* Separator)
{
    fprintf(fh, "# key%s x%s y%s \n", Separator, Separator, Separator);
}

void              
myGen3_print_table_line(FILE* fh, myGen3_t* it, const char* Separator)
{
    int i;
    (void)i;
    fprintf(fh, "%li%s", (long)myGen3_key_get(it), Separator);
    it->hwut.section->implement(it);
    fprintf(fh, "%i%s", (int)it->x, Separator);
    fprintf(fh, "%f%s", (float)it->y, Separator);
    fprintf(fh, "\n");
}

void              
myGen3_print_table(FILE* fh, const char* Separator)
{
    myGen3_t it;

    myGen3_init(&it);

    myGen3_print_table_header(fh, Separator);

    while( myGen3_next(&it) ) {
        myGen3_print_table_line(fh, &it, Separator);
    }
}
#else
void              
myGen3_print(FILE* fh, myGen3_t* it)
{ (void)it; (void)fh; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen3_print_table_header(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen3_print_table_line(FILE* fh, myGen3_t* it, const char* Separator)
{ (void)it; (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen3_print_table(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }
#endif


void 
myGen3_0_init(myGen3_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 6, 1,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen3_0_implement(myGen3_t* it)
{
    {
        int primary_front = (int)0;
        int primary_back  = (int)5;
        int step_size     = (int)1;
        int index         = (int)(it->hwut.cursor.index[0]);
        int delta         = index * step_size;
        int value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->x = (int)value;
    }
    it->y = -2.0;

    return 1;
}                      

int  
myGen3_0_is_admissible(myGen3_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

void 
myGen3_1_init(myGen3_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 4, 1,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen3_1_implement(myGen3_t* it)
{
    {
        int primary_front = (int)5;
        int primary_back  = (int)10;
        int step_size     = (int)2;
        int index         = (int)(it->hwut.cursor.index[0]);
        int delta         = index * step_size;
        int value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->x = (int)value;
    }
    it->y = -1.0;

    return 1;
}                      

int  
myGen3_1_is_admissible(myGen3_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

void 
myGen3_2_init(myGen3_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 1, 6,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen3_2_implement(myGen3_t* it)
{
    it->x = (int)11;
    {
        float primary_front = 0.0;
        float primary_back  = 5.0;
        float step_size     = (float)1;
        float index         = (float)(it->hwut.cursor.index[1]);
        float delta         = index * step_size;
        float value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->y = (float)value;
    }

    return 1;
}                      

int  
myGen3_2_is_admissible(myGen3_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

void 
myGen3_3_init(myGen3_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 1, 5,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen3_3_implement(myGen3_t* it)
{
    it->x = (int)12;
    {
        float primary_front = 5.0;
        float primary_back  = 7.0;
        float step_size     = (float)0.5;
        float index         = (float)(it->hwut.cursor.index[1]);
        float delta         = index * step_size;
        float value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->y = (float)value;
    }

    return 1;
}                      

int  
myGen3_3_is_admissible(myGen3_t* it)
{
    /* Make setting parameters available under original name. */
#   define x (it->x)
#   define y (it->y)
    /* General constraints.   */
#   undef x
#   undef y

    return 1;
}                      

#include "hwut_generated_iterator.h"

extern void   myGen1_0_init(myGen1_t* it);
extern int    myGen1_0_implement(myGen1_t* it);
extern int    myGen1_0_is_admissible(myGen1_t* it);


static const myGen1_section_t  myGen1_section_array[1] = { 
    { 0, myGen1_0_init, myGen1_0_implement, myGen1_0_is_admissible },
 
};
static const myGen1_section_t* myGen1_section_array_begin = &myGen1_section_array[0];
static const myGen1_section_t* myGen1_section_array_end   = &myGen1_section_array[1];

static const myGen1_array_array_t myGen1_array_array_0 = { 4, {  1,  2,  3,  4,  } };
static const myGen1_array_array_t myGen1_array_array_1 = { 3, {  1,  2,  3, 0,  } };
static const myGen1_array_array_t myGen1_array_array_2 = { 2, {  1,  2, 0, 0,  } };
static const myGen1_array_array_t myGen1_array_array_3 = { 1, {  1, 0, 0, 0,  } };
static const myGen1_array_farray_t myGen1_array_farray_0 = { 2, {  1.000000,  1.100000,  } };
static const myGen1_array_farray_t myGen1_array_farray_1 = { 2, {  2.000000,  1.200000,  } };
static const myGen1_array_farray_t myGen1_array_farray_2 = { 2, {  3.000000,  1.300000,  } };
static const myGen1_array_farray_t myGen1_array_farray_3 = { 2, {  4.000000,  1.400000,  } };


void
myGen1_init(myGen1_t* it)
/* Use provided memory to construct an object of type myGen1_t.
 *                                                                           */
{
    it->hwut.print   = myGen1_print;
    it->hwut.section = (void*)0;
}

static int
myGen1_intern_next(myGen1_t* it)
{
    if( it->hwut.section == (void*)0 ) {
        /* The very first 'next'.                                            */
        it->hwut.section = myGen1_section_array_begin;
        if( it->hwut.section == myGen1_section_array_end ) {
            return 0;
        }
        it->hwut.section->init(it);
        return 1;
    }
    else if( hwut_cursor_next(&it->hwut.cursor) ) { 
        return 1;
    }
    /* Try to step into the next generator section.                          */
    ++(it->hwut.section);
    if( it->hwut.section == myGen1_section_array_end ) {
        return 0;
    }
    it->hwut.section->init(it);
    return 1;
}

int
myGen1_next(myGen1_t* it)
/* Set iterator to next admissible setting. The internal cursor will point 
 * to the next setting (which is not necessarily admissible).
 *
 * RETURNS: 0 if no further iterator is present.
 *          1 if the found setting is the next and valid.                    */
{
    if( it->hwut.section == myGen1_section_array_end ) {
        return 0;
    }

    /* Increment the iterator until something admissible is found.           */
    while( 1 + 1 == 2 ) {
        if( ! myGen1_intern_next(it) ) {
            return 0;
        }
        /* 'implement' returns 0, if implementation impossible.              */
        if( it->hwut.section->implement(it) ) {
            /* Check additional constraints.                                 */
            if( it->hwut.section->is_admissible(it) ) {
                break;
            }
        }
    }

    return 1;
}

hwut_cursor_key_t 
myGen1_key_get(myGen1_t* it)
/* This function is the inverse of 'myGen1_set(key)'.                 
 *
 * RETURNS: A numeric value, i.e. a 'key' which represents the iterator.     */
{
    return   it->hwut.section->key_offset 
           + hwut_cursor_to_key(&it->hwut.cursor);
}

void              
myGen1_key_set(myGen1_t* it, hwut_cursor_key_t key)
/* This function is the inverse of 'myGen1_get()'.                 
 *
 * Sets the iterator corresponding a numeric 'key'. In contrary to 'next'
 * it is possible to set inadmissible iterator settings using this function. 
 * If unsure about admissibility, use myGen1_is_admissible()
 * to double check.                                                          */            
{
    const myGen1_section_t* section_p = myGen1_section_array_begin;
    
    /* Find the section to which the key belongs.                            */
    while( section_p->key_offset > key && section_p != myGen1_section_array_end ) {
        ++section_p;
    }

    if( section_p != myGen1_section_array_begin ) {
        --section_p;
    } 

    if( section_p != it->hwut.section ) {
        it->hwut.section = section_p;
        it->hwut.section->init(it);
    }

    /* Cursor's key = key - key offset of current section.                     
     *
     * NOTE: Constant line iteration is a special case where the cursor has 
     *       only one dimension of the size = setting number.                */
    hwut_cursor_from_key(&it->hwut.cursor, 
                         key - it->hwut.section->key_offset);
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void              
myGen1_print(FILE* fh, myGen1_t* it)
{
    int i;
    (void)i;
    fprintf(fh, "    key:    %li;\n", (long)myGen1_key_get(it));
    fprintf(fh, "    x:      "); fprintf(fh, "%i%s", (int)it->x, "\n");
    fprintf(fh, "    y:      "); fprintf(fh, "%f%s", (float)it->y, "\n");
    fprintf(fh, "    str:    "); fprintf(fh, "\"%s\"%s", (const char*)it->str, "\n");
    fprintf(fh, "    array:  "); hwut_IARRAY_print(it->array, "\n");
    fprintf(fh, "    farray: "); hwut_FARRAY_print(it->farray, "\n");

}

void              
myGen1_print_table_header(FILE* fh, const char* Separator)
{
    fprintf(fh, "# key%s x%s y%s str%s array%s farray%s \n", Separator, Separator, Separator, Separator, Separator, Separator);
}

void              
myGen1_print_table_line(FILE* fh, myGen1_t* it, const char* Separator)
{
    int i;
    (void)i;
    fprintf(fh, "%li%s", (long)myGen1_key_get(it), Separator);
    it->hwut.section->implement(it);
    fprintf(fh, "%i%s", (int)it->x, Separator);
    fprintf(fh, "%f%s", (float)it->y, Separator);
    fprintf(fh, "\"%s\"%s", (const char*)it->str, Separator);
    hwut_IARRAY_print(it->array, Separator);
    hwut_FARRAY_print(it->farray, Separator);
    fprintf(fh, "\n");
}

void              
myGen1_print_table(FILE* fh, const char* Separator)
{
    myGen1_t it;

    myGen1_init(&it);

    myGen1_print_table_header(fh, Separator);

    while( myGen1_next(&it) ) {
        myGen1_print_table_line(fh, &it, Separator);
    }
}
#else
void              
myGen1_print(FILE* fh, myGen1_t* it)
{ (void)it; (void)fh; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen1_print_table_header(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen1_print_table_line(FILE* fh, myGen1_t* it, const char* Separator)
{ (void)it; (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
myGen1_print_table(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }
#endif

typedef struct {
    int                          x;
    float                        y;
    const char*                  str;
    const myGen1_array_array_t*   array;
    const myGen1_array_farray_t*  farray;
} myGen1_constant_line_db_entry_t;

static const myGen1_constant_line_db_entry_t myGen1_constant_line_db[4] = {
    { (int)1, (float)2.0, "a", &myGen1_array_array_0, &myGen1_array_farray_0,  },
    { (int)2, (float)2.1, "b", &myGen1_array_array_1, &myGen1_array_farray_1,  },
    { (int)3, (float)2.2, "c", &myGen1_array_array_2, &myGen1_array_farray_2,  },
    { (int)4, (float)2.3, "d", &myGen1_array_array_3, &myGen1_array_farray_3,  },
};

void 
myGen1_0_init(myGen1_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[1] = { 4 };

    hwut_cursor_init(&it->hwut.cursor, 1, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
myGen1_0_implement(myGen1_t* it)
{
    const myGen1_constant_line_db_entry_t* line_p = &myGen1_constant_line_db[it->hwut.cursor.index[0]];

    it->x = line_p->x;
    it->y = line_p->y;
    it->str = line_p->str;
    it->array = line_p->array;
    it->farray = line_p->farray;

    return 1;
}                      

int  
myGen1_0_is_admissible(myGen1_t* it)
{

    return 1;
}                      

