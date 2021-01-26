#! /usr/bin/env python
#
# PURPOSE: Runs all test scripts and reports results.
#
# (C) 2006, 2007 Frank-Rene Schaefer
# ABSOLUTELY NO WARRANTY
################################################################################
import sys
import os

from frs_py.string_handling import trim
from GetPot                 import GetPot
#
import hwut.aux        as aux
import hwut.directory  as directory
import hwut.io         as io
import hwut.good       as good
import hwut.difference as difference
import hwut.common     as common

def clean_all_TEST_subdirectories():
    test_dir_list = aux.get_TEST_directories()

    to_be_deleted_list = []
    for dir in test_dir_list:
	file_list = aux.get_hwut_unrelated_files_in_GOOD_and_OUT(dir)
	to_be_deleted_list.extend(map(lambda f: dir + f, file_list))

def run_all_TEST_subdirectories(AcceptAllF=False, FailedOnlyF=False):
    test_dir_list = aux.get_TEST_directories()

    result_dict = {}
    for dir in test_dir_list:
	result_dict[dir] = directory.do(dir, AcceptAllF, FailedOnlyF)

    # -- print result
    io.print_summary(result_dict)

    if not AcceptAllF:
	# -- interact with user on missing good files	    
	good.request_acceptance_for_missing_GOOD_files()


def __check_unrecognized_options(command_line):
    ufos = command_line.unidentified_options("-v", "--version",
	                                     "-h", "--help",
					     "-d", "--diff", "--vi", "--vimdiff", 
					     "-e", "--exec", "--clean", 
					     "--good", "--all-good",
					     "--errors", "--error")
    if ufos != []:
	print "unidentified command line option(s):"
	print ufos
	sys.exit(-1)


if __name__ == "__main__":    

    cl = GetPot(sys.argv)
    def __next_nominus():
	txt = cl.next("")
	if len(txt) > 1 and txt[0] == "-": return ""
	else:                              return txt

    # -- define the home directory as the directory where hwut was called
    directory.init_home()

    __check_unrecognized_options(cl)

    if   cl.search("-v", "--version"): 
	help.print_version()

    elif cl.search("-h", "--help"):    
	help.do()
    
    elif cl.search("-d", "--diff"):    
	difference.show(__next_nominus(), __next_nominus(), "diff", ExecuteF = cl.search("-e", "--exec"))
	sys.exit(0)

    elif cl.search("--vi", "--vimdiff"):
	difference.show(__next_nominus(), __next_nominus(), "vimdiff", ExecuteF = cl.search("-e", "--exec"))
	sys.exit(0)

    elif cl.search("--clean"):     
	clean_all_TEST_subdirectories()

    elif cl.search("--good"):      
	good.accept(os.getcwd(), __next_nominus(), __next_nominus(), cl.search("-e", "--exec"))

    elif cl.search("--all-good"):  
	run_all_TEST_subdirectories(AcceptAllF=True)	

    elif cl.search("--error", "--errors"):
	run_all_TEST_subdirectories(FailedOnlyF = True)

    else:
	# -- single test, or test the whole tree?
	arg1 = cl.get(1, "")
	arg2 = cl.get(2, "")

	test_name = ""
	choice    = ""
	if len(arg1) > 1 and arg1[0] != "-": test_name = arg1
	if len(arg2) > 1 and arg2[0] != "-": choice    = arg2

	if test_name != "":	
	    directory.go("./")
	    directory.do_single(common.home_directory, test_name, choice)
	    good.request_acceptance_for_missing_GOOD_files()
	else:
	    run_all_TEST_subdirectories(FailedOnlyF = False)


    print "<terminated>"

