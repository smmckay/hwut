Answering HWUT
---------------

Management Information
......................

Once the list of test applications is determined those applications are
made, if necessary, and interviewed. The interview consists of a simple call
of the application with one command line argument: ``--hwut-info``. Then 
the test application needs to respond on the standard output with some
information that is helpful for the test management. The following
paragraphs discuss how HWUT interprets the output of test applications
when it calls them with the command line argument ``--hwut-info``.

.. describe:: Test Title 

    The first line of output is considered as the human readable title 
    of the test. An application 'test-x.sh' that reacts like::

        > ./test-x.sh --hwut-info
        Testing Extra Functionality
        > 

    is considered to have the title 'Testing Extra Functionality' and this title is
    going to be used in the test reports. The first line be also terminated by a
    semi-colon ';' to separate the title from the rest of the output. All
    statements in the subsequent content must be seperated by ';'. 

.. describe:: CHOICES:

    A very useful feature is ``CHOICES``. An application ``test-y.sh`` that 
    reacts like::

        > ./test-y.sh --hwut-info
        Simple Functionality;
        CHOICES: int, long, double;
        > 

    causes HWUT to call ``test-y.sh`` three times each time with a different
    command line argument--each time the first command line argument is the name of
    a choices.  This comes handy when the test procedure differes only a little
    from test to test and can be controlled by a single parameter. If no 
    further statement appears, HWUT will store a seperate reference file for each 
    of its choices. 

.. describe:: SAME

    If all choices expected to produce all the same output, the ``SAME`` flag can
    be raised, e.g.::

        > ./test-y.sh --hwut-info
        Simple Functionality;
        CHOICES: int, long, double;
        SAME;
        > 

    causes now HWUT to store only one reference file for all choices ``int``,
    ``long`` and ``double``. All outputs are compared with this single file.

.. describe:: LOGIC:

    If temporal logic is to be applied to the output, the reference rule
    files can be mentioned after a ``LOGIC:`` keyword. For example an application
    responding on ``--hwut-info`` with::

        > ./test-z.sh --hwut-info
        NonDeterministic Special Test;
        CHOICES:  OK, FAIL;
        LOGIC:    Simple-1.tlr, Simple-2.tlr;

    tells hwut to perform a temporal logic test where the rule files are ``Simple-1.tlr``
    and ``Simple-2.tlr``. 

.. describe:: EXTRA_FILES: list of files;

    If ``EXTRA_FILES`` is specified, hwut considers a list of extra files as being 
    produced by the test application. Those files are stored also in the GOOD directory. 
    Each time the test is run not only the standard output is checked. Also, a
    binary comparison of each mentioned file with its good correspondance is done. 
    An 'EXTRA_FILES' option followed by a bracketted choice restricts the mentioned
    files to the given choice.  For example.

        > ./test-z.sh --hwut-info
        Hello World;
        CHOICES:           Good, Bad;
        EXTRA_FILES(Good): file1.txt, file2.txt;
        EXTRA_FILES(Bad):  error.dat;
        EXTRA_FILES:       protocol.log;

    In the above example, the files 'file1.txt' and 'file2.txt' are expected only
    for choice 'Good'. The choice 'Bad' is expected to produce 'error.dat' and the
    file 'protocol.log' is expected to be produced in any case.

The output that HWUT reads can be produced by simple ``printf()``-statements in C, 
or ``print``-statements in Python, or ``echo``-statements in a shell, or whatever
construct a particular programming language uses to print content on the console.



Tests
.....

In order to receive some input that can be used for comparison, HWUT calls the
test application. This is the same as a command line call::

    > ./my-test.exe
    test output 
    ...

It is generally a good praxis to end each test with some print out. This way, when
the terminating print out occurs, it is safe to assume that the test has reached
its proper end. Consider the following example. 

.. code-block:: cpp

    int main(int argc, char** argv ) {
        ...
        printf("Terminated\n");
        return 0;
    } 

In the real good case, the end of the ``main`` function is reached and the 
``Terminated`` string is printed to the standard output. If for example,
a segmentation fault happens, the program will exit prematurely and the 
``Terminated`` string is not printed. The terminating print out is the
means by which premature exits (segmentation faults, uncaught exceptions, 
uncaught signals, etc.) can be detected. 

If the test application has not reported any choices, It is called only once
with no command line argument. If it has reported choices, it is called for
each choice once, where the choice is the command line argument.  If there is
more than one choice, then additional command line arguments are passed that
tell whether it is the first or the last call to the test application. Argument
two can be ``FIRST`` or ``NOT-FIRST`` dependent on the choice call. Argument
three can be ``LAST`` or ``NOT-LAST`` dependent on the choice call be the last
or not. If ``my-test.exe`` has reported the choices ``1``, ``2``, 
and ``3``, then HWUT's calls to the application are equivalent to::

   > ./my-test.exe  1   FIRST       NOT-LAST
   ... 
   > ./my-test.exe  2   NOT-FIRST   NOT-LAST
   ... 
   > ./my-test.exe  3   NOT-FIRST   LAST
   ... 

This is useful, for example, if multiple choices rely on the same
generated resources for the test. When the application is called the first
time, i.e. ``argv[2] == "FIRST"``, the resources can be generated and if it is
called the last time, i.e. ``argv[3] == "LAST"``, the files may be cleaned up.
The fixed position of command line arguments for first and last is done to
simplify the comparison in the test program.

Similarly, when entering a directory for testing, HWUT calls the makefile
target ``hwut-begin``. When it leaves the directory, it calls the target
``hwut-end``. Again, multiple tests may rely on the same generated files and
``hwut-begin`` can be used to generate them, while ``hwut-end`` can be used to
clean them up. If there are two ``TEST`` directories in the subtree::

       example/directory/TEST
       example/another/directory/TEST

Then HWUT's interaction on entering and leaving the directories is equivalent to

   .. code-block:: bash

       > cd example/directory/TEST
       > make hwut-begin
       ... testing ...
       > make hwut-end
     
       > cd example/another/directory/TEST
       > make hwut-begin
       ... testing ...
       > make hwut-end

Note, however, that it might not be desireable to delete all generated 
files on ``hwut-end``. This would mean, that when HWUT is finished, the 
files are no longer present for manual testing. 
