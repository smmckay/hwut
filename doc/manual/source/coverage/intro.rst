.. _sec-coverage:

Test Coverage
=============

The aim of tests is to get an impression about the quality of a given piece of
software. When a HWUT component test reports ``Oll Korrect!`` this shall
express a certain trustworthiness. For this to be true, it must be safe
to assume that the tests actually test the component sufficiently. Thus, 
for a reasonable judgement a test result must be related to a measure
what 'portion' of the software is actually tested. The quality of 
a component must therefore be derived from three parameters

   *  A definition of the software component under test, i.e. which
      functions and modules are under test and which are not.

   *  Some number that tells how much of the software is tested, i.e.
      a so called *test coverage*.

   *  The test result.

There are many different ways to measure test coverage, e.g. by means of  *line
coverage*, *branch coverage*, etc. In many systems a nominal behavior must be
tested against a set of possible *scenarios*. Tests that are oriented versus
plain input/output behavior may be measured sufficiently with static measures,
such as line or branch coverage. For software components that manage an
internal state, different scenarios become important. 

A meaningful quantitative measure for the test coverage still requires 
the judgement of a human reviewer. In this section, though, the *coverage*
measure is introduced to help the developer of unit tests to set
his focus and identify weak points of his tests.

.. _sec-test-coverage-gcov:

The coverage considerations may be restricted in the ``hwut-info.dat`` files. 
In the section section, lines starting with ``--coverage`` and 
``--coverage-not`` determine file patterns and anti patterns. The first 
following pattern determines paths. The second, optional pattern determines 
functinos.  Consider the example below

    Some Title
    --------------------------------------------------------------
      ...

    --covergage-not  ./*    print_*

    --------------------------------------------------------------

Here, the file anti pattern is ``./*`` specifying all files of the current TEST
directory. The function anti pattern is ``print_*``. The result is that all
functions starting with ``print_`` in any file in the current directory are
omitted from coverage consideration. 

If no anti function pattern is specified then all functions of matching files
are forbidden. That is::

    --coverage-not   ./*

exempts the entirety of all functions in files in the current directory from
coverage considerations. The counterpart to anti-patterns are positive patterns
which determine the set of admissible files and functions. For example::

    --coverage module*.c

says, that only those modules have to be considered which match ``module*.c``.
On function level, the following example::

    --coverage compute.c  calc_*_float

says that only those functions have to be considered which are in file 'compute.c'
and match 'calc_*_float'. 

If a file does not match any anti pattern, then it is considered in its
entirety. When HWUT is called for a directory tree all coverage data is
collected. For a given file 'F' with the list of function names 'LFN' the
following procedure describes the selection of the set of considered functions

  # If there is no file anti pattern that matches the file 'F', then it 
    is considered for analysis. 

  # Otherwise, collect all function anti patterns for it.

  # Allow any function from 'LFN' where there is at least one function anti 
    pattern that does not match.

There is a subtle distinction being made on the first option passed to
``--coverage-not``. If the path specifier contains directory seperators, 
than it is considered a 'path pattern'. Otherwise, it is considered a 
file pattern. In that case, it concerns any file in any directory whose
base name matches the given name. For example::

    --coverage-not   hwut_cursor.c

ignores the source file ``hwut_cursor.c`` wherever it may be defined.

The sequence of occurrence of ``--coverage-not`` lines does not influence
the selection behavior. The procedure, however, is permissive in its nature. 
If two specifications can be applied and one permits, then the total verdict
is 'permission'.  For example,::

    --coverage-not ./*
    --coverage-not   *  xyz_*

does *not* exclude the files of the current directory. The reason for this is,
that files of the current directory match the second file anti pattern ``*``.
For the files matching it, any function is allowed which does not match
``xyz_*``. That is, even though the first line forbids all functions in files
of the current directory, the second line makes them 'permitted'--except
for those starting with ``xyz_`` in their name.

..note:: 

    Instead of using wildcards in path-names, use relative paths. All paths
    in the ``--coverage-not`` section shall be relative to the current
    test directory. 

Environment variables are expanded through the use of ${...} expressions. For
example::
    
    --coverage-not ${HWUT_PATH}/support/C/*

ignores all C-files from the support module of the currently used HWUT 
installation.


GCov for C/C++
..............

HWUT can interact with the GNU *gcov* utility to measure coverage. It either
refers to 'gcov' as it is found in the current 'PATH' variable, or if the
environment variable ``HWUT_GCOV_APPL`` is defined it relies on its content.
GCov is a tool to measure line coverage, i.e. it can tell to what percentage
the lines of a function are actually executed during the tests. In order to use
this tool, the code must be compiled with the GNU compiler using the two
compile options::

        gcc ... -fprofile-arcs -ftest-coverage ...

Note, also that for coverage measurement, the compilation should create an 
object file for each file under consideration. That means, you should *not*
simply write make rules like

    .. code-block:: make

       my-test.exe: file_0.c file_1.c ... file_77.c
            gcc file_0.c file_1.c ... file_77.c -o my-test.exe

Instead, the process is better split into

    .. code-block:: make

       my-test.exe: file_0.o file_1.o ... file_77.o
            gcc file_0.o file_1.o ... file_77.o -o my-test.exe

       %.o: %.c
            gcc -c -fprofile-arcs -ftest-coverage $< -o $@

The coverage of tests can be determined by means of the *gcov* service. That means,

   > hwut gcov

executes a coverage test for all TEST directories in the sub-directory tree. During
this process HWUT again interacts with the makefile in order to get some basic
information required to do the measurement. There are three make targets that
define the details of the coverage measurement:

  .. describe:: hwut-gcov-obj

     This target must return a whitespace separated list of directories 
     that contain generated object files. 

  .. describe:: hwut-gcov-info

     When HWUT calls ``make hwut-gcov-info`` the Makefile must return a
     whitespace separated list of C/C++ files that are to be considered for
     coverage. 

  .. describe:: hwut-gcov-funcs

     The implementation of this target is optional. When it is implemented
     it shall report the names of functions that are actually tested. This
     way, functions can be excluded from consideration that are part of the
     object files required to compile, but which do not have anything to do
     with the test.

Earlier it has been discussed that for a meaningful measurement it is essential
that the software under test is sufficiently precise defined. In the case of 
*gcov* the software under test is defined by the list of object files, i.e.
make target ``hwut-gcov-info`` and the list of functions, i.e. make target 
``hwut-gcov-funcs``. The following Makefile fragment shows an example

   .. code-block:: make

      hwut-gcov-obj:
           @echo ./ $(MAIN_OBJ_DIR)

      hwut-gcov-info:
           @echo $(SRC_TEST) $(SRC_MINE)

      hwut-gcov-funcs:
           @echo my_component_do \
                 my_component_let \
                 my_component_drop \
                 my_component_catch 

It tells that the object files to be considered for coverage measurement are
located either in the current directory or the directory referred to by variable
``MAIN_OBJ_DIR``.  The source files to be considered are stored in the variables
``SRC_TEST`` and ``SRC_MINE``. Note, that if files are included in test files,
such as to access static functions, then the test files *must* be specified
in the ``hwut-gcov-info`` target.

From all the functions in those files only the four functions reported by
``hwut-gcov-funcs`` are to be considered. The ``@`` at the begin of the echo
command tells that the string ``echo`` is not printed on the standard output.
This is essential to prevent ``echo`` itself from being considered as an object
directory, source file, or function under test.

In the result, functions that are omitted are printed in '(' ')' brackets. 
Due to compilations with different macro settings, the same function may appear in
different object files. If this is the case, then the function name is preceeded
by a '+' sign. The coverage value in this case is the coverage value of the
maximum.

.. note::

   In some cases, a 'time stamp error' occurs. This may mean, that object files
   have been compiled multiple times. To avoid this in 'gmake' declare all 
   object files as ``.SECONDARY`` targets. For example::

      .SECONDARY: file-x.o file-y.o file-z.o

   This keeps gmake from repeatedly deleting and rebuilding them.
