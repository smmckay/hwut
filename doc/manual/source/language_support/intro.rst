Programming Language Support
----------------------------

While HWUT is designed to support any programming language that is able to
produce an application that can be executed from the command line and print
something on the standard output, HWUT comes with some specific support for
several programming languages. This section outlines auxiliaries that may
facilitate the implementation of test applications. 

All language specific support is located in the directory
'$HWUT_PATH/support/X' where 'X' is the name of the specific programming
language.

Choices
.......

HWUT's interaction with the test applications is based on command 
line arguments. HWUT provides a means to check them elegantly
using the macro ``hwut_choice``. By means of this macro the 
following code fragment

  .. code-block:: c

    int main(int argc, char** argv)
    {
        uint8_t*  test_string = 0x0;

        if( argc > 1 )
            if( strcmp(argv[1], "--hwut-info") == 0 ) {
                printf("My String Function Test\n");
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
        // test on 'test_string' 
        ...
    }

can be transformed into

  .. code-block:: c

    #include "hwut_unit.h"

    int main(int argc, char** argv)
    {
        uint8_t*  test_string = 0x0;

        hwut_info("My String Function Test;\n"
                  "CHOICES: 7bit, 8bit, 16bit, 32bit;");
        hwut_choice("7bit",  test_string = create_7bit_encoded_example()  );
        hwut_choice("8bit",  test_string = create_8bit_encoded_example()  );
        hwut_choice("16bit", test_string = create_16bit_encoded_example() );
        hwut_choice("32bit", test_string = create_32bit_encoded_example() );

        // test on 'test_string' 
        ...
    }

which is at the same time shorter and more readable. The formal syntax of
the ``hwut_choice`` macro is 

   .. c:macro:: hwut_choice(CHOICE, STATEMENT)

      where ``CHOICE`` is the string against which command line argument '1' 
      is checked. ``STATEMENT`` is the statement to be executed if the first
      argument is equal to ``CHOICE``.

and the formal syntax of the ``hwut_info`` macro is 

   .. c:macro:: hwut_info(MESSAGE)

      where ``MESSAGE`` is the string to be reported as a response to the 
      command line argument ``--hwut-info``.

NUnit-Like Testing
..................

At the time of this writing there is a pre-dominant tool for unit testing
called 'NUnit'. With this tool tests are based on function calls like
``Assert.AreEqual(This, That)``. This is manytimes very inconvenient
when doing larger tests on system behavior. For 'real' unit tests that
are restricted to single function calls and what they return such tests
may be appropriate. HWUT provides a very simple means to support such tests
by the ``hwut_verify_verbose`` macro in 'C/C++'. It can be accessed by including

  .. code-block:: c

      #include <hwut_unit.h>

This macro allows to check for
expressions of any complexity in the syntax of C itself. For example:

  .. code-block:: c
     
      hwut_verify_verbose( 1 + 1 == 2 );
      hwut_verify_verbose( 1 + 1 == 3 );

results in the output::

      test-hwut_unit.c:      [OK] 1 + 1 == 2
      test-hwut_unit.c:24: [FAIL] 1 + 1 == 3

Note, that the line number is only output when the test fails. This prevents
that HWUT's plain comparison fails when only the position of tests changes
inside the file. If it is desired to print out a comment along with the 
test, then the macro ``hwut_verify_verbose`` may be used, e.g.

  .. code-block:: c
     
     hwut_verify_verbose("----------------------------\n" 
                  "One plus one is two, or not?\n"
                  1 + 1 == 2);

which results in::

     One plus one is two, or not?
     ----------------------------
     test-hwut_unit.c:      [OK] 1 + 1 == 2
     
If it is only required to print out errors, then the silent version ``

  .. code-block:: c
     
     hwut_verify( 1 + 1 == 2 );
     hwut_verify( 1 + 1 == 3 );
     hwut_averify("------------------------------------\n"           
                         "Silent: One plus one is two, or not?"
                         1 + 1 == 2);
                         
     hwut_averify("-------------------------------------------\n"
                         "Silent: One plus one is not three, or what?"
                         1 + 1 == 3);

results in the following output, where obviously the successful tests 
are not printed anymore::

     test-hwut_unit.c:24: [FAIL] 1 + 1 == 3
     -----------------------------------
     One plus one is not three, or what?
     test-hwut_unit.c:    [FAIL] 1 + 1 == 3
     
The formal specification of the macros for NUnit like testing is

   .. cmacro:: hwut_verify_verbose(CONDITION)

      Tests for ``CONDITION`` to me met. Dependent on the result it
      prints an OK message or a FAIL message on the screen. If it 
      fails, the place where the failure occured is printed on the 
      screen.

   .. cmacro:: hwut_verify(CONDITION)

      acts like ``hwut_verify_verbose`` but prints only in case of failure.


   .. cmacro:: hwut_verify_verbose(ANNOTATION, CONDITION)
   
      which is the 'annotated' version of ``hwut_verify_verbose`` that prints 
      the message ``ANNOTATION`` before the condition is checked.


   .. cmacro:: hwut_averify(ANNOTATION, CONDITION)

      acts like ``hwut_verify_verbose`` but prints only in case of failure.

The explicit test for equal, not equal, greater than, etc. becomes redundant
since with the ``hwut_verify_verbose`` macros all kinds of expressions can be tested. 
The complexity of its conditions is only restricted by the restrictions of 
the C-language.

In C, the abort upon error can be prevented by the definition of the command
line macro::

              HWUT_OPTION_CONTINUE_ON_FAIL

If defined, then hwut will continue processing after a verify-test failed.
    

Bit Fields
..........

Reading and writing bits can be particularily hard. To support the encoding and
decoding on a bit basis, hwut provides the ``hwut_bitfield`` functions.  The
header "hwut_bitfield.h" must be included in order to access the functionality.
The two functions for encoding and decoding are 

.. code-block:: cpp

   int hwut_bitfield_encode(array, ArraySize, ...);
   int hwut_bitfield_decode(array, ArraySize, ...);

They both receive a pointer to an array and its size in front of a variable
argument list. In order to write, for example, a 3 bit value ``a``, followed by
a six bit value ``b``, followed by a value ``c`` of 7 bit, one must call

.. code-block:: cpp

       uint8_t   array[2];

       //  Frame: |...|......|.......|
       //           a     b      c
       hwut_bitfield_encode(my_array, 2, 3, a, 6, b, 7, c, -1);

The first argument is the array, the second the size of the array in bytes. Then, 
the 3 tells that the next value occuppies three bit. The 6 tells about the next 
value occupying six bit and 7 tells that the value ``c`` needs to be placed on 
7 bit. The -1 is a terminator that tells that the list has ended. Similarly, 
such a frame can be decoded by

.. code-block:: cpp

       hwut_bitfield_decode(my_array, 2, 3, &a, 6, &b, 7, &c, -1);

The call only differs in its arguments by passing pointers to variables which
shall contain the content. That is, when this function is called, the content
of the first three bits is going to be placed ``a``, the next six bit are placed
in ``b`` and the last seven bits are placed in ``c``. Again, the -1 serves as 
a terminator.

Additionally, for printing the following functions are provided which work
exactly the same way as the encoders and decoders.

.. code-block:: cpp

    void hwut_bitfield_print_bytes(uint8_t* array, size_t ArraySize);
    void hwut_bitfield_print_dec(uint8_t* array, size_t ArraySize, ...);
    void hwut_bitfield_print_numeric(uint8_t* array, size_t ArraySize, 
                                     const int Base, ...);
    void hwut_bitfield_print_borders(uint8_t* array, size_t ArraySize, ...);

