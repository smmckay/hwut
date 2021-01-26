import sys
import time

from   hwut.frs_py.string_handling import trim

def print_ok(Dir):
    sys.stdout.write("---------------------------------------------------------------------------------\n")
    print "  ___  _ _   _  __                        _     _" 
    print " / _ \| | | | |/ /___  _ __ _ __ ___  ___| |_  | |"
    print "| | | | | | | ' // _ \| '__| '__/ _ \/ __| __| | |"
    print "| |_| | | | | . \ (_) | |  | | |  __/ (__| |_  |_|"
    print " \___/|_|_| |_|\_\___/|_|  |_|  \___|\___|\__| (_)"
    print  

def print_failure(Dir, FailedTestList):
    sys.stdout.write("---------------------------------------------------------------------------------\n")
    print " _____     _ _                  _" 
    print "|  ___|_ _(_) |_   _ _ __ ___  | |"
    print "| |_ / _` | | | | | | '__/ _ \ | |"
    print "|  _| (_| | | | |_| | | |  __/ |_|"
    print "|_|  \__,_|_|_|\__,_|_|  \___| (_)"
    print
    for name in FailedTestList:
    	print "error: " + name

def request_copy_OUT_to_GOOD(Dir, ProtocolFileName):

    print 
    print "Copy:  %s/OUT/%s" % (Dir, ProtocolFileName)
    print "to:    %s/GOOD/ ?" % Dir
    print "Note, that this means that it is taken for reference during any later unit test!"
    print "('yes', 'all', 'no', 'none')"

    return trim(sys.stdin.readline()).upper()

def print_summary(ResultDict):
    """ResultDict = directory --> result (True if all OK, else False)
    """
    if len(ResultDict.keys()) <= 1: return

    print "SUMMARY:"
    L = max(map(lambda x: len(x), ResultDict.keys()))
    for dir, result_f in ResultDict.items():
	if result_f == True: judgement = "[OK]"
	else:                judgement = "[FAIL]"
	
	print dir + "." * (L + 4 - len(dir)) + judgement

def on_directory_enter(Dir, HWUT_TITLE_FILE):
    
    # -- print title of the tests in the given directory
    try:
	fh = open(HWUT_TITLE_FILE)
	print fh.read()
	fh.close()
    except:
	print "<no file '%s'>" % HWUT_TITLE_FILE
    
    # -- print basic information about the directory
    print "DIR:  " + Dir
    print "DATE: " + time.asctime()

def on_directory_terminated(ResultF, Dir, FailedTestList):
    if ResultF == False: print_failure(Dir, FailedTestList)
    else:                print_ok(Dir)

    sys.stdout.write("---------------------------------------------------------------------------------\n")

def on_test_group_start(GroupName):
    if GroupName != "": 
	sys.stdout.write("\n -- %s:\n\n" % GroupName)

def on_test_start(GroupedF, entry):
    if GroupedF != "": sys.stdout.write("    %s\n" % entry.title)
    else:              sys.stdout.write(" -- %s\n" % entry.title)

def on_test_end(Result, TestProgram, Choice="", FirstF=None):
    if Choice != "":
	if not FirstF: Label = " " * len(TestProgram) + " " + Choice
	else:          Label = TestProgram + " " + Choice
    else:              Label = TestProgram

    sys.stdout.write("    %s " % Label)
    TitleL = len(Label)
    if TitleL < 72: sys.stdout.write("." * (63-TitleL))

    if   Result == True:           sys.stdout.write(".........[OK]\n")
    elif Result == False:          sys.stdout.write(".......[FAIL]\n") 
    elif Result == "MAKE FAILED":  sys.stdout.write("[MAKE FAILED]\n")
    else:                          sys.stdout.write(".......[DONE]\n") 

def on_update_program_entry_info(Filename):
    print "// update: call '%s --hwut-info'" % Filename

def on_update_program_entry_info_all_terminated():
    print  # newline after possible "// update:" messages

def on_copied_OUT_to_GOOD(Dir, ProtocolFileName):
    print "copied: %sOUT/%s to %sGOOD/" % (Dir, ProtocolFileName, Dir) 

def on_enter_directory_of_missing_good_files(Dir, FileList):
    print "DIR: " + Dir
    print "The following files have no entry in their 'GOOD' directories:"
    print
    for file in FileList:
	print "    " + file
    print 

def on_raise_write_protection(Dir, Filename):
    sys.stdout.write("set write protection for '%s/%s'\n" % (Dir, Filename)) 

def on_no_test_program_specified():
    print "error: no test program specified"

def on_file_access_error(Filename):
    print "error: file '%s'" % Filename
    print "error: cannot be accessed." 

def on_file_does_not_exist(Filename):
    print "error: file '%s'" % Filename
    print "error: does not exists." 

def on_error_make_failed(Bunch):
    for program in Bunch:
	print "error: make failed on '%s'" % program

def on_make_bunch_of_test_programs(Bunch):
    for program in Bunch:
	print "make: %s" % program

def on_choice_not_available(Choice, TestProgramName):
    print "error: program '%s' does not provide choice '%s'" % (TestProgramName, Choice)

def on_makefile_does_not_contain_target_hwut_info(Directory):
    print "error: Makefile in directory '%s'" % Directory
    print "error: does not report test file list for target 'hwut-info'. Please, add something" 
    print "error: like the following lines to your makefile:"
    print "error:"
    print "error: FILE_LIST = my_test-1 my_test-2 my_test-3 ... my_test-N"
    print "error:"
    print "error: ..."
    print "error:"
    print "error: hwut-info:"
    print "error:     @echo $(FILE_LIST)"
    print "error:"
    print "error: Hwut expects if it says 'make hwut-info', then it gets a list of files"
    print "error: that are to be built."

