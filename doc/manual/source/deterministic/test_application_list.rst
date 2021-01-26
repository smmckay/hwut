.. _sec-list-of-applications:

List of Test Applications
=========================

Each ``TEST`` directory groups a list of test applications that cover some
specific functionality. Some test applications might be executable scripts
which are interpreted by some interpreter program, others require a build
process to be built. This section discusses the process how HWUT determines
the list of test applications in a given ``TEST`` directory. It consists
of three basic steps:

   #. Requesting the *list of make-able applications* from the Makefile.

   #. Determining the *filtered list of present files* in the ``TEST``
      directory.

   #. Unifying both lists into a single list of test applications

The list of make-able test applications is reported by the Makefile, as
specified by the user. There is no need for any further user controlled 
filtering of this list. Considering the list of present files in the ``TEST``
test directory, however, might necessitate some control in order to prevent
unwanted files to be considered as test applications. Since make-able
applications can be also in the list of present files, both lists need to 
be unified.

Make-dependent Applications
---------------------------

Using the make application [#f1]_ HWUT interacts with the Makefile in the
current directory. It does so by invoquing ``make hwut-info`` and reading the
standard output. If there is no response, for example because there is no
makefile, the hwut continues with step 2.

If the Makefile responds with a non-emptry string its response is considered
as the list of make-able test applications. In the Makefile itself there should
be a section such as 
   
   .. code-block:: make

      FILES = test-border \
              test-equivalence-classes \
              test-special-cases \
              test-mean-conditions
      ....

      hwut-info:
           @echo $(FILES)

The ``@`` before 'echo' prevents that 'echo' appears in the output itself. Since
the user has full control over the list of test applications he wants to report
as response to ``hwut-info``, there is no need to filter the list of make-able
test applications. It would actually be harmful, since there would be no 
longer one distinct place of specification. 


Filtered List of Present Files in ``TEST``
------------------------------------------

For test applications that can be run without any build procedure, e.g.
scripts of any kind, HWUT considers the list of present files in the ``TEST``
directory. In order to separate the wheat from the chaff it applies
*filtering*. The user can control the filtering by means of the file
``ADM/scripts.txt``, or HWUT relies on default filtering. 

Default Filtering
.................

If no file ``ADM/scripts.txt`` is present, then HWUT will apply 
a simple filtering rules:

   # If there are make-able applications than filter out
     all present files in the directory. No script will be
     considered.

   # If there are no make-able files then consider only  
     executable files in the current ``TEST`` directory. 

On Unix systems, 'executable' means that the file has its executable 
rights set. On Windows and Cygwin systems is searches for files with 
extensions '.bat' and '.exe'. This is the default behavior and 
it should work for most cases. The default filtering is sufficient as
long as all tests are make-able tests, or as long as the executable
flags of test applications can be preserved safely.

When tests are to be applied on different platforms, or if they
are communcated in a way were executable flags are not preserved 
(e.g. through a configuration management tool), then it becomes
necessary to apply controlled filtering as described in the next 
section.

Controlled Filtering
....................

If the file ``ADM/scripts.txt`` is present and if it is non-empty, then it is
used for filtering.  In this file, the user can specify filtering rules
explicitly. The syntax of this file is line based and it relies on regular
expressions in the UNIX-shell command line style to specify file patterns, i.e.

    +------------+---------------------------------------+
    | Pattern    | Match                                 |
    +============+=======================================+
    | ``?``      | one arbitrary character               |
    +------------+---------------------------------------+
    | ``*``      | list of arbitrary characters          |
    +------------+---------------------------------------+
    | ``[abc]``  | any character *a*, *b*, or *c*        |
    +------------+---------------------------------------+
    | ``[!abc]`` | any character except *a*, *b*, or *c* |
    +------------+---------------------------------------+

The filtering script consists of two part: first, 'inclusive' lines that
defines patterns of files to be generally considered test applications.
Second, 'exclusive' lines to filter out files that look like test applications
but are not. Exclusive lines start with a ``--not`` key word.  Inclusive lines
my start with the name of the interpreter that is used to execute the test
application. Consider the following example::

      python30  *-3.0.py
      python24  *-2.4.py
      *.sh
      latex     *.tex
      
      --not [aA]ux*.py
      --not test-?-*-doc-*.tex

The first four lines define  that files ending with ``-3.0.py``, ``-2.4.py``,
``.sh``, and ``.tex`` from the ``TEST`` directory are all candidates of test
applications. Additionally, it is specified that files ending with ``-3.0.py``
are to be executed by ``python30``, files ending with ``-2.4.py`` are executed
by ``python24``, files ending with ``.tex`` are executed by ``latex`` and
files ending with ``.sh`` are directly be executed by the system.

The last two lines defines how the list of candidates can be pruned further.
If, for example a file ends with ``.py`` but starts with ``aux`` or ``Aux``
then it is excluded, as specified by the first ``--not`` line. The second
``--not`` line specifies that a file that ends with ``.tex`` but starts
with ``test-`` followed by an arbitrary character, followed by ``-``, and
contains ``-doc-`` somewhere in its name is also excluded. The above example
was chosen to show the possibilites. In practical, the filtering script
is most probably are very simple one, such as::

       *.py

       --not test_helper.py
       --not benchmark-*.py

This says that  only python files are considered, except for two types.
First, the file ``test_helper.py`` is not a test application, may be 
because it is imported by multiple test applications. Second, no file 
that matches ``benchmark-*.py`` because may be used to make some general
measurements which are not related to unit tests.

    .. _fig-filter-application-list:

    .. figure:: ../figures/application-list-filter.*

       Filtering of the list of test applications.

Figure :ref:`fig-filter-application-list` shows graphically how filtering 
works for the following example setup: 

    #. The makefile responds to ``make hwut-info`` with: ``test0.exe`` and ``test1.exe``. 
 
    #. The list of files in the ``TEST`` directory is ``congruence.py``, ``auxiliary.py``, 
       ``A-Test.py``, ``old-Test.py``.

The script ``ADM/scripts.txt`` looks as follows::

    *-Test.py
    --not *old*

As can be seen in the figure, the make-able applications pass directly to
the set of test applications and are not filtered. The list of files in ``TEST``
is first reduced to those that match ``*-Test.py``. Here, only ``A-Test.py``
and ``old-Test.py`` remain. Now, ``old-Test.py`` is filtered out by the exclusive
filter matching ``*old*`` and only ``A-Test.py`` is added to the list of 
test applications.

.. footnotes:

   [#f1] The make application is either the ``make`` that is available through
         the system's path variable, or if specified, the value of the environment
         variable ``HWUT_MAKE_APPL``.

