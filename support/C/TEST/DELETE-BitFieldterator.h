#ifndef INCLUDE_GUAGE_HWUT_GENERATOR_BitFieldterator_h
#define INCLUDE_GUAGE_HWUT_GENERATOR_BitFieldterator_h
#include <stdint.h>

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
struct Error_t_tag;

typedef struct Error_section_t_tag {
    hwut_cursor_key_t  key_offset;

    void (*init)(struct Error_t_tag* it);
    int  (*implement)(struct Error_t_tag* it); 
    int  (*is_admissible)(struct Error_t_tag* it); 
} Error_section_t;



typedef struct Error_t_tag {
    /* Internal iterator data _______________________________________________*/
    struct { 
        /* Cursor and section                                                */
        hwut_cursor_t          cursor;
        const Error_section_t* section;

        void   (*print)(FILE*, struct Error_t_tag*);

        /* Allocate memory for the index array of the cursor directly along  
         * with the memory of the iterator.                                  */
        hwut_cursor_index_t    __memory_index_array[1];
        
    } hwut;

    /* Parameter settings ___________________________________________________*/
    uint32_t bit_n1;
    uint32_t bits1;
    uint32_t bit_n2;
    uint32_t bits2;
    uint32_t bit_n3;
    uint32_t bits3;

} Error_t;

/* API ______________________________________________________________________*/

extern void              Error_init(Error_t* me);

extern int               Error_next(Error_t* it);

extern hwut_cursor_key_t Error_key_get(Error_t* it);
extern void              Error_key_set(Error_t* it, hwut_cursor_key_t key);
extern int               Error_is_admissible(Error_t* it);

/* Print functions for convenience                                           */
/* (No <stdio.h>, then 'FILE*' is 'int*' and functions are dummies.)         */
extern void Error_print(FILE* fh, Error_t* it);
extern void Error_print_table_header(FILE* fh, const char* Separator);
extern void Error_print_table_line(FILE* fh, Error_t* it, const char* Separator);
extern void Error_print_table(FILE* fh, const char* Separator);

#include <stdint.h>

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
struct Three_t_tag;

typedef struct Three_section_t_tag {
    hwut_cursor_key_t  key_offset;

    void (*init)(struct Three_t_tag* it);
    int  (*implement)(struct Three_t_tag* it); 
    int  (*is_admissible)(struct Three_t_tag* it); 
} Three_section_t;



typedef struct Three_t_tag {
    /* Internal iterator data _______________________________________________*/
    struct { 
        /* Cursor and section                                                */
        hwut_cursor_t          cursor;
        const Three_section_t* section;

        void   (*print)(FILE*, struct Three_t_tag*);

        /* Allocate memory for the index array of the cursor directly along  
         * with the memory of the iterator.                                  */
        hwut_cursor_index_t    __memory_index_array[3];
        
    } hwut;

    /* Parameter settings ___________________________________________________*/
    uint32_t bit_n1;
    uint32_t bit_n2;
    uint32_t bit_n3;

} Three_t;

/* API ______________________________________________________________________*/

extern void              Three_init(Three_t* me);

extern int               Three_next(Three_t* it);

extern hwut_cursor_key_t Three_key_get(Three_t* it);
extern void              Three_key_set(Three_t* it, hwut_cursor_key_t key);
extern int               Three_is_admissible(Three_t* it);

/* Print functions for convenience                                           */
/* (No <stdio.h>, then 'FILE*' is 'int*' and functions are dummies.)         */
extern void Three_print(FILE* fh, Three_t* it);
extern void Three_print_table_header(FILE* fh, const char* Separator);
extern void Three_print_table_line(FILE* fh, Three_t* it, const char* Separator);
extern void Three_print_table(FILE* fh, const char* Separator);

#include <stdint.h>

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
struct Two_t_tag;

typedef struct Two_section_t_tag {
    hwut_cursor_key_t  key_offset;

    void (*init)(struct Two_t_tag* it);
    int  (*implement)(struct Two_t_tag* it); 
    int  (*is_admissible)(struct Two_t_tag* it); 
} Two_section_t;



typedef struct Two_t_tag {
    /* Internal iterator data _______________________________________________*/
    struct { 
        /* Cursor and section                                                */
        hwut_cursor_t          cursor;
        const Two_section_t*   section;

        void   (*print)(FILE*, struct Two_t_tag*);

        /* Allocate memory for the index array of the cursor directly along  
         * with the memory of the iterator.                                  */
        hwut_cursor_index_t    __memory_index_array[2];
        
    } hwut;

    /* Parameter settings ___________________________________________________*/
    uint32_t bit_n1;
    uint32_t bit_n2;

} Two_t;

/* API ______________________________________________________________________*/

extern void              Two_init(Two_t* me);

extern int               Two_next(Two_t* it);

extern hwut_cursor_key_t Two_key_get(Two_t* it);
extern void              Two_key_set(Two_t* it, hwut_cursor_key_t key);
extern int               Two_is_admissible(Two_t* it);

/* Print functions for convenience                                           */
/* (No <stdio.h>, then 'FILE*' is 'int*' and functions are dummies.)         */
extern void Two_print(FILE* fh, Two_t* it);
extern void Two_print_table_header(FILE* fh, const char* Separator);
extern void Two_print_table_line(FILE* fh, Two_t* it, const char* Separator);
extern void Two_print_table(FILE* fh, const char* Separator);

#include <stdint.h>

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
struct One_t_tag;

typedef struct One_section_t_tag {
    hwut_cursor_key_t  key_offset;

    void (*init)(struct One_t_tag* it);
    int  (*implement)(struct One_t_tag* it); 
    int  (*is_admissible)(struct One_t_tag* it); 
} One_section_t;



typedef struct One_t_tag {
    /* Internal iterator data _______________________________________________*/
    struct { 
        /* Cursor and section                                                */
        hwut_cursor_t          cursor;
        const One_section_t*   section;

        void   (*print)(FILE*, struct One_t_tag*);

        /* Allocate memory for the index array of the cursor directly along  
         * with the memory of the iterator.                                  */
        hwut_cursor_index_t    __memory_index_array[1];
        
    } hwut;

    /* Parameter settings ___________________________________________________*/
    uint32_t bit_n1;

} One_t;

/* API ______________________________________________________________________*/

extern void              One_init(One_t* me);

extern int               One_next(One_t* it);

extern hwut_cursor_key_t One_key_get(One_t* it);
extern void              One_key_set(One_t* it, hwut_cursor_key_t key);
extern int               One_is_admissible(One_t* it);

/* Print functions for convenience                                           */
/* (No <stdio.h>, then 'FILE*' is 'int*' and functions are dummies.)         */
extern void One_print(FILE* fh, One_t* it);
extern void One_print_table_header(FILE* fh, const char* Separator);
extern void One_print_table_line(FILE* fh, One_t* it, const char* Separator);
extern void One_print_table(FILE* fh, const char* Separator);

#endif /* INCLUDE_GUAGE_HWUT_GENERATOR_BitFieldterator_h */
