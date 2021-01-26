/* This file has been generated with HWUT 0.27.4.
 *___________________________________________________________________________*/
#include "BitFieldIterator.h"

extern void   Error_0_init(Error_t* it);
extern int    Error_0_implement(Error_t* it);
extern int    Error_0_is_admissible(Error_t* it);


static int   Error_implement(Error_t* it);

static const Error_section_t  Error_section_array[1] = { 
    { 0, Error_0_init, Error_0_implement, Error_0_is_admissible },
 
};
static const Error_section_t* Error_section_array_begin = &Error_section_array[0];
static const Error_section_t* Error_section_array_end   = &Error_section_array[1];



void
Error_init(Error_t* it)
/* Use provided memory to construct an object of type Error_t.
 *                                                                           */
{
    it->hwut.print   = Error_print;
    it->hwut.section = (void*)0;
}

static int
Error_intern_next(Error_t* it)
{
    if( it->hwut.section == (void*)0 ) {
        /* The very first 'next'.                                            */
        it->hwut.section = Error_section_array_begin;
        if( it->hwut.section == Error_section_array_end ) {
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
    if( it->hwut.section == Error_section_array_end ) {
        return 0;
    }
    it->hwut.section->init(it);
    return 1;
}

int
Error_next(Error_t* it)
/* Set iterator to next admissible setting. The internal cursor will point 
 * to the next setting (which is not necessarily admissible).
 *
 * RETURNS: 0 if no further iterator is present.
 *          1 if the found setting is the next and valid.                    */
{
    if( it->hwut.section == Error_section_array_end ) {
        return 0;
    }

    /* Increment the iterator until something admissible is found.           */
    while( 1 + 1 == 2 ) {
        if( ! Error_intern_next(it) ) {
            return 0;
        }
        if( Error_implement(it) ) {
            return 1;
        }
    }
}

static int
Error_implement(Error_t* it)
/* Sets the concrete values for iterator members according to current setting
 * of .cursor. 
 *
 * RETURNS: 0 if implementation was successful.
 *          1 if implementation failed.                                      */
{
    /* 'implement' returns 0, if implementation impossible.                  */
    if( ! it->hwut.section->implement(it) ) {
        return 0;
    }
    /* Check additional constraints.                                         */
    return it->hwut.section->is_admissible(it);
}

hwut_cursor_key_t 
Error_key_max()
/* RETURNS: the maximum value of the iterator key.                           */
{
    return (hwut_cursor_key_t)2;
}

hwut_cursor_key_t 
Error_key_get(Error_t* it)
/* This function is the inverse of 'Error_set(key)'.                 
 *
 * RETURNS: A numeric value, i.e. a 'key' which represents the iterator.     */
{
    return   it->hwut.section->key_offset 
           + hwut_cursor_to_key(&it->hwut.cursor);
}

int              
Error_key_set(Error_t* it, hwut_cursor_key_t key)
/* This function is the inverse of 'Error_get()'.                 
 *
 * Sets the iterator corresponding a numeric 'key'. In contrary to 'next'
 * it is possible to set inadmissible iterator settings using this function. 
 *
 * RETURNS: 0 -- if setting could not be implemented or was inadmissible.
 *          1 -- if setting is ok.                                           */
{
    const Error_section_t* section_p = Error_section_array_begin;
    
    /* Find the section to which the key belongs.                            */
    while( section_p->key_offset > key && section_p != Error_section_array_end ) {
        ++section_p;
    }

    if( section_p != Error_section_array_begin ) {
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

    return Error_implement(it);
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void              
Error_print(FILE* fh, Error_t* it)
{
    int i;
    (void)i;
    fprintf(fh, "    key:    %li;\n", (long)Error_key_get(it));
    fprintf(fh, "    bit_n1: "); fprintf(fh, "%i%s", (int)it->bit_n1, "\n");
    fprintf(fh, "    bits1:  "); fprintf(fh, "%i%s", (int)it->bits1, "\n");
    fprintf(fh, "    bit_n2: "); fprintf(fh, "%i%s", (int)it->bit_n2, "\n");
    fprintf(fh, "    bits2:  "); fprintf(fh, "%i%s", (int)it->bits2, "\n");
    fprintf(fh, "    bit_n3: "); fprintf(fh, "%i%s", (int)it->bit_n3, "\n");
    fprintf(fh, "    bits3:  "); fprintf(fh, "%i%s", (int)it->bits3, "\n");

}

void              
Error_print_table_header(FILE* fh, const char* Separator)
{
    fprintf(fh, "# key%s bit_n1%s bits1%s bit_n2%s bits2%s bit_n3%s bits3%s \n", Separator, Separator, Separator, Separator, Separator, Separator, Separator);
}

void              
Error_print_table_line(FILE* fh, Error_t* it, const char* Separator)
{
    int i;
    (void)i;
    fprintf(fh, "%li%s", (long)Error_key_get(it), Separator);
    it->hwut.section->implement(it);
    fprintf(fh, "%i%s", (int)it->bit_n1, Separator);
    fprintf(fh, "%i%s", (int)it->bits1, Separator);
    fprintf(fh, "%i%s", (int)it->bit_n2, Separator);
    fprintf(fh, "%i%s", (int)it->bits2, Separator);
    fprintf(fh, "%i%s", (int)it->bit_n3, Separator);
    fprintf(fh, "%i%s", (int)it->bits3, Separator);
    fprintf(fh, "\n");
}

void              
Error_print_table(FILE* fh, const char* Separator)
{
    Error_t it;

    Error_init(&it);

    Error_print_table_header(fh, Separator);

    while( Error_next(&it) ) {
        Error_print_table_line(fh, &it, Separator);
    }
}
#else
void              
Error_print(FILE* fh, Error_t* it)
{ (void)it; (void)fh; /* Dummy, <stdio.h> forbidden. */ }

void              
Error_print_table_header(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
Error_print_table_line(FILE* fh, Error_t* it, const char* Separator)
{ (void)it; (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
Error_print_table(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }
#endif

typedef struct {
    uint32_t bit_n1;
    uint32_t bits1;
    uint32_t bit_n2;
    uint32_t bits2;
    uint32_t bit_n3;
    uint32_t bits3;
} Error_constant_line_db_entry_t;

static const Error_constant_line_db_entry_t Error_constant_line_db[3] = {
    { (uint32_t)8, (uint32_t)256, (uint32_t)16, (uint32_t)65535U, (uint32_t)24, (uint32_t)16777215U,  },
    { (uint32_t)8, (uint32_t)255, (uint32_t)16, (uint32_t)65536U, (uint32_t)24, (uint32_t)16777215U,  },
    { (uint32_t)8, (uint32_t)255, (uint32_t)16, (uint32_t)65535U, (uint32_t)24, (uint32_t)16777216U,  },
};

void 
Error_0_init(Error_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[1] = { 3 };

    hwut_cursor_init(&it->hwut.cursor, 1, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
Error_0_implement(Error_t* it)
{
    const Error_constant_line_db_entry_t* line_p = &Error_constant_line_db[it->hwut.cursor.index[0]];

    it->bit_n1 = line_p->bit_n1;
    it->bits1 = line_p->bits1;
    it->bit_n2 = line_p->bit_n2;
    it->bits2 = line_p->bits2;
    it->bit_n3 = line_p->bit_n3;
    it->bits3 = line_p->bits3;

    return 1;
}                      

int  
Error_0_is_admissible(Error_t* it)
{

    return 1;
}                      

/* This file has been generated with HWUT 0.27.4.
 *___________________________________________________________________________*/
#include "BitFieldIterator.h"

extern void   Three_0_init(Three_t* it);
extern int    Three_0_implement(Three_t* it);
extern int    Three_0_is_admissible(Three_t* it);


static int   Three_implement(Three_t* it);

static const Three_section_t  Three_section_array[1] = { 
    { 0, Three_0_init, Three_0_implement, Three_0_is_admissible },
 
};
static const Three_section_t* Three_section_array_begin = &Three_section_array[0];
static const Three_section_t* Three_section_array_end   = &Three_section_array[1];



void
Three_init(Three_t* it)
/* Use provided memory to construct an object of type Three_t.
 *                                                                           */
{
    it->hwut.print   = Three_print;
    it->hwut.section = (void*)0;
}

static int
Three_intern_next(Three_t* it)
{
    if( it->hwut.section == (void*)0 ) {
        /* The very first 'next'.                                            */
        it->hwut.section = Three_section_array_begin;
        if( it->hwut.section == Three_section_array_end ) {
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
    if( it->hwut.section == Three_section_array_end ) {
        return 0;
    }
    it->hwut.section->init(it);
    return 1;
}

int
Three_next(Three_t* it)
/* Set iterator to next admissible setting. The internal cursor will point 
 * to the next setting (which is not necessarily admissible).
 *
 * RETURNS: 0 if no further iterator is present.
 *          1 if the found setting is the next and valid.                    */
{
    if( it->hwut.section == Three_section_array_end ) {
        return 0;
    }

    /* Increment the iterator until something admissible is found.           */
    while( 1 + 1 == 2 ) {
        if( ! Three_intern_next(it) ) {
            return 0;
        }
        if( Three_implement(it) ) {
            return 1;
        }
    }
}

static int
Three_implement(Three_t* it)
/* Sets the concrete values for iterator members according to current setting
 * of .cursor. 
 *
 * RETURNS: 0 if implementation was successful.
 *          1 if implementation failed.                                      */
{
    /* 'implement' returns 0, if implementation impossible.                  */
    if( ! it->hwut.section->implement(it) ) {
        return 0;
    }
    /* Check additional constraints.                                         */
    return it->hwut.section->is_admissible(it);
}

hwut_cursor_key_t 
Three_key_max()
/* RETURNS: the maximum value of the iterator key.                           */
{
    return (hwut_cursor_key_t)32767;
}

hwut_cursor_key_t 
Three_key_get(Three_t* it)
/* This function is the inverse of 'Three_set(key)'.                 
 *
 * RETURNS: A numeric value, i.e. a 'key' which represents the iterator.     */
{
    return   it->hwut.section->key_offset 
           + hwut_cursor_to_key(&it->hwut.cursor);
}

int              
Three_key_set(Three_t* it, hwut_cursor_key_t key)
/* This function is the inverse of 'Three_get()'.                 
 *
 * Sets the iterator corresponding a numeric 'key'. In contrary to 'next'
 * it is possible to set inadmissible iterator settings using this function. 
 *
 * RETURNS: 0 -- if setting could not be implemented or was inadmissible.
 *          1 -- if setting is ok.                                           */
{
    const Three_section_t* section_p = Three_section_array_begin;
    
    /* Find the section to which the key belongs.                            */
    while( section_p->key_offset > key && section_p != Three_section_array_end ) {
        ++section_p;
    }

    if( section_p != Three_section_array_begin ) {
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

    return Three_implement(it);
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void              
Three_print(FILE* fh, Three_t* it)
{
    int i;
    (void)i;
    fprintf(fh, "    key:    %li;\n", (long)Three_key_get(it));
    fprintf(fh, "    bit_n1: "); fprintf(fh, "%i%s", (int)it->bit_n1, "\n");
    fprintf(fh, "    bit_n2: "); fprintf(fh, "%i%s", (int)it->bit_n2, "\n");
    fprintf(fh, "    bit_n3: "); fprintf(fh, "%i%s", (int)it->bit_n3, "\n");

}

void              
Three_print_table_header(FILE* fh, const char* Separator)
{
    fprintf(fh, "# key%s bit_n1%s bit_n2%s bit_n3%s \n", Separator, Separator, Separator, Separator);
}

void              
Three_print_table_line(FILE* fh, Three_t* it, const char* Separator)
{
    int i;
    (void)i;
    fprintf(fh, "%li%s", (long)Three_key_get(it), Separator);
    it->hwut.section->implement(it);
    fprintf(fh, "%i%s", (int)it->bit_n1, Separator);
    fprintf(fh, "%i%s", (int)it->bit_n2, Separator);
    fprintf(fh, "%i%s", (int)it->bit_n3, Separator);
    fprintf(fh, "\n");
}

void              
Three_print_table(FILE* fh, const char* Separator)
{
    Three_t it;

    Three_init(&it);

    Three_print_table_header(fh, Separator);

    while( Three_next(&it) ) {
        Three_print_table_line(fh, &it, Separator);
    }
}
#else
void              
Three_print(FILE* fh, Three_t* it)
{ (void)it; (void)fh; /* Dummy, <stdio.h> forbidden. */ }

void              
Three_print_table_header(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
Three_print_table_line(FILE* fh, Three_t* it, const char* Separator)
{ (void)it; (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
Three_print_table(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }
#endif


void 
Three_0_init(Three_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[3] = { 32, 32, 32,  };

    hwut_cursor_init(&it->hwut.cursor, 3, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
Three_0_implement(Three_t* it)
{
    {
        uint32_t primary_front = (uint32_t)1;
        uint32_t primary_back  = (uint32_t)32;
        uint32_t step_size     = (uint32_t)1;
        uint32_t index         = (uint32_t)(it->hwut.cursor.index[0]);
        uint32_t delta         = index * step_size;
        uint32_t value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->bit_n1 = (uint32_t)value;
    }
    {
        uint32_t primary_front = (uint32_t)1;
        uint32_t primary_back  = (uint32_t)32;
        uint32_t step_size     = (uint32_t)1;
        uint32_t index         = (uint32_t)(it->hwut.cursor.index[1]);
        uint32_t delta         = index * step_size;
        uint32_t value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->bit_n2 = (uint32_t)value;
    }
    {
        uint32_t primary_front = (uint32_t)1;
        uint32_t primary_back  = (uint32_t)32;
        uint32_t step_size     = (uint32_t)1;
        uint32_t index         = (uint32_t)(it->hwut.cursor.index[2]);
        uint32_t delta         = index * step_size;
        uint32_t value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->bit_n3 = (uint32_t)value;
    }

    return 1;
}                      

int  
Three_0_is_admissible(Three_t* it)
{
    /* Make setting parameters available under original name. */
#   define bit_n1 (it->bit_n1)
#   define bit_n2 (it->bit_n2)
#   define bit_n3 (it->bit_n3)
    /* General constraints.   */
#   undef bit_n1
#   undef bit_n2
#   undef bit_n3

    return 1;
}                      

/* This file has been generated with HWUT 0.27.4.
 *___________________________________________________________________________*/
#include "BitFieldIterator.h"

extern void   Two_0_init(Two_t* it);
extern int    Two_0_implement(Two_t* it);
extern int    Two_0_is_admissible(Two_t* it);


static int   Two_implement(Two_t* it);

static const Two_section_t  Two_section_array[1] = { 
    { 0, Two_0_init, Two_0_implement, Two_0_is_admissible },
 
};
static const Two_section_t* Two_section_array_begin = &Two_section_array[0];
static const Two_section_t* Two_section_array_end   = &Two_section_array[1];



void
Two_init(Two_t* it)
/* Use provided memory to construct an object of type Two_t.
 *                                                                           */
{
    it->hwut.print   = Two_print;
    it->hwut.section = (void*)0;
}

static int
Two_intern_next(Two_t* it)
{
    if( it->hwut.section == (void*)0 ) {
        /* The very first 'next'.                                            */
        it->hwut.section = Two_section_array_begin;
        if( it->hwut.section == Two_section_array_end ) {
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
    if( it->hwut.section == Two_section_array_end ) {
        return 0;
    }
    it->hwut.section->init(it);
    return 1;
}

int
Two_next(Two_t* it)
/* Set iterator to next admissible setting. The internal cursor will point 
 * to the next setting (which is not necessarily admissible).
 *
 * RETURNS: 0 if no further iterator is present.
 *          1 if the found setting is the next and valid.                    */
{
    if( it->hwut.section == Two_section_array_end ) {
        return 0;
    }

    /* Increment the iterator until something admissible is found.           */
    while( 1 + 1 == 2 ) {
        if( ! Two_intern_next(it) ) {
            return 0;
        }
        if( Two_implement(it) ) {
            return 1;
        }
    }
}

static int
Two_implement(Two_t* it)
/* Sets the concrete values for iterator members according to current setting
 * of .cursor. 
 *
 * RETURNS: 0 if implementation was successful.
 *          1 if implementation failed.                                      */
{
    /* 'implement' returns 0, if implementation impossible.                  */
    if( ! it->hwut.section->implement(it) ) {
        return 0;
    }
    /* Check additional constraints.                                         */
    return it->hwut.section->is_admissible(it);
}

hwut_cursor_key_t 
Two_key_max()
/* RETURNS: the maximum value of the iterator key.                           */
{
    return (hwut_cursor_key_t)1023;
}

hwut_cursor_key_t 
Two_key_get(Two_t* it)
/* This function is the inverse of 'Two_set(key)'.                 
 *
 * RETURNS: A numeric value, i.e. a 'key' which represents the iterator.     */
{
    return   it->hwut.section->key_offset 
           + hwut_cursor_to_key(&it->hwut.cursor);
}

int              
Two_key_set(Two_t* it, hwut_cursor_key_t key)
/* This function is the inverse of 'Two_get()'.                 
 *
 * Sets the iterator corresponding a numeric 'key'. In contrary to 'next'
 * it is possible to set inadmissible iterator settings using this function. 
 *
 * RETURNS: 0 -- if setting could not be implemented or was inadmissible.
 *          1 -- if setting is ok.                                           */
{
    const Two_section_t* section_p = Two_section_array_begin;
    
    /* Find the section to which the key belongs.                            */
    while( section_p->key_offset > key && section_p != Two_section_array_end ) {
        ++section_p;
    }

    if( section_p != Two_section_array_begin ) {
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

    return Two_implement(it);
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void              
Two_print(FILE* fh, Two_t* it)
{
    int i;
    (void)i;
    fprintf(fh, "    key:    %li;\n", (long)Two_key_get(it));
    fprintf(fh, "    bit_n1: "); fprintf(fh, "%i%s", (int)it->bit_n1, "\n");
    fprintf(fh, "    bit_n2: "); fprintf(fh, "%i%s", (int)it->bit_n2, "\n");

}

void              
Two_print_table_header(FILE* fh, const char* Separator)
{
    fprintf(fh, "# key%s bit_n1%s bit_n2%s \n", Separator, Separator, Separator);
}

void              
Two_print_table_line(FILE* fh, Two_t* it, const char* Separator)
{
    int i;
    (void)i;
    fprintf(fh, "%li%s", (long)Two_key_get(it), Separator);
    it->hwut.section->implement(it);
    fprintf(fh, "%i%s", (int)it->bit_n1, Separator);
    fprintf(fh, "%i%s", (int)it->bit_n2, Separator);
    fprintf(fh, "\n");
}

void              
Two_print_table(FILE* fh, const char* Separator)
{
    Two_t   it;

    Two_init(&it);

    Two_print_table_header(fh, Separator);

    while( Two_next(&it) ) {
        Two_print_table_line(fh, &it, Separator);
    }
}
#else
void              
Two_print(FILE* fh, Two_t* it)
{ (void)it; (void)fh; /* Dummy, <stdio.h> forbidden. */ }

void              
Two_print_table_header(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
Two_print_table_line(FILE* fh, Two_t* it, const char* Separator)
{ (void)it; (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
Two_print_table(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }
#endif


void 
Two_0_init(Two_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[2] = { 32, 32,  };

    hwut_cursor_init(&it->hwut.cursor, 2, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
Two_0_implement(Two_t* it)
{
    {
        uint32_t primary_front = (uint32_t)1;
        uint32_t primary_back  = (uint32_t)32;
        uint32_t step_size     = (uint32_t)1;
        uint32_t index         = (uint32_t)(it->hwut.cursor.index[0]);
        uint32_t delta         = index * step_size;
        uint32_t value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->bit_n1 = (uint32_t)value;
    }
    {
        uint32_t primary_front = (uint32_t)1;
        uint32_t primary_back  = (uint32_t)32;
        uint32_t step_size     = (uint32_t)1;
        uint32_t index         = (uint32_t)(it->hwut.cursor.index[1]);
        uint32_t delta         = index * step_size;
        uint32_t value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->bit_n2 = (uint32_t)value;
    }

    return 1;
}                      

int  
Two_0_is_admissible(Two_t* it)
{
    /* Make setting parameters available under original name. */
#   define bit_n1 (it->bit_n1)
#   define bit_n2 (it->bit_n2)
    /* General constraints.   */
#   undef bit_n1
#   undef bit_n2

    return 1;
}                      

/* This file has been generated with HWUT 0.27.4.
 *___________________________________________________________________________*/
#include "BitFieldIterator.h"

extern void   One_0_init(One_t* it);
extern int    One_0_implement(One_t* it);
extern int    One_0_is_admissible(One_t* it);


static int   One_implement(One_t* it);

static const One_section_t  One_section_array[1] = { 
    { 0, One_0_init, One_0_implement, One_0_is_admissible },
 
};
static const One_section_t* One_section_array_begin = &One_section_array[0];
static const One_section_t* One_section_array_end   = &One_section_array[1];



void
One_init(One_t* it)
/* Use provided memory to construct an object of type One_t.
 *                                                                           */
{
    it->hwut.print   = One_print;
    it->hwut.section = (void*)0;
}

static int
One_intern_next(One_t* it)
{
    if( it->hwut.section == (void*)0 ) {
        /* The very first 'next'.                                            */
        it->hwut.section = One_section_array_begin;
        if( it->hwut.section == One_section_array_end ) {
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
    if( it->hwut.section == One_section_array_end ) {
        return 0;
    }
    it->hwut.section->init(it);
    return 1;
}

int
One_next(One_t* it)
/* Set iterator to next admissible setting. The internal cursor will point 
 * to the next setting (which is not necessarily admissible).
 *
 * RETURNS: 0 if no further iterator is present.
 *          1 if the found setting is the next and valid.                    */
{
    if( it->hwut.section == One_section_array_end ) {
        return 0;
    }

    /* Increment the iterator until something admissible is found.           */
    while( 1 + 1 == 2 ) {
        if( ! One_intern_next(it) ) {
            return 0;
        }
        if( One_implement(it) ) {
            return 1;
        }
    }
}

static int
One_implement(One_t* it)
/* Sets the concrete values for iterator members according to current setting
 * of .cursor. 
 *
 * RETURNS: 0 if implementation was successful.
 *          1 if implementation failed.                                      */
{
    /* 'implement' returns 0, if implementation impossible.                  */
    if( ! it->hwut.section->implement(it) ) {
        return 0;
    }
    /* Check additional constraints.                                         */
    return it->hwut.section->is_admissible(it);
}

hwut_cursor_key_t 
One_key_max()
/* RETURNS: the maximum value of the iterator key.                           */
{
    return (hwut_cursor_key_t)31;
}

hwut_cursor_key_t 
One_key_get(One_t* it)
/* This function is the inverse of 'One_set(key)'.                 
 *
 * RETURNS: A numeric value, i.e. a 'key' which represents the iterator.     */
{
    return   it->hwut.section->key_offset 
           + hwut_cursor_to_key(&it->hwut.cursor);
}

int              
One_key_set(One_t* it, hwut_cursor_key_t key)
/* This function is the inverse of 'One_get()'.                 
 *
 * Sets the iterator corresponding a numeric 'key'. In contrary to 'next'
 * it is possible to set inadmissible iterator settings using this function. 
 *
 * RETURNS: 0 -- if setting could not be implemented or was inadmissible.
 *          1 -- if setting is ok.                                           */
{
    const One_section_t* section_p = One_section_array_begin;
    
    /* Find the section to which the key belongs.                            */
    while( section_p->key_offset > key && section_p != One_section_array_end ) {
        ++section_p;
    }

    if( section_p != One_section_array_begin ) {
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

    return One_implement(it);
}

#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
void              
One_print(FILE* fh, One_t* it)
{
    int i;
    (void)i;
    fprintf(fh, "    key:    %li;\n", (long)One_key_get(it));
    fprintf(fh, "    bit_n1: "); fprintf(fh, "%i%s", (int)it->bit_n1, "\n");

}

void              
One_print_table_header(FILE* fh, const char* Separator)
{
    fprintf(fh, "# key%s bit_n1%s \n", Separator, Separator);
}

void              
One_print_table_line(FILE* fh, One_t* it, const char* Separator)
{
    int i;
    (void)i;
    fprintf(fh, "%li%s", (long)One_key_get(it), Separator);
    it->hwut.section->implement(it);
    fprintf(fh, "%i%s", (int)it->bit_n1, Separator);
    fprintf(fh, "\n");
}

void              
One_print_table(FILE* fh, const char* Separator)
{
    One_t   it;

    One_init(&it);

    One_print_table_header(fh, Separator);

    while( One_next(&it) ) {
        One_print_table_line(fh, &it, Separator);
    }
}
#else
void              
One_print(FILE* fh, One_t* it)
{ (void)it; (void)fh; /* Dummy, <stdio.h> forbidden. */ }

void              
One_print_table_header(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
One_print_table_line(FILE* fh, One_t* it, const char* Separator)
{ (void)it; (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }

void              
One_print_table(FILE* fh, const char* Separator)
{ (void)fh; (void)Separator; /* Dummy, <stdio.h> forbidden. */ }
#endif


void 
One_0_init(One_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[1] = { 32,  };

    hwut_cursor_init(&it->hwut.cursor, 1, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
One_0_implement(One_t* it)
{
    {
        uint32_t primary_front = (uint32_t)1;
        uint32_t primary_back  = (uint32_t)32;
        uint32_t step_size     = (uint32_t)1;
        uint32_t index         = (uint32_t)(it->hwut.cursor.index[0]);
        uint32_t delta         = index * step_size;
        uint32_t value         = primary_front + delta;
        if     ( delta < 0 )             return 0; /* impossible */
        else if( value < primary_front ) return 0; /* impossible */
        else if( value > primary_back )  return 0; /* impossible */
        it->bit_n1 = (uint32_t)value;
    }

    return 1;
}                      

int  
One_0_is_admissible(One_t* it)
{
    /* Make setting parameters available under original name. */
#   define bit_n1 (it->bit_n1)
    /* General constraints.   */
#   undef bit_n1

    return 1;
}                      

