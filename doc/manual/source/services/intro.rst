HWUT Services
-------------

Based on the first command line argument HWUT can executed different services.
The most obvious services are: testing, accepting and viewing differences.
These services have been discussed in section :ref:`Quick Start
<sec-quick-start>`.  This section lists all services and explains their usage.
Note, that HWUT walks recursively through the path tree and searches for
``TEST`` directories to apply the specified service.

.. describe:: version, v, --version, -v 

   This service prints the current version of hwut on the screen, e.g.::

     > hwut version
     HWUT Version 0.13.1
     >

.. describe:: help, h, -h, --help, -?, /?, /h, /help

   The *help* service prints some basic information about how to use HWUT
   on the command line.

.. describe:: test, t

   If ``test`` or ``t`` is passed as first command line argument, then  
   then software tests are executed. The same is true if no command line
   argument is passed at all. HWUT then walks down the path tree until 
   it finds a ``TEST`` directory. Then, in each such directory it searches
   for all test applications and executes them in a manner as discussed in
   previous sections. Then, the test reported is printed on the screen. 

   In the background, HWUT stores information about the current status
   of testing in the file ``ADM/database.xml`` and stores history 
   information in ``ADM/history.xml``.

   Additionally, more command line arguments can be passed to HWUT. The
   following optional argument specifies the file name of the test application to
   be tested. The subsequent optional argument specifies the particular choice
   to be tested. Note, that if the name of the test application is different
   from any of the services (which they usually are), then the ``test`` 
   command line argument can be omitted. Thus::

     > hwut test my-application.sh

   and:: 

     > hwut my-application.sh

   both test only ``my-application.sh``. If this test application has 
   multiple choices, they are all avaluated. A command line call::

     > hwut my-application.sh Scenario_A

   will execute only the test in ``my-application.sh`` with the string
   ``Scenario_A`` as choice. If the first argument is a directory, i.e. 
   it ends with `\\` on Windows or `/' on Unix, the HWUT will enter this
   directory, perform the test and return. Also, if the first
   argument is an application name containing a path, HWUT will enter
   this directory access the application, even if it has to be made, 
   executes the test and returns. For example::

     > hwut components/video/TEST/basic-test.exe Control

   causes hwut to enter ``components/video/TEST``, make ``basic-test.exe``
   and execute it with the choice ``Control``. Once the test is terminated
   it returns to the current directory.

   Again, if your test application carries the name of a
   HWUT service, such as ``info`` or ``delete``, it is necessary to specify the
   test service ``test`` explicitly, e.g.::

     > hwut test delete

   tries to execute the application ``delete`` in the TEST directory, rather
   then performing the service ``delete``. 
   
.. describe:: info, i

   Testing usually requires a substantial amount of time until reports can be
   produced.  The HWUT service ``info`` allows to produce a test report based on
   the information stored in the database files. The printed test report is
   virtually identical to the report printed during testing. The time to produce
   the output is mainly determined by the time to parse the database files. Where
   a test of all ``TEST`` directories of a path tree might take hours to complete,
   the same report can be produced 'in real time' using the *info* service.
   However, that the info service only produces reports on tests that have been
   run before. 

.. describe:: accept, a

   By means of the *accept* service the textual output of a test application is
   taken as a reference for future tests. In pratical, the output is stored in a
   file inside the GOOD directory. If no further command line argument is 
   passed, then all files are considered. For each file where the current output
   differs from the reference output, the user is asked to acknowledge that the 
   reference output is overwritten with the current output. If one more
   command line argument is passed, then this argument specifies the test application.
   Again, one more argument specifies the choice, e.g.::

     > hwut a my-application.sh   Scenerio_0

   will check wether the output of ``my-application.sh`` with choice ``Scenario_0``
   differs from the reference output. If it does, it asks the user to confirm
   that the content shall be copied. To avoid this confirmation question, the command
   line argument ``--grant`` can be passed.

.. describe:: dd

   Once HWUT reports an error for a test, it might be of interest to know how and
   where the error actually occurs. For this, HWUT can call a difference 
   display application. There is a large variety of such tools available,
   free and commercial. By defaul HWUT relies on ``vimdiff``. If this is not 
   wanted, the environment variable ``HWUT_DIFF_APPL`` can be used to specify 
   the difference display application. Also, the command line option ``--app``
   may be used for that same purpose. The command line format is the same as 
   for the *accept* service, i.e.::

     > hwut dd my-application.sh 

   or

     > hwut dd my-application.sh --app kdiff3

   if 'kdiff3'  is the difference display application to be used. The specified
   command iterates over all choices of ``my-application.sh``. If there is a
   difference between the current output and the reference output, the difference
   display application is called. Once, it terminates HWUT askes if it is desired
   to copy the current output as a reference. If a third argument is provided only
   a specific choice is considered, i.e.::

     > hwut dd my-application.sh   Scenario_0

   checks only for difference in the output for choice ``Scenario_0`` is 
   considered.

   It is sometimes advantageous to use the difference display application to 
   merge the current output into the reference output. This has the advantage, 
   that the user observes each single place in the file that is copied. A 
   plain ``accept`` causes the copying of the whole file, which is more prone
   to neglect some details.


.. describe:: run ...

   Executes a command line in every ``TEST`` subdirectory. Note, that pattern
   matching, for example, as it happens in a bash or similar shells is not
   available, by default. To achieve such things a shall must be called
   explicitly.  For example, the following call to hwut deletes all files from
   ``OUT/`` subdirectories of ``TEST`` directories::

    
     > hwut run bash -c 'rm OUT/*'

   The above command executes the 'bash' implicitly and passes the string ``rm -f OUT/*'
   to be executed. The bash is able to perform the pattern matching in order to 
   match all files in the OUT subdirectory.


.. describe:: make

   The *make* service allows for a call to make in all ``TEST`` diretories located
   in the sub-trees of the current directory. The third argument passed to hwut 
   is the make target, thus::

      > hwut make clean

   walks down all sub-directories of the current directory. If it finds a 
   directory with name ``Test`` containing a 'makefile' or a 'Makefile' it
   calls ``make`` with the target as specified. In the example above 
   it calls the target ``clean`` which is by common practise supposed to 
   clean up all unessary and intermediate files.
   As long as one stays in one directory, there is no difference between 
   calling::

      > make clean

   directly or calling it via HWUT. The strenght of the HWUT service, though, 
   lies in its recursive walk through all sub-directories.

.. describe:: time

   When the testing time becomes an issue, the HWUT *time* service may be used
   to determine what tests require how much time to make and to execute. This
   information may be used to decide where optimzations may be applied. Sometimes
   tests cover much more than boundary conditions and equivalence classes. During
   compilation often more headers are included than actually necessary, etc. 
 
   With the *time* service bottlenecks can be identified, simply by typing::

     > hwut time

   and HWUT presents the following output:: 
   
        ==================================================================
        Example Tests On FBlock
        Thu Feb  4 16:23:11 2010
        (this directory)
        ------------------------------------------------------------------

            Fail 5x, then CentralRegistry.
                failure-central-registry.exe <<MAKE>> ....[00:00:10:281]
                                             .............[00:00:00:380]
            ...

            Simple
                just-for-gaudi.exe <<MAKE>> ..............[00:00:01:844]
                                   Expected ..............[00:00:00:340]
                                   UnExpected ............[00:00:00:340]
        ------------------------------------------------------------------
        Execution Time ...................................[00:00:01:890]
        Make Time ........................................[00:00:58:233]
        Total Time Sum ...................................[00:01:00:123]
        ==================================================================
        SUMMARY:

          Total Time:   Make Time:    Directory:
          00:01:00:123  00:00:58:233  (this directory)
        ------------------------------------------------------------------
          00:01:00:123  00:00:58:233  (make time = 96.86%)
        ==================================================================

   A time stamp reported by HWUT has the following format::

                       HH:MM:SS:MIL

   That means, the first two digits are hours, the second two digits are
   minutes, the third represent seconds, and the last three digits represent
   milliseconds.  The time reporting works, as many HWUT services recursively. If
   the *time* service is called in some upper directory, it delivers at the end a
   summary information about the time spend for 'make'-ing and executing the test
   applications, e.g.::

        ==================================================================
        SUMMARY:

          Total Time:   Make Time:    Directory:
          00:02:41:914  00:02:37:064  example_NetworkMaster/TEST
          00:01:53:340  00:00:00:000  it_compiles/TEST
          00:01:00:041  00:00:58:171  most_shadow/TEST
          00:00:58:767  00:00:54:077  most_fblock/TEST
          00:00:52:859  00:00:37:219  example_SDARS/TEST
          00:00:00:549  00:00:00:000  regression/TEST
        ------------------------------------------------------------------
          00:07:27:474  00:05:06:534  (make time = 68.50%)
        ==================================================================

   The list of directories is listed by decreasing total time. The entries
   on top of the list are the most time consuming. Such reports provide a 
   quantitative basis for decisions about efforts to be made towards test time
   optimization.

.. describe:: remove, rm

   When files are no longer to be part of the testing procedure, they can 
   be deleted from the internal database using the *delete* service. The
   file could actually be deleted without telling HWUT, but then HWUT would
   print a ``VANISHED`` message for the file each time it is executed. So, 
   calling

    .. code-block:: bash

       > hwut rm path/to/TEST/file.sh

   will delete the file ``file.sh`' in ``path/to/TEST/``, if it still exists and
   take it out of the datase records. Note, that the deletion is recorded
   in the history file.

.. describe:: move, mv

    When test applications are renamed or moved not only a ``VANISHED`` 
    flag will appear. HWUT also needs to update the correspondent files
    in the ``GOOD`` subdirectory. This could be done by hand, but a
    much more convenient way is to use the *move* service, e.g.
    
    .. code-block:: bash

       > hwut mv    path/to/file.sh   path/to/file_new.sh

    renames the application 'file.sh' in the subdirectory 'path/to' to
    'file_new.sh'. Database entries and files in the GOOD directory are
    changed accordingly. Also,

    .. code-block:: bash

       > hwut mv    path/to/TEST      path/to/NEW_TEST

    moves a whole test directory from one place in the directory tree
    to another. All changes are reported in the file 'ADM/history.xml'.

.. describe:: futile, fu

   The *futile* service outputs a list of files that have no meaning to HWUT 
   in the current TEST directory. They are not necessarily trash. But, the
   printed list is a good basis for cleaning up old ``TEST`` directories
   that are scattered with files of unknown utility.
  
.. describe:: gcov

   This service is discussed in detail in section :ref:`sec-test-coverage-gcov`.

.. describe:: try:logic

.. describe:: try:logic

.. describe:: try:remote

.. describe:: try:regex
