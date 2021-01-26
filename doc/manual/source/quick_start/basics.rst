Basic Concept
-------------

The basic idea of HWUT is that a test-application interacts with software to be
tested. During this process strings are printed to the standard output. The
human tester checks this output until he is of the opinion that it is correct.
He invoques HWUT with the command ``accept`` and HWUT stores it away for
reference. HWUT is now able to compile and execute the test application,
compare its output to the reference and judge wether it is the same or not. If
it is not the same, the test has failed.

.. fig-usage-basic-I:

.. figure:: ../figures/HWUT-test-output.*

   Test observation based on text passed to the standard output.

.. figure:: ../figures/HWUT-test-comparison.*

   Judgement based on textual comparison.

What HWUT does is that it look for all test applications in a ``TEST``
directory. There are lines which are excluded from comparison: Lines that start
or end with a double hash mark ``##`` are not considered.  This facilitates the
implementation of debug output that is not subject to the test itself. If the 
reference output is

.. code-block:: bash

    Init Elements --> assigned 10.
    Sort Elements --> list size = 10.
    list: 90, 94, 100, 201, 202, 401, 510, 550, 3123, 53123
    Destruct list --> pointer set to 0x0.

The this is equivalent to

.. code-block:: bash

    Init Elements --> assigned 10.
    ## quicksort split at i = 5
    ## ...
    ## quicksort done
    Sort Elements --> list size = 10.
    list: 90, 94, 100, 201, 202, 401, 510, 550, 3123, 53123
    ## destructor catches exception!!!
    Destruct list --> pointer set to 0x0.

Except for the comment lines, both outputs are the same. Note, also that 
multiple spaces and tabulator marks are reduced to one single space. Thus,

.. code-block:: bash

         print "This is an output"

and 

.. code-block:: bash

         print "This is an   \t output"

write equivalent strings to the standard output. 

Given a specific TEST directory, HWUT executes them and compares their output
with the reference that it stored earlier. The test result is then printed as
follows::

    2010y02m02d 16h55
    (this directory)
    make: just-for-fun.exe .....................................[MADE]
    make: just-for-gaudi.exe ...................................[MADE]
    make: notification-failure-central-registry.exe ............[MADE]
    make: notification-failure-central-registry-2.exe ..........[MADE]
    -------------------------------------------------------------------

     -- Notification:

        Fail 5x, then CentralRegistry.
            notification-failure-central-registry.exe .......[OK]
        Notification Fail, then CR, but FBlock Vanishes.
            notification-failure-central-registry-2.exe .....[OK]

     -- Via Notification:

        Simple
            just-for-fun.exe ................................[OK]

     -- Via Requests:

        Simple
            just-for-gaudi.exe Expected .....................[OK]
                               UnExpected ...................[OK]

         ___  _ _   _  __                        _     _ 
        / _ \| | | | |/ /___  _ __ _ __ ___  ___| |_  | |
       | | | | | | | ' // _ \| '__| '__/ _ \/ __| __| | |
       | |_| | | | | . \ (_) | |  | | |  __/ (__| |_  |_|
        \___/|_|_| |_|\_\___/|_|  |_|  \___|\___|\__| (_)

    ===================================================================


The final *Oll Korrect* states that all tests in this directory have passed. If
a test would not have passed a ``[FAIL]`` flag would be reported instead of
``[OK]`` and the total result would be *Failure*.

Directory Structure
-------------------

Three subdirectories in a ``TEST`` directories are used by HWUT for
special purposes--as they are:

  .. describe:: ADM

     In this subdirectory administrative files are located.  HWUT keeps
     track of the history of testing and the current state of testing. User
     editable files in this directory are:

     .. describe:: title.txt

        Which contains the name of the tests in the ``TEST`` directory.
        This is usualy the name of the module or function group to be
        tested.

     .. describe:: scripts.txt

        This file contains information about how to distinguish between
        files in ``TEST`` that are test applications and those which are 
        not. The default distinction is usually sufficient. Please, consider
        section :ref:`sec-list-of-applications` for more details.

  .. describe:: OUT

     This subdirectory contains the output files of the last run of the test
     application. The content of this directory can be deleted without any 
     harm.

  .. describe:: GOOD

     This directory contains the 'treasured gold', i.e. the reference output
     of test runs that were judged to be correct. Those files result from competent
     human observation of the system behavior and they preserve *knowledge* about
     requirements and behavioral details. 

     With the files in this directory software tests can be performed even
     if detailed knowledge of this system is lost or forgotten. When using
     a configuration management system, it must be ensured that those
     files are kept safe and sound.

The files in ``OUT`` and ``GOOD`` are under control of HWUT. There is no
need for the user to tamper with the files in these two directories. 


Test Applications
-----------------

In a first step HWUT needs to determine the list test applications in the
current ``TEST`` directory. It does so by collecting executable files in the
directory and, optionally, asking a Makefile about applications to be built by
make procedure. In a second step those test applications are interviewed, i.e.
they are called with a command line argument ``--hwut-info``. HWUT then reads
the standard output of the program and interprets it.  The first line of the
application's response is interpreted as test title. For example a Python test
program ``mytest.py``:

   .. code-block:: python

      if "--hwut-info" in sys.argv:
          print "My Stuff's Test"
          sys.exit()

tells HWUT that its title is ``My Stuff's Test``. This title is then used when
printing the test results, e.g.::

        My Stuff's Test
            mytest.py .......................................[OK]

The most important part, though, is still missing: the textual output that
tells about the behavior of the software under test. Imagine a simple 
program that computes Fibonacci numbers and is located in module 
"main/fibonacci.py". A simple test file ``fibo-test.py`` might look like

   .. code-block:: python

      import main.fibonacci as fibonacci

      if "--hwut-info" in sys.argv:
          print "Fibonacci Test"
          sys.exit()

      print 0, "-->", fibonacci.compute(0)
      print 1, "-->", fibonacci.compute(1)
      print 997, "-->", fibonacci.compute(997)
      print 998, "-->", fibonacci.compute(998)

When this program is run, four lines are printed, i.e.::

        0 --> 0
        1 --> 1
        997 --> 497503
        998 --> 498501
        
Once, it is safe to say that the output is correct and covers the intended
functionality, HWUT can accept it, i.e. store the text it as a reference in the
``GOOD`` directory. This is done on the command line by::

     > hwut a fibo-test.py 

Provided that the file is executable, HWUT can now execute tests on its own 
and judge if the test succeeds or fails. It simply compares its current
text output and the text that was stored as a reference. To run HWUT on th
current TEST directory simply type::

    > hwut

on the command line, and all test applications in the current directory are
evaluated. If you only want to execute one particular test application 
``special-test.sh``, then type::

    > hwut special-test.sh

and only this particular test is performed. If an error occurs, the difference
between the current output and the reference output can be viewed by typing::

    > hwut dd special-test.sh

provided that the environment variable ``HWUT_DIFF_APPL`` points to a
diff-display program. If the variable is not set, hwut relies on ``vimdiff`` so
then this program should be installed.

If a GOOD file has to be built incrementally, the ``ai`` accept incrementally
option may be used. It works like ``dd`` only that it creates an empty file if
the GOOD file does not exist. The merge tool may then be used to copy the
elements of the output which are fine.

The test applications and choices may be specified with patterns of the 'Unix
file name pattern matching'--which are not regular expressions. A call to hwut with

   > hwut "test-*-even.sh" "*[Tt]rue*"

executes only those tests where the application's name starts with ``test-``
and ends with ``-even.sh``. The choices to be considered must contain ``True``
or ``False``. These wildcards are:

    +-------------+------------------------------+
    | Pattern     | Match                        |
    +=============+==============================+
    | ``*``       | everything                   |
    +-------------+------------------------------+
    | ``?``       | any single character         |
    +-------------+------------------------------+
    | ``[seq]``   | any character in *seq*       |
    +-------------+------------------------------+
    | ``[!seq]``  | any character not in *seq*   |
    +-------------+------------------------------+

For a literal match, wrap the meta-characters in brackets.  For example,
``'[?]'`` matches the character ``'?'``. Those wildcard matches are also applied
in the ``hwut-info.dat`` file.

.. note::

   Some people write HWUT tests in a DOS/Windows(tm) environment, others in 
   a Unix environment. Pathnames and things may different significantly. So, 
   on larger projects this may cause confusion. For such cases, HWUT provides
   a bridge from DOS/Windows to CygWin (Unix World inside Windows). That means, 
   it can be called from within Windows on TEST-s that have been written and
   designed under Unix. To do this, the batch file::

                      hwut2cygwin 

   has to be called instead of cygwin. A version to bridge from Unix to 
   Windows files is under consideration at the time of this writing. It 
   will likely be called::

                     hwut2wine

   which insinuates that the 'wine' utility will be used to achieve the
   bridging.

Make Dependent Test Applications
--------------------------------

In many cases, test code needs to be compiled before it can executed. This is 
particularly true for test written in *compiled languages* such as 'C', 
'ALGOL', and 'Pascal'. The process of generating executables from test code
must be managed by a Makefile. HWUT needs to be able to say::

   > make some-test.exe

If 'some-test.exe' is a test application to be run in the current directory. HWUT 
asks the Makefile about the test applications to be made by asking::

   > make hwut-info

and parsing the standard output of the call to make. If 'test0.exe', 'test1.exe', and
'test2.exe' are tests to be made in the current directory, then there should be a
make rule::

     hwut-info:
         @echo test0.exe test1.exe test2.exe

The '@' before echo prevents the string ``echo`` to be printed to standard
output. The whitespace separated list of 'words' is interpreted as the list of
test applications that can be built by this Makefile. Consider the following
test file written in 'C' for testing some fibonacci number computing component:

   .. code-block:: c

      #include "fibonacci.h"

      int
      main(int argc, char** argv)
      {
          if( argc >= 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
              printf("Fibonacci Test");
              return 0;
          }
          printf("%i --> %i", 0,   fibonacci_compute(0));
          printf("%i --> %i", 1,   fibonacci_compute(1));
          printf("%i --> %i", 997, fibonacci_compute(997));
          printf("%i --> %i", 998, fibonacci_compute(998));
      }

The makefile that contains the test should at least tell how to buildt 
an executable and that HWUT needs to consider it, e.g.

    .. code-block:: make

       FILES = fibo-test.exe

       all: $(FILES)

       fibo-test.exe: fibo-test.c  fibonacci.h
            gcc fibo-test.c -o fibo-test.exe

       hwut-info: 
            @echo $(FILES)
                  
With this makefile, the user can generate his test applications by simply
typing::

      > make

on the command line. He can then check the output of his program until he is
satisfied and tell HWUT to accept it in the same manner as before, i.e.::

     > hwut a fibo-test.py 

Tests can now be performed in the same way as with scripts that do not need any 
compilation. 

Multi-Platform Tests
--------------------

It makes sense to write Makefiles in such a way that they may be used on
multiple platforms, in particular Unix and Windows. Relying on GNU Make ensures
that directory names can be specified by 'slashes' on both systems.  So, as
long as one relies on relative paths, the directory definitions may remain the
same. Using 'MinGW/MSys' on Windows as a compilation environment further makes
sure that the compile options remain the same. 

One issue may remain: The PATH variable may sometimes not be communicated
correctly to the underlying shell. If HWUT is used for code generation, then
a ``HWUT_EXE`` variable should be defined. In general, it may not be a bad
idea to have variable 'OS' being assigned with the name of the operating 
system. This way, OS specific things may be defined correspondingly.::

    ifneq ($(strip $(SystemRoot) $(SYSTEMROOT)),)
        OS := WINDOWS
    else
        OS := UNIX
    endif
    ...

    ifeq ($(OS),WINDOWS)
        HWUT_EXE := python $(HWUT_PATH)/hwut-exe.py
    else
        HWUT_EXE := $(HWUT_PATH)/hwut-exe.py
    endif
    ...

    stub.c:
        $(HWUT_PATH) stub description.c -o my_stub
       

Summary
-------

This section discussed the basic usage of HWUT for script based and compilation
based testing. Tests are performed by typing::

    > hwut 

in the test directory. To accept the output of a test application one needs to
pass ``a`` as first command line argument and optionally the application name,
e.g.::

    > hwut a my-application.py

If errors occur, the difference of the output can be viewed by passing ``dd``
as first command line argument, e.g.::

    > hwut dd my-application.py

Real life examples can be found in the directories ``demo/scripts/TEST`` and
``demo/compiled/TEST`` that come with the distribution of HWUT. The next two
section elaborate on the details of deterministic and temporal logic tests.
    

