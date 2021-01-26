#! /usr/bin/env python
#
# PURPOSE: Runs all test scripts and reports results.
#
# (C) 2006, 2007 Frank-Rene Schaefer
# ABSOLUTELY NO WARRANTY
################################################################################
import sys
import os

if os.environ.has_key("HWUT_PATH"):
    sys.path.insert(0, os.environ["HWUT_PATH"])
else:
    print "error: Environment variable 'HWUT_PATH' is not defined'"
    print "error: Let it point to the directory where hwut is installed."
    sys.exit(-1)

from hwut.frs_py.string_handling import trim
from hwut.GetPot    import GetPot
from hwut.classes   import TestApplicationDB
#
import hwut.auxiliary  as aux
import hwut.directory  as directory
import hwut.io         as io
import hwut.common     as common
import hwut.core       as core
from hwut.strategies.accept     import AcceptStrategy
from hwut.strategies.clean      import CleanStrategy
from hwut.strategies.difference import DifferenceDisplayStrategy
from hwut.strategies.info       import InfoStrategy
from hwut.strategies.test       import TestExecutionStrategy
# TODO: from hwut.strategies.zip        import ZipStrategy


class Setup:
    def __init__(self, cl):
        self.program_name  = get_next_nominus(cl)
        self.choice        = get_next_nominus(cl)
        self.execution_f            = cl.search("-e", "--exec")
        self.failed_only_f          = cl.search("--fail")
	self.compression_f          = cl.search("--compress")

        if cl.search("--no-grant"): self.grant = "NONE"  # "no grant" overrides "grant" for safety
        elif cl.search("--grant"):  self.grant = "ALL"
        else:                       self.grant = "INTERACTIVE"

	if cl.search("--clean"):          self.make_target = "clean"
	elif cl.search("--mostly-clean"): self.make_target = "mostlyclean"
        elif cl.search("--make"):         self.make_target = get_next_nominus(cl)





def execute_test(cl):
    setup = Setup(cl)
    core.run(setup, TestExecutionStrategy(setup))

def accept(cl):
    setup = Setup(cl)
    core.run(setup, AcceptStrategy(setup))

def difference(cl, DiffProgramName):
    # call this function first, to make sure we grab the next argument
    diff_program_name = get_next_nominus(cl)

    # resolve abreviations:
    try:
	diff_program_name = {
		"":         "diff",
		"diff":     "diff",
		"v":        "vimdiff",
		"vimdiff":  "vimdiff",
		"gv":       "gvimdiff",
		"gvimdiff": "gvimdiff",
		"tk":       "tkdiff",
		"tkdiff":   "tkdiff",
		}[diff_program_name]
    except:
	io.on_unknown_diff_program(diff_program_name)

    setup = Setup(cl)
    setup.diff_program_name = diff_program_name

    core.run(setup, DifferenceDisplayStrategy(setup))

def clean(cl, CleanMakeTarget):
    setup = Setup(cl)
    assert setup.make_clean_target in ["clean", "mostlyclean"]
    core.run(setup, CleanStrategy(setup))

def info(cl):
    setup = Setup(cl)
    core.run(setup, InfoStrategy(setup))

def __check_unrecognized_options(cl):
    ufos = cl.unidentified_options("-v", "--version",
                                   "-h", "--help",
				   #
                                   "d",  "diff", 
                                   "c",  "clean", 
				   "mc", "mostly-clean", 
                                   "a",  "accept", 
                                   "i",  "info",
				   #
                                   "-e", "--exec", 
				   "--make",
                                   "--grant", "--no-grant",   # avoid interaction 'yes', 'no', 'all' ...
                                   "--fail")
    if ufos != []:
	print "Error: unidentified command line option(s):"
        print ufos
        sys.exit(-1)

def get_next_nominus(cl):
    cl.search_failed_f = False  # otherwise the 'next()' command wont work
    #                                # in case no flag was tested before
    txt = cl.next("")
    if len(txt) > 1 and txt[0] == "-": return ""
    else:                              return txt

if __name__ == "__main__":    
    cl = GetPot(sys.argv)

    # -- define the home directory as the directory where hwut was called
    directory.init_home()

    # -- initialize the database
    common.application_db = TestApplicationDB()

    # -- comment on any ufo
    __check_unrecognized_options(cl)

    if   cl.search("-v", "--version"):   help.print_version()
    elif cl.search("-h", "--help"):      help.do()
    #
    elif cl[1] in ["i", "info"]:         cl.search(cl[1]); info(cl)
    elif cl[1] in ["d", "diff"]:         cl.search(cl[1]); difference(cl, "diff")
    elif cl[1] in ["c", "clean"]:        cl.search(cl[1]); clean(cl, "clean")
    elif cl[1] in ["m", "mostly-clean"]: cl.search(cl[1]); clean(cl, "mostyclean")
    elif cl[1] in ["a", "accept"]:       cl.search(cl[1]); accept(cl)
    #
    else:                                execute_test(cl)


    print "<terminated>"

