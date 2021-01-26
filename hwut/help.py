import sys
import hwut.common as common

txt = \
"""
H.W.U.T. - The Hello-Worldler's Unit Test

USAGE:

     hwut [service] [test-program [choice]] [options] 

        These calls initiate unit tests. If the test-program and
        the choice is specified, then only the given test-program
        is executed with the given choice. If no choice is specified
        then all choices for the given test program are examined.
        If no test-program is specified, than HWUT searches recursively
        for all TEST directories (including the current directory, if
        it is called TEST). It executes any executable test in those
        directories.

     hwut service [test-program [choice]] [options] 

        If the first argument passed to HWUT is the name of a service, 
        the service is executed. The set of tests can be restricted
        in the same way as for normal tests--see the description above.
        Section SERVICES describes the services that HWUT has to offer.


OPTIONS:

   -v, --version   Version of the H.W.U.T. program.

   -h, --help      This help.

   --exec
        For non-test services only. If this option is set, the 
        test is executed before further consideration. Otherwise,
        The output from the ./OUT directory is taken.

   --fail
        Consider only tests that failed

   --grant
        Answer all interactive questions with 'yes'.

   --no-grant
        Answer all interactive questions with 'no'.

   -w, --terminal-width number
        Sets the terminal width for the output. Default = 80 
        characters.

SERVICES:
   
   hwut test [test-program [choice]] 
   hwut t    [test-program [choice]] 
   hwut [test-program [choice]] 

        With 'test' as the first argument, hwut does perform
        unit tests. That means, that it executes all executable
        files in the TEST directory and all files reported 
        by 'make hwut-info'. Then it compares their output with
        the output in the GOOD directories.
     
        Note: The service name 'test' is optional. If no service 
        is specified, then 'test' is assumed. In practice, this means
        that it is only to be mentioned explicitly if your test
        application has the name of a hwut service (e.g. diff, info, etc.).
        Thus under normal circumstance just leave it.

   hwut diff prg [test-program [choice]] 
   hwut d    prg [test-program [choice]] 

        Displays the difference between good and bad outputs. The 
        difference display program can be one of the following:

        d  or diff     for the standard unix diff application.
        v  or vimdiff  for the vimdiff application.
        tk or tkdiff   for the tkdiff application.
        gv or gvimdiff for the gvimdiff application.
   
   hwut accept [test-program [choice]] 
   hwut a      [test-program [choice]] 

        Accept a test as good. That means, that it copies the output
        of the test into the GOOD directory.

   hwut info [test-program [choice]] 
   hwut i    [test-program [choice]] 

        Re-print the output of the last test run without actually 
        running the program.


   hwut clean
   hwut c    

        Clean the TEST directories from unrelated files. Call
        'make clean' for all directories. 

   hwut mostlyclean
   hwut mc

        Clean the TEST directories from unrelated files. Call
        'make mostlyclean' for all directories. 

LICENSE:

   This program is distributed under LPGL under the constraint
   that it is not used for military applications. There is no
   license for military applications.

   THERE IS ABSOLUTELY NO WARRANTY PROVIDED WITH THIS PRODUCT.
   
AUTHOR:

   (C) 2007 Frank-Rene Schaefer (11.02.1970)

FURTHER INFO:

   Please, visit http://hwut.sourceforge.net for the newest 
   updates and documentation.

"""

def do():
    global txt
    print txt
    sys.exit(0)

def print_version():
    print "HWUT Version " + common.HWUT_VERSION
    sys.exit(0)
