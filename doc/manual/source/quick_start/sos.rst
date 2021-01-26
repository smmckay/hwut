SOS -- Creating Makefiles
-------------------------

Creating Makefiles for modules or tests that already belong to a larger project
can be a pain. HWUT supports the creation of Makefiles and test templates for
C.  This is done using the 'SOS' (safe our souls) or 'SOLS' (safe our lazy
souls) mode. A call to HWUT with:: 

  > hwut sos test1.c test2.c other.c ... [OPTIONS]

Creates a Makefile that produces ``test1.exe`` and ``test2.exe``  provided that
``test1.c`` and ``test2.c`` are the source files in the list that contain
``main()`` functions. In the generated Makefile all include directories,
required libraries, and related source files are setup to produce the test
application. A call to hwut with 'sols' goes even further::

  > hwut sols my-module.c [OPTIONS]

In that case HWUT investigates 'my-module.c' for all function that it
implements, external and internal (i.e. ``static``). It generates test
templates for all functions where implementations have been found. For
external functions the test files are named ``test-FFF.c`` and for internal
``test-FFF-static.c`` where ``FFF`` stands for the name of the function.

The investigation of include directories and reference implementations must be
supported by ``OPTIONS``. At least, the ``--root`` option must be provided so
that HWUT can find the root directory from where to search related header
files, source files, and libraries. The ``--args ... --`` options is most
likely necessary to pass compile flags to the compiler and linker. The complete
list of related options is given below.

 .. option:: --root-include [DIR]+

    Whitespace separated list of root directories from where any include file
    can be searched.

 .. option:: --root-sources [DIR]+

   
    Whitespace separated list of root directories from where to search for
    source files implementing required references.

 .. option:: --root-libs [DIR]+
    
    Whitespace separated list of root directories from where to search for libraries.

 .. option:: --root-objects [DIR]+

    Whitespace separated list of root directories to search for pre-compiled
    object files to implement required references.

 .. option:: --root [DIR]+

    Sets the default list of directories for each one of the above, if it is
    not defined.

 .. option:: --makefile NAME

    Explicitly defines the name of the Makefile. Default is ``Makefile``.

 .. option:: --exclude [PATTERN]+

    Whitespace separated list of patterns that filter out files to be excluded
    from consideration. Example ``--exclude "stub-*.c"`` excludes any C-files
    from consideration that starts with ``stub-``.

 .. option:: --exclude [PATTERN]+

    Whitespace separated list of patterns that filter out directories to be
    excluded from consideration. Example ``--exclude-dir "*/TEST" "*/TEST/*"``
    any file located in a ``TEST`` directory or a subdirectory from
    consideration.

 .. option:: --cc-args [...] --

    Passes the arguments given until ``--`` to the compiler.  For example, some
    tests might required something like a ```-DOPTION_UNIT_TEST`` definition to
    compile under unit test environments. At this place, only such options make
    sense which are required to compile. Options for warning detection, code
    optimization, coverage analysis, profiling, or the like are best added
    later in the resulting Makefile. 

 .. option:: --ld-args [...] --

    Passes the arguments given until ``--`` to the linker. 

 .. option:: --args [...] --

    Passes the arguments given until ``--`` to both, the compiler and the linker.

The best way to invoke HWUT for makefile generation is to write a tiny shell
script such as::

    hwut sols ../src/my-module.c                          \
              --args -DOPTION_HWUT -DOPTION_LINUX_X86 --  \
              --root-include ../src                       \
                             ../../../                    \
                             $HWUT_PATH/support/C         \
              --root-sources ../src                       \
                             ../../common/src             \
              --exclude-dir  "*/TEST" "*/TEST/*"
  

When a new module is written there is some significant effort related to 
finding the required headers and include directories. To support this initial
effort, the 'sosi' feature comes to the resque. When run in that mode, HWUT 
tries to find reasonable include directories, and, at the same time tries
to find headers where identifiers are defined. 


    hwut sosi --root ../../../../               \
                     ../../../../other/src      \
              --identifiers  unsigned8          \
                             extractNameFromDb  \
                             xBool              

With this instruction HWUT will first find a set of include directories which
does not contain an include header twice. This may require user interaction. 
Then, it tries to find as many identifiers in include headers as possible. The 
list of include paths is printed on the screen preceeding a '-I' in front of 
each include path. The proposed headers are printed in the C-include command
format, i.e. following the scheme '#include <header.h>'. With these informations
it shall be particularily easy to compile a C file into an object file.
