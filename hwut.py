#! /usr/bin/env python
#
# PURPOSE: runs all test scripts and reports results.
# (C) 2006 Frank-Rene Schaefer
# ABSOLUTELY NO WARRANTY
################################################################################
import sys
import os
import stat
import re
import time
import subprocess
import StringIO

from frs_py.string_handling import trim

HWUT_VERSION = "0.2.1"

error_test_list = []
error_f = False

class TestProgram:
    def __init__(self, FileName, SectionTitle, Title):
    	self.file_name     = FileName
    	self.section_title = SectionTitle
        self.title         = Title

def do(TestProgramList, CreateOnlyOutputF=False):
    for section, test_program_list in TestProgramList.items():    
        if section != "": sys.stdout.write("\n -- %s\n" % section)
	for program in test_program_list:
	    if section != "": sys.stdout.write("    ")
	    else:             sys.stdout.write(" -- ")
            sys.stdout.write(program.title + "\n")
            perform_test(program.file_name, CreateOnlyOutputF)   
            sys.stdout.write("\n") 
    
def perform_test(test_program, CreateOnlyOutputF=False):    
    """Performs a test and returns an object of type 'TestInfo'
       containing also the result of the test.
    """
    global error_f
    # (*) run the test program
    if len(test_program) < 2 or test_program[:2] != "./": 
	test_program = "./" + test_program
    test_result = run_program(test_program)
    if test_result == -1: return

    if CreateOnlyOutputF: sys.stdout.write("\n"); return
    
    # (*) compare with expectation
    try:
        expected_result = open("GOOD/" + test_program + ".txt").read()    
    except:
        sys.stdout.write("\n  error: no file 'GOOD/%s'" % (test_program + ".txt"))
        return

    # -- avoid confusion with 'carriage return/line feed' on different
    #    operating systems
    result_str   = test_result.replace("\n\r", "\n")
    expected_str = expected_result.replace("\n\r", "\n")
    # -- substitute debug output with empty string
    # COMMENT_TO_NEWLINE = re.compile("^\s*##.*\n", re.MULTILINE)
    # COMMENT_RANGE = re.compile("^\s*/\*.*<\*/\s*\n", re.MULTILINE)
    # result_str = COMMENT_TO_NEWLINE.sub("", result_str) 
    # expect_str = COMMENT_TO_NEWLINE.sub("", expected_str)
    # result_str = COMMENT_RANGE.sub("", result_str) 
    # expect_str = COMMENT_RANGE.sub("", expected_str)

    # (*) print the result (nicely formatted)
    sys.stdout.write("    %s " % test_program)
    TitleL = len(test_program)
    if TitleL < 72: sys.stdout.write("." * (72-TitleL))
    if result_str == expected_str: 
    	sys.stdout.write("[OK]\n")
    else:
	sys.stdout.write("[FAIL]\n"); 
	error_f = True;  
	error_test_list.append(test_program)

def find(Dir, OptionStr):
    """Search for all files with executable rights in the given directory."""    
    fh = open("HWUT-test-file-list.tmp", "w")

    if OptionStr.find("-type") == -1:     OptionStr = "-type f " + OptionStr
    if OptionStr.find("-mindepth") == -1: OptionStr = "-maxdepth 1 " + OptionStr
    
    subprocess.call(["find", Dir] + OptionStr.split(), stdout = fh)

    fh.close()
    fh = open("HWUT-test-file-list.tmp")
    
    file_list_str = fh.read()  
    fh.close()
    
    # return list of files
    return file_list_str.split()

def get_program_list():
    """get all executable files in current directory """
    sorted_list = find("./", "-perm +u+x")
    # exclude the 'HWUT' file from consideration
    sorted_list = filter(lambda x: os.path.basename(x).find("HWUT") != 0, sorted_list)
    # sort the test program files 
    sorted_list.sort()
    
    # -- arrange tests with the same text before the ':' to groups
    group_map = {}
    def add_program(name, section, title):
        if group_map.has_key(section):
     	    group_map[section].append(TestProgram(program, section_title, title))	    
        else:
	    group_map[section] = [ TestProgram(program, section_title, title) ]
	
    for program in sorted_list:
	# (*) get information about the test
        program = program.replace("\n", " ")
	info = run_program(program, ["--test-info"])
	# 
        field_list = info.split(":")
	field_list = map(trim, field_list)
        if len(field_list) > 1: section_title = field_list[0]; title = field_list[1]
        else:                   section_title = ""; title = field_list[0]
	add_program(program, section_title, title)

    return group_map 

def raise_write_protection(Dir):
    """find files in Dir that are not write protected"""
    unprotected_files = find(Dir, "-perm +u+w")    
    for file in unprotected_files:
        sys.stdout.write("set write protection for '%s'\n" % file) 
	os.chmod(file, stat.S_IREAD)

def print_over_title():
    try:
        fh = open("HWUT-INFO.txt")
	print fh.read()
        fh.close()
    except:
        print "<no file 'HWUT-INFO.txt>"
    
def run_program(program_name, args=[]):
    """Runs a program and returns the whole output as a single string."""
    result_fh = open("OUT/" + program_name + ".txt", "w")
    try:
        subprocess.call([program_name] + args, stdout = result_fh)    
    except:
        sys.stdout.write("\nerror: program '%s' is not executable (or does not exists)\n" % program_name)
	return -1
    result_fh.close()
    result_fh = open("OUT/" + program_name + ".txt")
    result_str = result_fh.read()
    result_fh.close()
    return result_str

def aux_show_difference(ARGV):
    """Shows the difference between an output file and the stored 'good' file.
       ARGV contains the list of arguments passed to this program from the 
       command line. It is expected that the name of the program under 
       concern directly follows the '--diff' option.
    """
    arg_position = ARGV.index("--diff")
    if len(ARGV) <= arg_position + 1:
 	print "'--diff' option requires a filename"
	sys.exit(-1)

    program_name = ARGV[arg_position + 1]

    # if '--exec' option is given than execute the program
    if "--exec" in ARGV or "-e" in ARGV: 
	perform_test(program_name, CreateOnlyOutputF=True) 
    
    os.system("diff OUT/%s.txt GOOD/%s.txt" % (program_name, program_name))
    
def aux_let_it_be_good(ARGV):
    """Copies the content of an output file in OUT/ to the directory GOOD/.
       This means that the content of the output file is to be considered as 'good'.
       ARGV contains the list of arguments passed to this program from the 
       command line. It is expected that the name of the program under 
       concern directly follows the '--diff' option.
    """
    arg_position = ARGV.index("--good")
    if len(ARGV) <= arg_position + 1:
 	print "'--good' option requires a filename"
	sys.exit(-1)
    program_name = ARGV[arg_position + 1]
    # if '--exec' option is given than execute the program
    if "--exec" in ARGV or "-e" in ARGV: 
	perform_test(program_name, CreateOnlyOutputF=True) 
	
    print "Are you sure that you want to copy the file 'OUT/%s.txt'" % program_name
    print "into the directory 'GOOD/'? Note, that this means that it is"
    print "taken for reference for any later unit test!\n(type 'yes' if so)"
    reply = sys.stdin.readline()
    if reply.find("yes") != 0: 
        print "<nothing is copied>"
	return
    os.system("chmod u+w GOOD/%s.txt" % program_name)
    os.system("cp OUT/%s.txt GOOD/" % program_name)
    os.system("chmod u-w GOOD/%s.txt" % program_name)
    
    #os.system("chmod u-w GOOD/%s.txt" % program_name)
    print "<copy accomplished>"

def aux_clean_directories():
     """Cleans sub-directories ./GOOD and ./OUT from any file that does not
        have an executable in the current directory.
     """	
     test_programs        = find("./", "-perm +u+x")
     test_program_outputs = map(lambda x: os.path.basename(x) + ".txt", test_programs)
     to_be_deleted_list = []
     for subdir in ["./GOOD", "./OUT"]:
	 # get all files in the directory and watch if the correspond to the test files
	 files = find("./" + subdir, "-type f")
	 files = map(lambda x: os.path.basename(x), files)
  	 nonsense_files = filter(lambda x: x not in test_program_outputs, files)	
	 to_be_deleted_list.extend(map(lambda x: subdir + "/" + x, nonsense_files))

     print "None of the following files is currently important to unit testing:"
     file_str = ""
     for file in to_be_deleted_list:
	 print file
	 file_str += file + " "
     print "Are you sure, that you want to delete all of the above files?"
     reply = sys.stdin.readline()
     if reply.find("yes") != 0: 
         print "<nothing is deleted>"
 	 return

     # set write permissions
     os.system("chmod u+w " + file_str)
     # delete the files
     os.system("rm " + file_str)
     print "<clean accomplished>"

def aux_let_all_be_good(test_file_list):
     do(test_file_list, True)
     print "Are you sure, that you want to try to copy all files from ./OUT to ./GOOD ?"
     print "(existing files in ./GOOD with write protection intact will be left as they are)"
     reply = sys.stdin.readline()
     if reply.find("yes") != 0: 
         print "<nothing is copied>"
 	 return

     os.system("cp ./OUT/* ./GOOD/")
     print "<copy accomplished>"
     
def aux_ensure_directory_structure():
    """Makes sure that ./OUT and ./GOOD exist in the current directory."""
    directories = find("./", "-type d")
    if "./GOOD" not in directories: os.system("mkdir ./GOOD")
    if "./OUT" not in directories:  os.system("mkdir ./OUT")
     
def print_ok():
    sys.stdout.write("---------------------------------------------------------------------------------\n")
    print "  ___  _ _   _  __                        _     _" 
    print " / _ \| | | | |/ /___  _ __ _ __ ___  ___| |_  | |"
    print "| | | | | | | ' // _ \| '__| '__/ _ \/ __| __| | |"
    print "| |_| | | | | . \ (_) | |  | | |  __/ (__| |_  |_|"
    print " \___/|_|_| |_|\_\___/|_|  |_|  \___|\___|\__| (_)"
    print  

def print_failure():
    sys.stdout.write("---------------------------------------------------------------------------------\n")
    print " _____     _ _                  _" 
    print "|  ___|_ _(_) |_   _ _ __ ___  | |"
    print "| |_ / _` | | | | | | '__/ _ \ | |"
    print "|  _| (_| | | | |_| | | |  __/ |_|"
    print "|_|  \__,_|_|_|\__,_|_|  \___| (_)"
    print
    for name in error_test_list:
    	print "error: " + name

def hwut_core():
    """What HWUT does when it is in a ./TEST directory ...
       RETURNS:  True if all tests in the directory went well
                 False if not
    """
    global error_test_list
    global error_f
    error_test_list = []
    error_f = False

    aux_ensure_directory_structure()
    if "--diff" in sys.argv: aux_show_difference(sys.argv); sys.exit(0)
    if "--good" in sys.argv: aux_let_it_be_good(sys.argv); sys.exit(0)
    if "--clean" in sys.argv: aux_clean_directories(); sys.exit(0)
    print_over_title()

    # check, if there is a makefile, if so do 'make all'
    if find("./", "-name \"[mM]akefile\"") != []: os.system("make all")

    # find all executable files in directory
    test_file_list = get_program_list()

    # if '--all-good' is specified then no comparison is done with expectation
    # use the flag to create output files that can be copied to 'good'.
    if "--all-good" in sys.argv: 
    	aux_let_all_be_good(test_file_list)
    else:
	do(test_file_list)
        if error_f: print_failure()
        else:       print_ok()

    # for safety: lock all files for good in directory GOOD/
    sys.stdout.write("---------------------------------------------------------------------------------\n")
    raise_write_protection("./GOOD")

    # check, if there is a makefile, if so do 'make clean'
    if find("./", "-name \"[mM]akefile\"") != []: os.system("make clean")

    return not error_f

def aux_help():
    print "H.W.U.T. - The Hello-Worldler's Unit Test"
    print ""
    print "USAGE:"
    print "         > HWUT [options]"
    print ""
    print "OPTIONS:"
    print ""
    print "   -v, --version   Version of the H.W.U.T. program."
    print ""
    print "   -h, --help      This help."
    print ""
    print "   --diff executable-filename"
    print "       Shows the differences between the good and the current output of the unit test."
    print ""
    print "   --good executable-filename"
    print "       Takes the current output of the unit test for good."
    print ""
    print "   --clean"
    print "        Cleans the directories ./OUT and ./GOOD from trailing files."
    print ""
    print "   --all-good"
    print "        Takes all unit tests that are currently to be executed for good."
    print ""
    print "   --exec"
    print "        If used after the --good or --diff option the unit test is executed again."
    print "        Otherwise, the output from the ./OUT directory is taken."
    print ""



if __name__ == "__main__":    
    
    TEST_DIR_NAME = "TEST"

    if "-v" in sys.argv or "--version" in sys.argv:
	print "HWUT Version " + HWUT_VERSION
	sys.exit(0)

    if "-h" in sys.argv or "--help" in sys.argv:
	aux_help()
	sys.exit(0)
    
    # -- find all sub-dirs that are ./TEST-directories
    test_dir_list = find("./", "-mindepth 1  -name TEST -type d")

    # -- take only those directories that end with "/TEST"
    test_dir_list = filter(lambda x: 
	                   len(x) >= len("/TEST") and x[-len("/TEST"):] == "/TEST",
			   test_dir_list)
 
    # -- add the current directory, if it is called 'TEST'
    if os.access("../TEST", os.F_OK): test_dir_list.append("./")

    result_dict = {}
    home_dir = os.getcwd()
    for dir in test_dir_list:
	# all directories are relative to where we started, thus gome first home ...
	print "DIR:  " + dir
	print "DATE: " + time.asctime()
	os.chdir(home_dir)
	os.chdir(dir)
        result_dict[dir] = hwut_core() 

    # -- print result
    if len(test_dir_list) > 1:
	print "SUMMARY:"
	L = max(map(lambda x: len(x), test_dir_list))
	for dir in test_dir_list:
	    if result_dict[dir] == True: judgement = "[OK]"
	    else:                        judgement = "[FAIL]"
	    
	    print dir + "." * (L-len(dir)) + judgement
