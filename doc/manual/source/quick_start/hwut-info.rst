The TEST Directory
==================

HWUT tests are located in directories called ``TEST`` (or what is defined
through the environment variable ``HWUT_TEST_DIR_NAME``). Starting from where
HWUT is called it walks recursively through the tree of subdirectories. Whenever
it finds a ``TEST`` directory, it searches for two things, as they are

  # A file called 'hwut-info.dat' which specifies the list of tests
    in this directory.

  # A file called 'Makefile' that responds to 'make hwut-info' with the 
    list of make-able test applications. 

If none of these is found, a directory is not considered for testing. HWUT uses
'make' to include the compile-ability *as part of a test* rather than requiring
compile-ability as precondition for testing. The advantage becomes obvious in
larger projects, when not every module is compile-able at every time. If test
applications are not scripts, and they need to be build this is best done 
in a ``Makefile`` and there should be a target inside called ``hwut-info``
of the form

.. code-block:: Makefile

   hwut-info: 
        @echo test0 test1 test2 

where ``test0``, ``test1`` and ``test2`` are the tests to be build by the Makefile.
Scripts and test applications which do not need a build process must be specified
in the file ``hwut-info.dat`` (or what is defined through the environment variable 
``HWUT_INFO_FILE_NAME``). This file has three sections separated by dashed lines.

 # The first section is the title of the tests of this directory. It should tell in 
   one sentence what the tests are supposed to do and make it clear why they appear
   together. 

 # The second section describes test applications of this directory.

   * A Line that does *not* start with ``--`` specifies a file pattern and 
     the interpreter sequence used to execute it. For example lines as::

         python test-*.py
         awk parser.awk *.csv

     tell that tests matching ``test-*.py`` are interpreted by Python. Files
     matching ``*.csv`` are interpreted by ``parser.awk`` which is a program
     that needs to be executed by the Awk utility. 

     The interpreter sequence is optional. For example, in a Unix environment a
     'shebang', i.e. first line starting with ``#!`` and naming the interpreter
     does a similar job, for example

         #! /usr/bin/env python 

     lets Unix use Python to interpret the script. The minimum requirement in
     such a line is the file pattern. HWUT selects only those files of the current
     directory as test applications which match a file pattern.

     This section is aware of environment variables. Identifiers inside ``${...}``
     expressions are expanded to the values of the correspondent environment 
     variable. For example

            perl prog-${MY_VERSION}.pl

     together with the setting of ``1.06`` in the environment variable ``MY_VERSION``
     lets HWUT only consider the perl file "prog-1.06.pl". Note, however, that those
     variables *must* be defined. Otherwise, the correspondent line is not considered.

   * A line starting with ``--not`` lists patterns of files of this directory
     which are not to be considered, even if they were selected previously.

   * A line starting with ``--coverage`` specifies a path or file pattern
     and optionally a function pattern. Files and their functions that match
     those patterns are considered, apriori, for coverage analysis. If nothing
     is specified, then everything is allowed, apriori.

   * A line starting with ``--coverage-not`` specifies a anti-path pattern
     and optionally an anti function pattern. That is, it defines what files 
     and functions *not* to consider for coverage analysis. More about this in 
     section :ref:`sec-coverage`.

 # The third section contains free-style documentation of the tests.


