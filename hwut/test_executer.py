import sys
import os
from   hwut.aux    import execute_this,          \
	                  get_protocol_filename, \
			  ensure_dot_slash
import hwut.common as common

def do(TestProgram, Choice, CreateOnlyOutputF=False):
    """RETURNS:
          True   output of program and expected output are equal
	  False  output of program and expected output differ
          None   no decision can be made
    """
    # (*) run the test program
    test_output = __run_program(TestProgram, Choice)
    if test_output == -1: return None
    
    description_str = TestProgram
    if Choice != "": description_str += " " + Choice

    if CreateOnlyOutputF: return None

    # (*) compare with expectation
    result = __compare_result(test_output, TestProgram, Choice)
    if result == False: common.failed_test_list.append(description_str)
    return result

def __compare_result(TestOutput, TestProgram, Choice):
    # (*) compare with expectation
    TestProgramProt = get_protocol_filename(TestProgram, Choice) 
    try:
	expected_result = open("GOOD/" + TestProgramProt).read()    
    except:
	sys.stdout.write("\n    error: no file 'GOOD/%s'\n" % TestProgramProt)
	dir = os.getcwd()
	if common.missing_good_files.has_key(dir): 
	    common.missing_good_files[dir].append(TestProgramProt)
	else:                               
	    common.missing_good_files[dir] = [ TestProgramProt ]
	return

    # -- avoid confusion with 'carriage return/line feed' on different
    #    operating systems
    result_str   = TestOutput.replace("\r\n", "\n")
    expected_str = expected_result.replace("\r\n", "\n")

    return result_str == expected_str

def __run_program(program_name, Choice):
    """Runs a test program and returns the whole output as a single string."""
    filename = "./OUT/" + get_protocol_filename(program_name, Choice)

    program_name = ensure_dot_slash(program_name) 

    try:
        result_str = execute_this(program_name, [Choice], filename)    
    except:
        sys.stdout.write("\nerror: program '%s' is not executable (or does not exists)\n" % program_name + \
			 "error:\n" + \
		         "error: current directory = " + os.getcwd() + "\n" + \
			 "error: choice            = " + Choice + "\n" + \
			 "error:\n" + \
			 "error: -- Is this a script and you forgot to specify your interpreter?\n" + \
			 "error:    If so, type '#! /usr/bin/env my_interpreter' in the first line of your file.\n" + \
			 "error: -- Or, maybe, release the executable flag, so it wont be considered a test file!\n")
	sys.exit(-1)

    return result_str

