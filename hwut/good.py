#! /usr/bin/env python
#
# PURPOSE: Runs all test scripts and reports results.
#
# (C) 2006, 2007 Frank-Rene Schaefer
#
# ABSOLUTELY NO WARRANTY
################################################################################
import os
import stat
import sys

from hwut.frs_py.string_handling import trim

import hwut.common    as common
import hwut.directory as directory
import hwut.io        as io
import hwut.aux       as aux
import hwut.test_executer as test_executer

def __copy_to_GOOD(Dir, ProtocolFileName, InteractF=True):	
    """RETURN: 
           ALL  -- user wants all files to be copied.
           NONE -- user wants no single file to be copied

       assume Dir = current directory
    """
	
    relative_dir = "." + Dir.replace(common.home_directory, "")

    reply = "YES"
    if InteractF: 
	reply = io.request_copy_OUT_to_GOOD(relative_dir, ProtocolFileName)

    if reply in ["YES", "ALL"]:

	if os.access("GOOD/%s" % ProtocolFileName, os.F_OK):
	    os.chmod("GOOD/%s" % ProtocolFileName, stat.S_IWRITE)

	if not os.access("OUT/%s" % ProtocolFileName, os.F_OK):
	    io.on_file_does_not_exist("OUT/%s" % ProtocolFileName)
	    return "NO"

	os.system("cp OUT/%s GOOD/"   % ProtocolFileName)
	if not os.access("GOOD/%s" % ProtocolFileName, os.F_OK):
	    io.on_file_access_error("GOOD/%s" % ProtocolFileName)
	    return "NO"

	os.chmod("GOOD/%s" % ProtocolFileName, stat.S_IREAD)
    
	io.on_copied_OUT_to_GOOD(relative_dir, ProtocolFileName)

    return reply

def accept(Dir, ProgramName, Choice, ExecuteF=False):
    """Copies the content of an output file in OUT/ to the directory GOOD/.
       This means that the content of the output file is to be considered as 'good'.
       ARGV contains the list of arguments passed to this program from the 
       command line. 
    """
    if not (type(ProgramName) == str and ProgramName != ""): 
	io.on_no_test_program_specified()
	return

    if ExecuteF: 
	test_executer.do(ProgramName, Choice, CreateOnlyOutputF=True) 

    __copy_to_GOOD(Dir, aux.get_protocol_filename(ProgramName, Choice))	

def accept_all(Dir, ExecuteF=True):

    directory.go(Dir) 

    # -- read content of cache file for current directory into the info_db
    common.info_db.read()
    failed_program_list = directory.__get_failed_program_list()
    #
    directory.do(Dir, CreateOnlyOutputF=True, FailedOnlyF=True)

    for entry in common.info_db.extract_entries(failed_program_list):
        program_name = entry.file_name
        if entry.choices == []:
	    __copy_to_GOOD(Dir, get_protocol_filename(program_name, ""))	
	else:
	    interaction_f = True
	    for choice in entry.choices:
	        user_reply = __copy_to_GOOD(Dir, aux.get_protocol_filename(program_name, choice), interaction_f)	
		if user_reply == "ALL":  interaction_f = False
		if user_reply == "NONE": break

def request_acceptance_for_missing_GOOD_files():
    """Asks user if the files for which there are no 'GOOD' files can be 
       copied into the ./GOOD/ directory.
    """   
    for dir, file_list in common.missing_good_files.items():
	directory.go(dir)
	io.on_enter_directory_of_missing_good_files(dir, file_list)

	interact_f = True
	for file in file_list:
	    reply = __copy_to_GOOD(dir, file, InteractF=interact_f)
	    if reply == "ALL":  interact_f = False
	    if reply == "NONE": break
