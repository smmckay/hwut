Installation
------------

Following stepts guide towards a working HWUT environment:


.. describe:: Python Language

    HWUT requires the Python Programming Language to be installed. 
    The website `http://python.org` <http://www.python.org>` maintains
    downloadable packages. Please, note that for HWUT, the python version
    shall be lesser than 3.0.

.. describe:: Unpack HWUT

    To install HWUT, a package of the form ``hwut-10y02m11d.tbz`` is required.
    It must be unpacked in an appropriate directory on your machine. The directory
    where HWUT is unpacked must be written to the environment variable 
    ``HWUT_PATH``, as explained later.

    On Windows, copy the file ``hwut.bat`` to ``C:\WINDOWS\SYSTEM32\`` or
    any other place in your system's path. The file contains a line of the
    type::

        python %HWUT_PATH%\hwut-exe.py ...

    If you have multiple versions of Python installed, please, replace ``python``
    with the exact path to a python version below 3.0, e.g.::

        C:\Python26\python %HWUT_PATH%\hwut-exe.py ...

    On Unix machines and the likes please, add a symbolic link from a bin directory
    to hwut-exe.py and set executable rights, i.e.::

       ln -s     $HWUT_PATH/hwut-exe.py  /usr/local/bin/hwut
       chmod a+x $HWUT_PATH/hwut-exe.py  /usr/local/bin/hwut

    You might also ensure executable rights for all subdirectories, so that hwut
    can write byte compiled files, i.e.::

       chmod a+wx -R $HWUT_PATH
 
.. describe:: Diff Display Application

    If the **diff-display** feature shall work, then HWUT requires a 
    diff-viewer, such as 'vimdiff', 'gvimdiff', 'BeyondCompare2', 'WinMerge'
    or 'TkDiff'. Those diff-display tools either come with the distribution
    of your operating system, or are available on the internet. Later
    in this section it is explained how to setup hwut for a particular
    diff display application.

    By default, HWUT relies on the *vimdiff* application which is 
    installed on most Unix machines.

.. describe:: Compile Environment

    For a solid compile environment at least a version of the *make* utility
    shall be installed. Preferably, `GNU-make <http://www.gnu.org/software/make/>`
    may be used. For coverage measurements in C-programs `gcov` must be installed
    together with a version of the GNU C/C++ Compiler. For Microsoft Windows
    the MinGW-Suite provides all required applications in one. For Unix based
    systems one can most probably rely on the distribution CD/DVD. 

.. describe:: Environment Variables

    Once all applications are present, the HWUT environment variables can be
    specified, as they are 

     .. data:: HWUT_PATH (mandatory)

              must contain the directory path to the place where HWUT was 
              installed. Please, use double quotes if the pathname contains
              whitespaces.

     .. data:: HWUT_DIFF_APP (optional)

              must contain the path and name of the difference display 
              application. By default 'vimdiff' is used. Note, that the
              diff display application can also be specified on the command
              line.

     .. data:: HWUT_TEST_DIR_NAME (optional)

              By default, HWUT checks for directories that are called ``TEST``. 
              If this shall be different, the environment variable above allows
              to specify customized directory name.

     .. data:: HWUT_MAKE_APPL (optional)

              For interaction with Makefiles, HWUT requires a version of *make*.
              By default it uses the make that is available through the system's
              ``PATH`` variable. To choose a different make, set the value of 
              ``HWUT_MAKE_APPL``.

     .. data:: HWUT_GCOV_APPL (optional)

              By default HWUT uses ``gcov`` as available in the system's path. 
              To use a specific gcov application set the value of ``HWUT_GCOV_APPL``.
              This variable needs only to be specified if coverage measurements
              in 'C' are to be performed and an application different from 'gcov'
              is to be used.

     .. data:: HWUT_TERMINAL_WIDTH (optional)

              Determines the width of the user's terminal in characters. If 
              this variable is not defined, a terminal width of 80 characters
              is assumed. The terminal width can also be specified for
              each call to hwut by the command line options ``-w`` or
              ``--terminal-width``.

     .. data:: HWUT_LCOV_APP (option)

              Defines the 'lcov' application for C/C++ coverage analysis. On 
              some systems something like 'perl C:\Lcov\lcov.perl' must be
              defined.

     .. data:: HWUT_GENHTML_APP (option)

              Defines the 'genhtml' application for C/C++ coverage analysis.



On Unix machines, these variables are best stored in the ``.bashrc``-file (or
whatever shell you use), or ``/etc/profile``.  On Microsoft Windows (tm)
clicking [Start][Settings][ControlPannel]-->[System][Advanced] opens a tab window
with a button [Environment Variables]. Click this button and define the environment
variables above.

The following sections explain the basic usage of HWUT. They show how with a
few commands and concepts software tests on the level on Unit Tests, i.e.
tests on the *per function*-level, and System Tests, i.e. tests on the
*behavior*-level can be performed and managed. In scenarios where the system's
behavior is no longer fully deterministic *temporal logic* rules need to be
applied. Those, however, are explained in later chapters. Again, HWUT supports
*deterministic tests* and *temporal logic* test. This introductory section only
elaborates on deterministic tests. 


