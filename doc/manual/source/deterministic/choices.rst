Choices
=======

Often the same test program is applied with only one or few parameters changed.
Someone might have a parsing function that works on 7, 8, 16 and 32 bit encoded
Unicode characters. The functions may be the same and so are the testing
functions. The only requirement is use different encodings for one and the same
test.  Here, _choices_ come handy. HWUT is able to pass an 'choice' string of
a list of possible choices to a test program. The test program can then decide
based on the command line argument what test to run.  To be able to do so, HWUT
must know what the choices for a program are, and thus, the program needs to
report them when it is called with `--hwut-info` as first argument. HWUT
requires to report the choices after a `CHOICES:` keyword, where the different
choices are comma separated. For the example mentioned above the response to
`--hwut-info` in C might be produced by a code fragment like this: 

.. code-block:: c

    ...
    int main(int argc, char** argv)
    {
        uint8_t*  test_string = 0x0;

        if( argc > 1 )
            if( strcmp(argv[1], "--hwut-info") == 0 ) {
                printf("My String Function Under Heavy Test\n");
                printf("CHOICES: 7bit, 8bit, 16bit, 32bit");
                return 0;
            }
            elif( strcmp(argv[1], "7bit") == 0 ) {
                test_string = create_7bit_encoded_example();
            }
            elif( strcmp(argv[1], "8bit") == 0 ) {
                test_string = create_8bit_encoded_example();
            }
            elif( strcmp(argv[1], "16bit") == 0 ) {
                test_string = create_16bit_encoded_example();
            }
            elif( strcmp(argv[1], "32bit") == 0 ) {
                test_string = create_32bit_encoded_example();
            }
        }
        /* test on 'test_string' */
        ...
    }

In the subdirectory './support/C/' there is a file ``hwut_unit.h``` which
contains useful macros. One of them is the macro ``hwut_choice`` which 
allows to express the choices more elegantly. The above code fragment
could be rewritten as follows:

.. code-block:: c

    #include "hwut_unit.h"

    int main(int argc, char** argv)
    {
        uint8_t*  test_string = 0x0;

        hwut_choice("--hwut-info", {
            printf("My String Function Under Heavy Test\n");
            printf("CHOICES: 7bit, 8bit, 16bit, 32bit");
            return 0;
        }):
        hwut_choice("7bit",  test_string = create_7bit_encoded_example()  );
        hwut_choice("8bit",  test_string = create_8bit_encoded_example()  );
        hwut_choice("16bit", test_string = create_16bit_encoded_example() );
        hwut_choice("32bit", test_string = create_32bit_encoded_example() );

        /* test on 'test_string' */
        ...
    }

This representation is more convenient to read and provides a quick
overview over all test choices.
   
The storage of results and the result reporting will now include the choices
passed to a given test program. Note, however, that this feature does not
directly support compile options. For C programs, for example, it should be
common practice to test with and without the `NDEBUG` macro defined. Otherwise,
panic might come up as soon as a program is run at full speed and errors
pop out of nowhere, only because some assert commands or `#ifndef
NDEBUG` commands have been written carelessly. 

An elegant way to deal with compile options is to put the makefile into
another directory (other than `TEST`) and then initiate the compile process
from a shell script that is located in the TEST directory. For the quex
project this technique is applied to compile the tests for the demo
programs. A shell script that initiates the compilation process and starts
the test program looks for example like this:

.. code-block:: bash

    #! /usr/bin/env bash
    if [[ $1 == "--hwut-info" ]]; then
        echo "demo/002: Indentation Based Scopes;"
        echo "CHOICES:  NDEBUG, DEBUG;"
        exit
    fi
    source core.sh 002 $1

where the script `core.sh` on which it relies is used by all test programs.
It initiates the compilation and runs the test and ensures that the
standard output is delivered as desired. It receives the directory
where to find the makefile as a first argument and the compile
option as a second argument. In principle such a shell script
looks like this:

.. code-block:: bash

    cd $1 
    if [[ $2 == "NDEBUG" ]]; then
        arg1="NDEBUG_F=-DNDEBUG"
    else
        arg1="NDEBUG_F= "
    fi
    # Making relying on 'my-makefile.mk'
    make -f my.mk $arg1 >& /dev/null
    # Executing
    ./test-program

Note, that is sets the `NDEBUG` flag according to the choice which was chosen
for the test program. 
