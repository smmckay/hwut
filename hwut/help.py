import sys
import hwut.common as common

txt = 
"""
H.W.U.T. - The Hello-Worldler's Unit Test

USAGE:
         > HWUT [options]

OPTIONS:

   -v, --version   Version of the H.W.U.T. program.

   -h, --help      This help.

   --diff executable-filename
       Shows the differences between the good and the current output of the unit test.

   --vimdiff executable-filename
       Shows the differences between the good and the current output of the unit test
       using 'vimdiff' -- if vim is installed on your system.

   --good executable-filename  [--exec|-e]
       Takes the current output of the unit test for good.

   --clean
        Cleans the directories ./OUT and ./GOOD from trailing files.

   --all-good
        Takes all unit tests that are currently to be executed for good.

   --exec
        If used after the --good or --diff option the unit test is executed again.
        Otherwise, the output from the ./OUT directory is taken.

   --failed
        Consider only tests that failed

"""

def do():
    global txt
    print txt
    sys.exit(0)

def print_version():
    print "HWUT Version " + common.HWUT_VERSION
    sys.exit(0)
