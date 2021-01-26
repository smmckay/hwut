.. _sec-function-stubs:

Function Stubs
==============

Functions which are called may relie on other sub functions which are
implemented in other modules.  The behavior of those sub-functions is,
strictly seen, an input to the function under test. In many cases, though, it
is difficult or even impossible to control the behavior of these functions by
setting of function parameters or global objects. This is especially true
for functions which interact with hardware. To cope with that HWUT provides
the feature of HWUT-Stubs. 

By the means of HWUT-Stubs the user may remote control the functions under the
hood. HWUT-Stubs control functions provide a means to specify the return
values of stubbed functions or link them to a specific behavior. For this, 
HWUT needs to generate some code. This is done in a stub specification
file. For 'C' one basically needs to copy/pase the function signature of
stubbed functions, together with some required headers. For example

.. code-block:: cpp

        #include <stdio.h>
        #define  size_t   int
        #define  bool     int
        #define  uint8_t  int

        /* <<functions>> */
        void my_write(float SignalID, int Value);
        int  my_read(float SignalID);

        void my_flag_unset(uint8_t* flag_memory, size_t BitIndex);
        void my_flag_set(uint8_t* flag_memory, size_t BitIndex);
        bool my_flag_get(uint8_t* flag_memory, size_t BitIndex);
        
pasted five signatures of functions which are required for a test. For them to
compile, some defines and includes are required. The header information is
separated from the function signatures by a line that contains the signal
"<<functions>>". If these settings are stored in a file "my_stubs.c", hwut can
be called with::

   > hwut stub my_stub.c

which results in two generated files: "hwut_stub.h" and "hwut_stub.c". The
first is to be used as include header, the latter needs to be linked against.
Provided that a function does not return 'void', it is now possible to control
the stubbed function's return values by

   .. describe:: function_name_RETURN(Value)

   .. describe:: function_name_RETURNS(N, Value0, Value1, Value2, ...)

The fist function tells that 'function_name' returns always 'Value'. The second
function lets it return Value0 the first time, Value1 the second time, etc. If
there are more than N calls to the function it starts all over again with
Value0. For aggregated types the ``_RETURN`` and ``_RETURNS`` functions take
*pointers to values*, rather than values.

In case that function return values are not enough the whole function may be
implemented in a simplified manner. The redirection to simplified
implementations is controlled by

   .. describe:: function_name_CALL(FunctionP)

   .. describe:: function_name_CALLS(FunctionP)

The first function lets 'function_name' call 'FunctionP' whenever it is
called. It calls FunctionP with the exact arguments as it receives. The
second function calls the given FunctionP with a first argument: N. Where
N is the number of times that the function has been called. This may 
help to mimik scenerios that can be related to sequences.

Imagine, a function "wait_for_acknowledgement()" which polls some receive
channel and only returns when it foind an 'acknowledge':

   .. code-block:: cpp

      bool wait_for_acknowledgement(char* buffer) {
        ...
            if( receive(buffer) ) return true;
        ...
        return false;
      }

The underlying 'receive' function could be served by 

   .. code-block:: cpp

      static bool
      my_receive(int N, char* buffer) {
          switch( N ) {
          default: *buffer = 0;                return false;
          case 10: memcpy(buffer, "hello", 6); return true;
          }
      }
      
Here, the 'my_receive' uses the number of calls to determine what to do.
In the test the simplified mimiker may be setup by 

   .. code-block:: cpp

      receive_CALLS(my_receive);

By means of HWUT-Stubs it is possible to observe the behavior of the 
underlying stubs and the test in *one single place*. This clearly 
supports the idea of obvious relations between tests and requirements.

.. note:: 

   Sometimes some functions of a modules need to be stubbed and others
   not. For such cases, make sure that the object file 'hwut_stub.o'
   (or howsoever you name it) appears before the correspondent object
   file which also implements the stubbed function. Then, the linker must
   be told to use the first definition. With GNU's 'ld' this is done
   by specifiying ``-z muldefs``. For example::

       gcc -z muldefs myfile.o hwut_stub.o other.o

   makes sure that any function implemented in hwut_stub.o will not be
   taken from other.o. Note, that 'gcc' calls 'ld' implicitly together
   will some compiler specific command line options.

.. note::

   Sadle, on some systems, there is no correspondent to '-z muldefs'.
   Then, one might either rely on compiling the concerned module into
   a shared library, or frame the stubbed functions by pre-processor
   conditionals. For a function 'x' which is supposedly to be stubbed
   consider a macro ``HWUT_IGNORE_x``. If it is defined the function
   shall be ignored. If not, which is the normal production case, the
   function is properly compiled and linked. Consider the following
   as an example.

   .. code-block:: cpp

      #ifndef HWUT_INGNORE_trouble_maker
      void trouble_maker(...)
      {
        ...
      }
      #endif

   Then, compile with ``HWUT_INGNORE_*`` which prevents the original 
   function to be compiled and the linker will pull-in the generated
   function stub.
