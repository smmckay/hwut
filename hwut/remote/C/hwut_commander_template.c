void example_function_1(const char*);
void example_function_2(const char*);
void example_function_3(const char*);

/* hwut_db: The database that maps from application name to function pointer.
 *          The functions take as a first argument a 'char*' which is a string
 *          containing the first argument-similar to what happens on the 
 *          command line on 'real' operating systems.                           */
type struct { 
    const char* application;
    void        (*function)(const char*);
} hwut_test_db_element;

#define HWUT_DB_SIZE (unsigned)3
hwut_test_db_element  hwut_db[HWUT_DB_SIZE] = {

    {"example-1", example_function_1, }
    {"example-2", example_function_2, }
    {"example-3", example_function_3, }

};

int
hwut_is_equal(const char* Str1, const char* Str2)
{
    const char* p1 = 0, p2 = 0;
    for(p1=Str1, p2=Str2; *p1 == *p2 ; ++p1, ++p2) {
        if( *p1 == '\0' ) return 1;
    }
    return 0;
}

void
hwut_route(const char* Message)
{
    hwut_test_db_element* iterator          = 0x0;
    hwut_test_db_element* End               = hwut_db + HWUT_DB_SIZE;
    char*                 miterator         = 0x0;
    char*                 application_end_p = 0x0;
    char*                 argument_begin_p  = 0x0;

    /* Separate the message into 'application' and 'argument' */
    /* -- Delete preceeding whitespace */
    for(miterator = Message; *miterator == ' ' || *miterator == '\t' ; ++miterator) {
        if( *miterator == '\0' ) return; /* premature terminating zero */
    }
    /* -- Find end of application name */
    for(; *miterator != ' ' && *miterator != '\t' && *miterator != '\0'; ++miterator)
    application_end_p = miterator;
    /* -- Find begin of argument name (may be of zero size). */
    for(; *miterator == ' ' || *miterator == '\t' || *miterator == '\0'; ++miterator);
    argument_begin_p = miterator;
    /* (Assume that the argument extends from the 'argument_begin_p' to the place of 
     *  the terminating zero. HWUT only sends commands with at most one argument.)   */

    /* Find the function pointer that belongs to the application */
    for(iterator = hwut_db; iterator != End; ++iterator) { 
        /* Compare database key and 'application name'. Do not rely on strcmp() to reduce 
         * required resources. */
        if( hwut_is_equal(iterator->application, application_end_p) ) { 
            (*iterator->function)(argument_begin_p);
            return;
        }
    }

}

void example_function_1(const char* Arg)
{ 
    hwut_spy_open(); 
    hwut_spy_print("function 1: "); 
    hwut_spy_print(Arg); 
    hwut_spy_close(); 
}

void example_function_2(const char* Arg)
{ 
    hwut_spy_open(); 
    hwut_spy_print("function 2: "); 
    hwut_spy_print(Arg); 
    hwut_spy_close(); 
}

void example_function_3(const char* Arg)
{ 
    hwut_spy_open(); 
    hwut_spy_print("function 3: "); 
    hwut_spy_print(Arg); 
    hwut_spy_close(); 
}


