#ifndef INCLUDE_GUARD_HWUT_UNIT
#define INCLUDE_GUARD_HWUT_UNIT


#if defined(__cplusplus)
#   include <cstdio>
#   include <cstring>
#   include <cstdlib>
#   define  hwut_printf     std::printf
#   define  hwut_flush()    std::fflush(stdout)
#else
#   include <stdio.h>
#   include <string.h>
#   include <stdlib.h>
#   define  hwut_printf     printf
#   define  hwut_flush()    fflush(stdout) 
#endif

#define hwut_exit() do { hwut_flush(); exit(0); } while(0)

#if defined(HWUT_OPTION_CONTINUE_ON_FAIL)
#   define hwut_on_failure() hwut_flush() /* nothing to be done */
#else
#   define hwut_on_failure() hwut_exit()
#endif

#define hwut_info(MESSAGE) \
    if( argc >= 2 && strcmp(argv[1], "--hwut-info") == 0 ) { \
        hwut_printf(MESSAGE);                                \
        hwut_exit();                                         \
    } 

#define hwut_choice(CHOICE_NAME, EXPRESSION) \
	do { if( (argc < 2) || (strcmp(argv[1],CHOICE_NAME)==0) ) { EXPRESSION; } } while(0)

#define hwut_if_choice(CHOICE_NAME) \
	if( (argc < 2) || (strcmp(argv[1],CHOICE_NAME)==0) )

/* In the 'good' case, no line numbers are printed. This is to avoid that
 * a simple line number shift causes all tests to fail.                    */
#define  hwut_report_ok(MSG)                                          \
         do {                                                         \
             hwut_printf("%s:     ", (const char*)__FILE__);          \
             if     ( (int)__LINE__ < 10 )    ;                       \
             else if( (int)__LINE__ < 100 )   hwut_printf(" ");       \
             else if( (int)__LINE__ < 1000 )  hwut_printf("  ");      \
             else if( (int)__LINE__ < 10000 ) hwut_printf("   ");     \
             else                             hwut_printf("    ");    \
             hwut_printf("[OK] %s\n", MSG);                           \
             hwut_flush();                                            \
         } while( 0 )

#define  hwut_report_fail(MSG) \
         do {                  \
             hwut_printf("%s:%i: [FAIL] %s\n", (const char*)__FILE__, (int)__LINE__, MSG); \
             hwut_flush();                                                                 \
         } while(0)

#define  hwut_report_annotation(MSG) \
         do {                        \
             hwut_printf(MSG "\n");  \
             hwut_flush();           \
         } while(0)

#define hwut_verify(CONDITION)          \
        do {                                   \
            if( ! (CONDITION) ) {              \
                hwut_report_fail(#CONDITION);  \
                hwut_on_failure();             \
            }                                  \
        } while(0)

#define hwut_verify_verbose(CONDITION) \
        do {                                                                     \
            if( CONDITION ) { hwut_report_ok(#CONDITION);   hwut_flush(); }      \
            else            { hwut_report_fail(#CONDITION); hwut_on_failure(); } \
        } while(0)

#define hwut_averify(ANNOTATION, CONDITION)  \
        do {                                        \
            if( ! (CONDITION) ) {                   \
                hwut_report_annotation(ANNOTATION); \
                hwut_report_fail(#CONDITION);       \
                hwut_on_failure();                  \
            }                                       \
        } while(0)

#define hwut_averify_verbose(ANNOTATION, CONDITION)                    \
        do {                                                   \
            hwut_report_annotation(ANNOTATION);                \
            if( CONDITION ) { hwut_report_ok(#CONDITION);   hwut_flush(); }      \
            else            { hwut_report_fail(#CONDITION); hwut_on_failure(); } \
        } while(0)

/* Application: Generator/Iterators ___________________________________________
 *                                                                           */
#define  hwut_report_it_fail(it, MSG) \
         do {                  \
             hwut_printf("%s:%i: [FAIL] %s {\n", (const char*)__FILE__, (int)__LINE__, MSG); \
             (it)->hwut.print(stdout, (it));                                                          \
             hwut_printf("%s", "}\n");                                                       \
             hwut_flush();                                                                   \
         } while(0)

#define hwut_verify_it(it, CONDITION)      \
        do {                                      \
            if( ! (CONDITION) ) {                 \
                hwut_report_it_fail((it), #CONDITION);  \
                hwut_on_failure();                \
            }                                     \
        } while(0)

#define hwut_verify_verbose_it(it, CONDITION) \
        do {                                                                        \
            if( CONDITION ) { hwut_report_ok(#CONDITION);      hwut_flush(); }      \
            else            { hwut_report_it_fail((it), #CONDITION); hwut_on_failure(); } \
        } while(0)

#define hwut_averify_it(it, ANNOTATION, CONDITION)  \
        do {                                               \
            if( ! (CONDITION) ) {                          \
                hwut_report_annotation(ANNOTATION);        \
                hwut_report_it_fail(it, #CONDITION);       \
                hwut_on_failure();                         \
            }                                              \
        } while(0)

#define hwut_averify_verbose_it(it, ANNOTATION, CONDITION)                               \
        do {                                                                     \
            hwut_report_annotation(ANNOTATION);                                  \
            if( CONDITION ) { hwut_report_ok(#CONDITION);   hwut_flush(); }      \
            else            { hwut_report_it_fail(it, #CONDITION); hwut_on_failure(); } \
        } while(0)

/* Application: Generator/Sm Walker ___________________________________________
 *                                                                           */
#define  hwut_report_walk_fail(walker, MSG) \
         do {                                                                                \
             hwut_printf("%s:%i: [FAIL] %s {\n", (const char*)__FILE__, (int)__LINE__, MSG); \
             hwut_sm_walker_print(stdout, (walker), 80);                                     \
             hwut_printf("%s", "}\n");                                                       \
             hwut_flush();                                                                   \
         } while(0)

#define hwut_verify_walk(walker, CONDITION)                          \
        do {                                                         \
            if( ! (CONDITION) ) {                                    \
                hwut_report_walk_fail(&(walker)->base, #CONDITION);  \
                hwut_on_failure();                                   \
            }                                                        \
        } while(0)

#define hwut_verify_verbose_walk(walker, CONDITION) \
        do {                                                                                  \
            if( CONDITION ) { hwut_report_ok(#CONDITION);                         hwut_flush(); }      \
            else            { hwut_report_walk_fail(&(walker)->base, #CONDITION); hwut_on_failure(); } \
        } while(0)

#define hwut_averify_walk(walker, ANNOTATION, CONDITION)            \
        do {                                                        \
            if( ! (CONDITION) ) {                                   \
                hwut_report_annotation(ANNOTATION);                 \
                hwut_report_walk_fail(&(walker)->base, #CONDITION); \
                hwut_on_failure();                                  \
            }                                                       \
        } while(0)

#define hwut_averify_verbose_walk(walker, ANNOTATION, CONDITION)                                       \
        do {                                                                                           \
            hwut_report_annotation(ANNOTATION);                                                        \
            if( CONDITION ) { hwut_report_ok(#CONDITION);                         hwut_flush(); }      \
            else            { hwut_report_walk_fail(&(walker)->base, #CONDITION); hwut_on_failure(); } \
        } while(0)

#endif  /* INCLUDE_GUARD_HWUT_UNIT */



