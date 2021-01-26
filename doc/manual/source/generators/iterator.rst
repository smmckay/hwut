Iterators
=========

TODO: Mention 'hwut_random_next()' which generates a deterministic sequence
      of random numbers platform independently. Numbers = 0 .. 2**31 - 11.

An iterator is a description which allows to define a larger sets of tests.
Instead of defining every combination of a parameter setting manually, 
generators provide iterators over permutation sets. For that HWUT generates
code which allows users to apply 'iterators' to iterate over their parameter
settings. 

In C an iterator may be used as follows:

.. code-block::cpp

   myIterator_t* it = myIterator_new();  // Initialize the iterator.         

   while( myIterator_next(it) ) {        // Loop while there is more.
       ...
       r = myfunc(it->x, it->y);         // Do something with parameters given    
       assert(r == it->result);          // by the current setting of 'it'.
       ...
   }

Generators are specified in text files (or in comments of actual source code).
Each parameter that appears in a setting must be specified along with the
set of possible values that it may take.  For statically typed languages the 'type'
must be specified along. The simplest case is an iteration over constant
values. In this case the specification of a iterator basically a 'CSV' file
content such as

.. code-block:: csv

   int x;  int y; char* my_string;  
       0;      1;         "hello";  
       0;      0;         "hello";
      10;      1;         "hello";
      10;      0;         "hello";
       0;      1;       "bonjour";  
       0;      0;       "bonjour";
      10;      1;       "bonjour";
      10;      0;       "bonjour";

The header line describes the parameters, namely ``x``, ``y``, and
``my_string``. What preceedes their names are their types. All following lines
describe the settings of those parameters. A generated iterator ``it`` in C may
then reproduce the content of this table easily by

.. code-block:: cpp

       myIterator_t* it = myIterator_new();

       while( myIterator_next(it) ) {
           printf("%i; %i; \"%s\";", it->x, it->y, it->my_string);
       }
   
Real tests may use the parameters provided by ``it`` to do some serious
testing. The syntax of 'selections' may be used to define a set of values for a
parameter to chose. Selections are defined as comma separated lists of values
surrounded by ``[`` and ``]`` brackets. Using selections the aforementioned 
example shrinks down to 

.. code-block:: csv

   int x;  int y;       char* my_string;  
  [0,10];  [0,1];  ["hello", "bonjour"];

This means that ``x`` can take the values 0 and 10, ``y`` can take the
values 0 and 1, and ``my_string`` can be set to ``"hello"`` and ``"bonjour"``.
HWUT automatically iterates over all permutations of theses settings without
changing any line in the code that uses the iterator. 

Every line following the header line is a permutation specification.  HWUT can
provide iterators that seeminglessly iterate over multiple permutation sets.
For example, consider to test a function that tells whether the product of two
numbers is even or odd.  Math tells us that if a number is multiplied with an
even number, then the result is even, if both operands are odd, the result is
odd. 

.. code-block:: cpp

  int x;          int y;           bool even;
  ## Odd  x Odd  => Odd
  [1,3,5,7,9];    [1,3,5,7,9];     false;   
  ## Even x Odd  => Even
  [0,2,4,6,8,10]; [1,3,5,7,9];     true;    
  ## Odd  x Even => Even
  [1,3,5,7,9];    [0,2,4,6,8,10];  true;    
  ## Even x Even => Even
  [0,2,4,6,8,10]; [0,2,4,6,8,10];  \
                                   true;    

Each of the four lines after the header line describes a iterator. Lines
starting or ending with ``##`` are comment lines and semantically ignored.  The
backslash ``\`` allows to continue a line after line break, as shown in the
last line of the fragment.  Since the numbers for ``x`` and ``y`` in the first
line are all odd, it can be said that any permutation of them results in
products which are odd. All other iterators result in products which are even.
The test code in C would be

.. code-block:: cpp

       myIterator_t   it;

       while( myIterator_next(it) ) {
           assert( product_is_even(it->x, it->y) == it->result );
       }
   
The above table is a transparent description of a large number of tests,
namely: 5x5 + 6x5 + 5x6 + 6x6 = 121 tests. Ranges may be used to make 
things even more concise. They are expressions following the pattern::

          |first:last|
          |first:last| step Delta

where ``first`` is a numeric value that defines the first number in the range
and ``last`` defines the last number in the range. Optionally, the step size may
be specified following the keyword ``step``. 

.. code-block:: cpp

     int x;          int y;         bool even;
  ## Odd           * Odd            => Odd
     |1:9| step 2;   |1:9| step 2;  false;     
  ## Even          * Anything       => Even
     |0:10| step 2;  |0:10|;        true;      
     |0:10|;         |0:10| step 2; true;      

The ranges may contain trivial numeric expressions in order to specify
dependencies. For example:

.. code-block:: cpp

     int x;          int y;         
     |0:99|;     |x+1:100|;

tells that ``x`` is combined with all ``y`` greater than ``x`` while
``x+y`` is equal to 100. That is, a trivial expression as a range border
may have the form::

        identifier operator number

where the operator may be ``+`` for addition, ``-`` for subtraction, ``*`` for
multiplication, or ``/`` for division. 

.. warning::

   The trivial expression used in ranges is of the type of the parameter
   which it feeds.

If a parameter ``y`` is of type ``unsigned`` and defined to be in the range
``|x-1:x+1|`` then this might cause issues, in case that ``x`` can be zero. 

Trivial numeric expressions in ranges may be used, for example to define
a parameter's value in the vicinity of another parameter's value. In order to
remain in a certain border a *cut range*. For example::

        
     int x;                        int y;         
     |0:0xFF|;     |x-1:x+1| in |0:0xFF|;

defines that ``x`` is combined with settings of ``y`` where ``y`` is one less, 
equal and one larger than ``x``. However, the cut range ``|0:0xFF|`` ensures
that no combination is produced where ``y`` is less than zero or greater than
0xFF. 

The next two sections discuss in detail the types of parameters and the way
that ranges can be specified. The following table summarizes the different way
to define possible parameter values.

    +--------------------------+----------------------+---------------------------+
    |                          | Syntax Example       |  Meaning                  |
    +==========================+======================+===========================+
    | Selection                | ``[3,5,6, ...]``     |  Any value from ``3``,    |
    |                          |                      |  ``5``, ``6``, ...        |
    +--------------------------+----------------------+---------------------------+
    | Range                    | ``|3:7|``            |  Numbers from ``3``       | 
    |                          |                      |  to ``7`` including       |
    |                          |                      |  ``3`` and ``7``. Numbers |
    |                          |                      |  have a distance of 1.    |
    +--------------------------+----------------------+---------------------------+
    | ... with step size       | ``|3:7| step 2``     |  Like previous where      | 
    |                          |                      |  numbers have a distance  |
    |                          |                      |  of ``2``.                |
    +--------------------------+----------------------+---------------------------+
    | ... with references      | ``|x-1:y|``          |  Numbers at ``x-1`` until | 
    |                          |                      |  ``y``.                   |
    +--------------------------+----------------------+---------------------------+
    | ... with limits          | ``|x-1:y| in |0:2|`` |  Like previous, but       | 
    |                          |                      |  numbers lie in between   |
    |                          |                      |  zero to two.             |
    +--------------------------+----------------------+---------------------------+
    | ... with references,     | ``|x-1:y| in |0:2|`` |  Like previous where      | 
    | limits, and step size.   | ``step 0.1``         |  numbers have a distance  |
    |                          |                      |  of 0.1 between each      | 
    |                          |                      |  other.                   |
    +--------------------------+----------------------+---------------------------+

.. note::

   Some elegant constants in line

     a set of tests quite well define.

   A nicer choice for your collection 

     comes with the feature called 'selection'.

   And, to avoid much hokus pocus

     instruct your par'meters to 'focus'.
   

Value Types
===========

HWUT defines elementary types to describe parameter values. Those value types
are HWUT-intern and not directly related to the concrete types as they are
mentioned in the header line of the iterator description.  The value of a
parameter will be *squeezed* into the parameter's concrete type once code is
generated.  

The HWUT value types are the following:

.. describe:: INTEGER

   Values of positive and negative integers. Accepted integer formats
   are

    +-------------------+---------------------+-----------------------+
    | Numeric Base      | Pattern             | Example               |
    +===================+=====================+=======================+
    | Decimal           | ``[0-9]+``          | 4711                  |
    +-------------------+---------------------+-----------------------+
    | Hexadecimal       | ``0x[0-9a-fA-F.]+`` | 0xC0.FFEE.BABA        |
    +-------------------+---------------------+-----------------------+
    | Octal             | ``0o[0-9a-fA-F.]+`` | 0o731                 |
    +-------------------+---------------------+-----------------------+
    | Binary            | ``0b[0-1.]+``       | 0b111.0100.1.10.101   |
    +-------------------+---------------------+-----------------------+

   The '.' may be used in prefixed numbers as a redundant marker to help
   reading the number itself. This comes handy in larger bit frames for
   examples, where it would be difficult otherwise to identify specific
   bits.

   INTEGER values can be used as constants, in selections, in ranges, and in
   focus ranges. 

.. describe:: FLOAT

   A FLOAT is a finite number of digits following the decimal
   point. In the description of INTEGER the '.' has been disallowed 
   as marker. This happened because the '.' following the decimal number
   pattern results in the FLOAT pattern. 

   Example::

                             0.815

   FLOAT values can be used as constants, in selections, in ranges, and 
   in focus ranges. 

.. describe:: STRING

   A sequence of characters in ``"`` quotes is interpreted as a string.
   A backslashed ``"`` is replaced by a quote. A backslashed backslash 
   is replaced by a backslash.

   Example::

                         "Hello World!"

   STRING values can only be used as constants and in selections.

.. describe:: IARRAY

   An array is a sequence of integers bracket by ``{`` and
   ``}`` brackets. Elements of the array are separated by commas. 

   Example::

                    { 0x01, 0x04, 0xFE, 0xE4 }

   IARRAY objects can only be used as constants and in selections.

   When a variable is of type IARRAY, then its content is accessed
   by to sub-members. For a example a member 'array' can be accessed
   via::

           &it->my_array.data[0]     // --> pointer to the array
           it->my_array.length

.. describe:: FARRAY

   An array is a sequence of floats. They follow the syntax of IARRAY
   except that the numbers in brackets are floats.

   Example::

             { 3.14159, 2.71828, 1.61803, 2.58498 }


   FARRAY objects can only be used as constants and in selections.
   Accessing FARRAY-s happens in the same way as for IARRAY-s.

.. note::

    INTEGER, STRING, and also FLOAT

     allow your scalars to promote.

    If arrays enter then the play
   
     embrace IARRAY and F-ARRAY!

    Those names you talk then a la mode

     but never write them in your code.

The terms INTEGER, FLOAT, STRING, IARRAY, FARRAY never appear in any iterator
specification. A parameter's type is determined through their pattern and
syntax. So, the user needs somehow be aware about what type is his specifying.
    

Minimalist Example
==================

This section provides a complete example using generators in C. It is a good
idea to keep the iterator definition in the test file, so that all test
related data is in one place. The iterator code must be setup in a region
which is semantically indifferent to the compiler.  This can be a long ``/*``
to ``*/`` comment or a region spun by ``#if 0`` and ``#endif``. Consider the
following file ``test-it.c``

.. code-block:: cpp

    #if 0 
    <<hwut-iterator:  myIterator>> 
    ------------------------------------------------------------------------
    #include <stdint.h>
    ------------------------------------------------------------------------
        int Case;         int x;         int y; 
               0;  |1:9| step 2;  |1:9| step 2;
               1; |0:10| step 2;        |0:10|;
    ------------------------------------------------------------------------
    #endif  

    #include "hwut_unit.h"
    #include "myIterator.h"

    int main(int argc, char** argv) 
    {
        myIterator_t it;

        hwut_info("Check product of even and odd;");

        myIterator_init(&it);

        while( myIterator_next(&it) ) {
            if( it->Case == 0 ) {
               // Odd x Odd == Odd 
               assert( my_product(it->x, it->y) % 2 != 0 );
            } else if( it->Case == 0 ) {
               // Even x Anything == Even 
               assert( my_product(it->x, it->y) % 2 == 0 );
               assert( my_product(it->y, it->x) % 2 == 0 );
            }
        }
    }

The marker ``<<hwut-iterator: myIterator>>`` tells the parser that from here on a
iterator definition follows. Calling hwut with::

   > hwut gen test-it.c -o myIterator

defines the file stem of the output files to be ``myIterator``. The section
following the first dashed line contains source code to be pasted into the
iterator header iterator. What follows the second dashed line is the
definition of the iterator sections. The last dashed line signalizes the end
of the iterator. Precisely an iterator definition consists of the following 
elements:

   # A ``<<hwut-iterator ...>>`` tag.

   # A dashed line.

   # Some source header content to be pasted in from of the iterator's header.

   # A dashed line. 

   # The iterator definition consisting of:

       # A header line defining the name of the elements and possibly their type.

       # A list of lines which define permutation sections.

   # A dashed line.

Multiple iterators may be specified in the same file. For this, simply a new
``<<<hwut-iterator ...>>`` tag appear somewhere else--followed by the
aforementioned sequence of definitions.

.. note::

    There is a family of ``hwut_verify_verbose_it...``-functions which take use of 
    the iterators. They check a condition and print the setting of the 
    iterator directly, in case of error. Namely, those functions are::

          hwut_verify_verbose_it(it, condition);
          hwut_verify_it(it, condition);
          hwut_verify_verbose_it(it, annotation, condition);
          hwut_verify_it(it, annotation, condition);

    All functions expect a pointer to an iterator as first argument. The
    ``condition`` argument specifies the condition to be tested. The
    ``annotation`` is some additional message to be printed on screen when this
    test is considered. They are good candidates to replace the ``assert``
    statements during the test.

    If a particular test failed and needs to be investigated the function
    '_key_set()' comes handy. In fact, it may make sense to setup tests as in
    the following code fragment.

    .. code-block:: cpp

            #   if 1              
                while( Setup_next(&it) ) {
                    self_test(&it); 
                    count_n += 1;
                }
            #   else
                assert(Setup_key_set(&it, 19)); // .key upon error was = 19
                self_test(&it); 
            #   endif

    If the test fails and the hwut verifiers report a iterator key, then the 'if 1'
    may be turned into 'if 0' and the key may be set according to the reported
    value.


In the C code the new header file ``myIterator.h`` needs to included so
that the names of the iterator are known. Later, the linker needs to link the
test application against a compiled version ``myIterator.c`` which provides
the functionality.

Hwut needs to called with ``gen`` as first argument in order to trigger
iterator code generation. This is best done in a *Makefile*. 

.. code-block:: make

    test-it.exe: test-it.c 
        hwut gen test-it.c  -o hwut_stub
        $(CC) -I$(HWUT_PATH)/support/C             \
              $(HWUT_PATH)/support/C/hwut_cursor.c \
              test-it.c                            \
              myIterator.c                         \
              hwut_stub.c                          \
              -o test-it.c

Since ``myIterator.c`` needs to be redone each time that ``test-it.c`` is
modified no separate rule is required for the ``hwut gen`` command. It can be
pasted immediately before the ``CC`` compile command. The HWUT iterators use
``hwut_cursor.c`` which has to be specified also on the command line. The
include path ``-I$(HWUT_PATH)/support/C`` is required so that HWUT's headers
may be found.  This test can be build with::

   > make test-it.exe

and executed by::

   > ./test-it.exe

..  
   Using 'satisfactors' simplifies the task of stimulating 
   particular conditions. They are specified after the parameter settings
   in side ``?{^`` and ``^}`` brackets.
   int x;      int y;
   |0:0xFF|;   |0:0xFF|;   ?{^  ((x << bit_n) * y) >  0x10 ^};
   |0:0xFF|;   |0:0xFF|;   ?t{^ ((x << bit_n) * y) >  0x10 ^};
   |0:0xFF|;   |0:0xFF|;   ?t{^ ((x << bit_n) * y) <= 0x10 ^};
   |0:0xFF|;   |0:0xFF|;   ?tf{^ ((x << bit_n) * y) <= 0x10 ^}; => 1 true, 1 false
                           // If at the end, one is missing => assert fails.
   |0:0xFF|;   |0:0xFF|;   ?tf{^ ((x << bit_n) * y) <= 0x10 ^}; => 1 true, 1 false
                           ?tf{^ Something else ^}; 
                           // MC/DC tests.

