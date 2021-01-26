#ifndef INCLUDE_GUAGE_HWUT_GENERATOR_myGen_iterator_h
#define INCLUDE_GUAGE_HWUT_GENERATOR_myGen_iterator_h
#include <stdint.h>

/* This file has been generated with HWUT 0.27.4.
 *___________________________________________________________________________*/
#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
#   include <stdio.h>
#else
    typedef int FILE; /* Required to implement the dummy 'print' functions.  */
#endif

#if ! defined(HWUT_OPTION_ALLOC_FORBIDDEN)
#   include <malloc.h>
#endif

#include <hwut_cursor.h>   /* Use: -I<<HWUT_PATH>>/support/c                  */

/* The 'hwut_cursor_t' is a type which is kept inside the generator. It
 * is pasted along the generated code. To avoid exposing it in detail, 
 * a forward decleration is used here.                                       */
struct myGen4_t_tag;

typedef struct myGen4_section_t_tag {
    hwut_cursor_key_t  key_offset;

    void (*init)(struct myGen4_t_tag* it);
    int  (*implement)(struct myGen4_t_tag* it); 
    int  (*is_admissible)(struct myGen4_t_tag* it); 
} myGen4_section_t;



typedef struct myGen4_t_tag {
    /* Internal iterator data _______________________________________________*/
    struct { 
        /* Cursor and section                                                */
        hwut_cursor_t           cursor;
        const myGen4_section_t* section;

        void   (*print)(FILE*, struct myGen4_t_tag*);

        /* Allocate memory for the index array of the cursor directly along  
         * with the memory of the iterator.                                  */
        hwut_cursor_index_t    __memory_index_array[2];
        
    } hwut;

    /* Parameter settings ___________________________________________________*/
    int    x;
    float  y;

} myGen4_t;

/* API ______________________________________________________________________*/

extern void               myGen4_init(myGen4_t* me);

extern int                myGen4_next(myGen4_t* it);

/* Each setting can be associated with a unique scalar key. The transformation
 * from key to setting and from setting to key is done with the subsequent 
 * functions.
 * 
 * The total number of iterations is equal to 'max. key + 1'.                */
extern hwut_cursor_key_t  myGen4_key_max(); 
extern hwut_cursor_key_t  myGen4_key_get(myGen4_t* it);
extern int                myGen4_key_set(myGen4_t* it, hwut_cursor_key_t key);
extern int                myGen4_is_admissible(myGen4_t* it);

/* Print functions for convenience                                           */
/* (No <stdio.h>, then 'FILE*' is 'int*' and functions are dummies.)         */
extern void myGen4_print(FILE* fh, myGen4_t* it);
extern void myGen4_print_table_header(FILE* fh, const char* Separator);
extern void myGen4_print_table_line(FILE* fh, myGen4_t* it, const char* Separator);
extern void myGen4_print_table(FILE* fh, const char* Separator);

#include <stdint.h>

/* This file has been generated with HWUT 0.27.4.
 *___________________________________________________________________________*/
#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
#   include <stdio.h>
#else
    typedef int FILE; /* Required to implement the dummy 'print' functions.  */
#endif

#if ! defined(HWUT_OPTION_ALLOC_FORBIDDEN)
#   include <malloc.h>
#endif

#include <hwut_cursor.h>   /* Use: -I<<HWUT_PATH>>/support/c                  */

/* The 'hwut_cursor_t' is a type which is kept inside the generator. It
 * is pasted along the generated code. To avoid exposing it in detail, 
 * a forward decleration is used here.                                       */
struct myGen2_t_tag;

typedef struct myGen2_section_t_tag {
    hwut_cursor_key_t  key_offset;

    void (*init)(struct myGen2_t_tag* it);
    int  (*implement)(struct myGen2_t_tag* it); 
    int  (*is_admissible)(struct myGen2_t_tag* it); 
} myGen2_section_t;

typedef struct {
    long     length;
    uint32_t data[4];
} myGen2_array_array_t;
typedef struct {
    long  length;
    float data[2];
} myGen2_array_farray_t;


typedef struct myGen2_t_tag {
    /* Internal iterator data _______________________________________________*/
    struct { 
        /* Cursor and section                                                */
        hwut_cursor_t           cursor;
        const myGen2_section_t* section;

        void   (*print)(FILE*, struct myGen2_t_tag*);

        /* Allocate memory for the index array of the cursor directly along  
         * with the memory of the iterator.                                  */
        hwut_cursor_index_t    __memory_index_array[5];
        
    } hwut;

    /* Parameter settings ___________________________________________________*/
    int                          x;
    float                        y;
    const char*                  str;
    const myGen2_array_array_t*   array;
    const myGen2_array_farray_t*  farray;

} myGen2_t;

/* API ______________________________________________________________________*/

extern void               myGen2_init(myGen2_t* me);

extern int                myGen2_next(myGen2_t* it);

/* Each setting can be associated with a unique scalar key. The transformation
 * from key to setting and from setting to key is done with the subsequent 
 * functions.
 * 
 * The total number of iterations is equal to 'max. key + 1'.                */
extern hwut_cursor_key_t  myGen2_key_max(); 
extern hwut_cursor_key_t  myGen2_key_get(myGen2_t* it);
extern int                myGen2_key_set(myGen2_t* it, hwut_cursor_key_t key);
extern int                myGen2_is_admissible(myGen2_t* it);

/* Print functions for convenience                                           */
/* (No <stdio.h>, then 'FILE*' is 'int*' and functions are dummies.)         */
extern void myGen2_print(FILE* fh, myGen2_t* it);
extern void myGen2_print_table_header(FILE* fh, const char* Separator);
extern void myGen2_print_table_line(FILE* fh, myGen2_t* it, const char* Separator);
extern void myGen2_print_table(FILE* fh, const char* Separator);

#include <stdint.h>

/* This file has been generated with HWUT 0.27.4.
 *___________________________________________________________________________*/
#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
#   include <stdio.h>
#else
    typedef int FILE; /* Required to implement the dummy 'print' functions.  */
#endif

#if ! defined(HWUT_OPTION_ALLOC_FORBIDDEN)
#   include <malloc.h>
#endif

#include <hwut_cursor.h>   /* Use: -I<<HWUT_PATH>>/support/c                  */

/* The 'hwut_cursor_t' is a type which is kept inside the generator. It
 * is pasted along the generated code. To avoid exposing it in detail, 
 * a forward decleration is used here.                                       */
struct myGen3_t_tag;

typedef struct myGen3_section_t_tag {
    hwut_cursor_key_t  key_offset;

    void (*init)(struct myGen3_t_tag* it);
    int  (*implement)(struct myGen3_t_tag* it); 
    int  (*is_admissible)(struct myGen3_t_tag* it); 
} myGen3_section_t;



typedef struct myGen3_t_tag {
    /* Internal iterator data _______________________________________________*/
    struct { 
        /* Cursor and section                                                */
        hwut_cursor_t           cursor;
        const myGen3_section_t* section;

        void   (*print)(FILE*, struct myGen3_t_tag*);

        /* Allocate memory for the index array of the cursor directly along  
         * with the memory of the iterator.                                  */
        hwut_cursor_index_t    __memory_index_array[2];
        
    } hwut;

    /* Parameter settings ___________________________________________________*/
    int    x;
    float  y;

} myGen3_t;

/* API ______________________________________________________________________*/

extern void               myGen3_init(myGen3_t* me);

extern int                myGen3_next(myGen3_t* it);

/* Each setting can be associated with a unique scalar key. The transformation
 * from key to setting and from setting to key is done with the subsequent 
 * functions.
 * 
 * The total number of iterations is equal to 'max. key + 1'.                */
extern hwut_cursor_key_t  myGen3_key_max(); 
extern hwut_cursor_key_t  myGen3_key_get(myGen3_t* it);
extern int                myGen3_key_set(myGen3_t* it, hwut_cursor_key_t key);
extern int                myGen3_is_admissible(myGen3_t* it);

/* Print functions for convenience                                           */
/* (No <stdio.h>, then 'FILE*' is 'int*' and functions are dummies.)         */
extern void myGen3_print(FILE* fh, myGen3_t* it);
extern void myGen3_print_table_header(FILE* fh, const char* Separator);
extern void myGen3_print_table_line(FILE* fh, myGen3_t* it, const char* Separator);
extern void myGen3_print_table(FILE* fh, const char* Separator);

#include <stdint.h>

/* This file has been generated with HWUT 0.27.4.
 *___________________________________________________________________________*/
#if ! defined(HWUT_OPTION_STDIO_FORBIDDEN)
#   include <stdio.h>
#else
    typedef int FILE; /* Required to implement the dummy 'print' functions.  */
#endif

#if ! defined(HWUT_OPTION_ALLOC_FORBIDDEN)
#   include <malloc.h>
#endif

#include <hwut_cursor.h>   /* Use: -I<<HWUT_PATH>>/support/c                  */

/* The 'hwut_cursor_t' is a type which is kept inside the generator. It
 * is pasted along the generated code. To avoid exposing it in detail, 
 * a forward decleration is used here.                                       */
struct myGen1_t_tag;

typedef struct myGen1_section_t_tag {
    hwut_cursor_key_t  key_offset;

    void (*init)(struct myGen1_t_tag* it);
    int  (*implement)(struct myGen1_t_tag* it); 
    int  (*is_admissible)(struct myGen1_t_tag* it); 
} myGen1_section_t;

typedef struct {
    long     length;
    uint32_t data[4];
} myGen1_array_array_t;
typedef struct {
    long  length;
    float data[2];
} myGen1_array_farray_t;


typedef struct myGen1_t_tag {
    /* Internal iterator data _______________________________________________*/
    struct { 
        /* Cursor and section                                                */
        hwut_cursor_t           cursor;
        const myGen1_section_t* section;

        void   (*print)(FILE*, struct myGen1_t_tag*);

        /* Allocate memory for the index array of the cursor directly along  
         * with the memory of the iterator.                                  */
        hwut_cursor_index_t    __memory_index_array[1];
        
    } hwut;

    /* Parameter settings ___________________________________________________*/
    int                          x;
    float                        y;
    const char*                  str;
    const myGen1_array_array_t*   array;
    const myGen1_array_farray_t*  farray;

} myGen1_t;

/* API ______________________________________________________________________*/

extern void               myGen1_init(myGen1_t* me);

extern int                myGen1_next(myGen1_t* it);

/* Each setting can be associated with a unique scalar key. The transformation
 * from key to setting and from setting to key is done with the subsequent 
 * functions.
 * 
 * The total number of iterations is equal to 'max. key + 1'.                */
extern hwut_cursor_key_t  myGen1_key_max(); 
extern hwut_cursor_key_t  myGen1_key_get(myGen1_t* it);
extern int                myGen1_key_set(myGen1_t* it, hwut_cursor_key_t key);
extern int                myGen1_is_admissible(myGen1_t* it);

/* Print functions for convenience                                           */
/* (No <stdio.h>, then 'FILE*' is 'int*' and functions are dummies.)         */
extern void myGen1_print(FILE* fh, myGen1_t* it);
extern void myGen1_print_table_header(FILE* fh, const char* Separator);
extern void myGen1_print_table_line(FILE* fh, myGen1_t* it, const char* Separator);
extern void myGen1_print_table(FILE* fh, const char* Separator);

#endif /* INCLUDE_GUAGE_HWUT_GENERATOR_myGen_iterator_h */
