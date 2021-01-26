import os
import sys

import hwut.common as common

from   hwut.frs_py.string_handling import trim
from   hwut.strategies.core        import test_info

__home_directory = ""  # updated by 'core.do_directory_tree()'

def __get_relative_directory(Dir):
    return "." + Dir.replace(__home_directory, "")

def print_line_separator():
    sys.stdout.write("--------------------------------------------------------------------------------------\n")

def print_double_line_separator():
    sys.stdout.write("======================================================================================\n")

def print_ok(Dir):
    print_line_separator()
    print "  ___  _ _   _  __                        _     _" 
    print " / _ \| | | | |/ /___  _ __ _ __ ___  ___| |_  | |"
    print "| | | | | | | ' // _ \| '__| '__/ _ \/ __| __| | |"
    print "| |_| | | | | . \ (_) | |  | | |  __/ (__| |_  |_|"
    print " \___/|_|_| |_|\_\___/|_|  |_|  \___|\___|\__| (_)"
    print  

def print_failure(Dir, FailedTestList):
    assert type(FailedTestList) == list
    assert map(lambda x: x.__class__.__name__, FailedTestList) == ["test_info"] * len(FailedTestList), \
           "received: " + repr(map(type, FailedTestList))
    print_line_separator()
    print " _____     _ _                  _" 
    print "|  ___|_ _(_) |_   _ _ __ ___  | |"
    print "| |_ / _` | | | | | | '__/ _ \ | |"
    print "|  _| (_| | | | |_| | | |  __/ |_|"
    print "|_|  \__,_|_|_|\__,_|_|  \___| (_)"
    print
    for test_element in FailedTestList:
        print "error: " + test_element.program + " " + test_element.choice

def request_copy_OUT_to_GOOD(ProtocolFileName):
    Dir = __get_relative_directory(os.getcwd())
    print 
    print "     Copy:  %s/OUT/%s" % (Dir, ProtocolFileName)
    print "     to:    %s/GOOD/ ?" % Dir
    print "     Note, that this means that it is taken for reference during any later unit test!"
    print "     ('yes', 'all', 'no', 'none', simply [Return] means 'no')"
    print "     ",

    return trim(sys.stdin.readline()).upper()

def request_accept_all_remaining_test_programs(RemainingTestPrograms):
    print 
    print "Remaining Test Programs:"
    for program_name in RemainingTestPrograms:
        print "    ", program_name
    print "Do you want to accept all choices of all remaining test programs?"
    print "('yes', 'no')"
    return trim(sys.stdin.readline()).upper()

def request_not_accept_all_remaining_test_programs(RemainingTestPrograms):
    print 
    print "Remaining Test Programs:"
    for program_name in RemainingTestPrograms:
        print "    ", program_name
    print "Do you want to drop remaining test programs from consideration?"
    print "('yes', 'no')"
    return trim(sys.stdin.readline()).upper()

def request_file_list_deletion(Dir, FilenameList):
    """Returns a list of indeces or index-ranges indexing the files
       in the file name list that are to be deleted.
    """
    print "Following files are to be deleted:"
    print
    print "[index]  filename:"
    for file_name in FilenameList:
	print "[%05i]: %s" % (i, file_name)

    print "Specify files to be deleted by their indices. Type 'all' to delete all."
    print "Example: 5                  deletes file number '5'"
    print "         5-10               deletes file number 5, 6, 7, 8, 9, and 10."
    print "         3, 5-8, 24, 27-30  deletes file number 3, 5, 6, 7, 8, 24, 27, 28, 29, 30"
    print 

    user_response = trim(sys.stdin.readline()).upper()
    if user_response == "ALL": return range(len(FilenameList))

    response_list = response.split(",")
    result = []
    for response in response_list:
	fields = map(trim, response.split("-"))
	if fields.isdigit() == False:
	    io.on_invalid_response(response)
	    return []
	if len(fields)   == 1:
	    result.append(int(fields[0]))
	elif len(fields) == 2:
	    result.append(range(int(fields[0]), int(fields[1]) + 1))
	else:
	    on_invalid_response(response)
	    return []
 
    return result


def on_invalid_response(Response):
    print "Error: User response invalid."
    print "Error: '%s'" % Response

def print_summary(Directory_vs_Result_Pairs):
    print_double_line_separator()
    print "SUMMARY:"
    L = max(30, max(map(lambda x: len(x[0]), Directory_vs_Result_Pairs)))

    for dir, result in Directory_vs_Result_Pairs:
        if   result == "OK":   judgement = "[OK]"
	elif result == "DONE": judgement = "[DONE]"
        else:                  judgement = "[FAIL]"
        
	if dir == "./": dir = "(this directory)"
        print dir + " " + "." * (L + 4 - len(dir)) + judgement
    print_double_line_separator()

def on_directory_enter(Dir, DateStr):
    
    print_double_line_separator()
    
    # -- print basic information about the directory
    print "ENTER: " + __get_relative_directory(Dir)
    print "DATE:  " + DateStr
    txt = "TITLE: "

    # -- print title of the tests in the given directory
    try:
        fh = open(common.HWUT_TITLE_FILE)
        txt += fh.read()
        fh.close()
    except:
        txt += "<no file '%s'>" % common.HWUT_TITLE_FILE
    print txt

def on_directory_terminated(Dir):
    print "EXIT:  " + __get_relative_directory(Dir)


class ParallelizedTestOutputManager:
    last_reported_id = -1
    delayed_output   = {}
    done_id_list     = []

    def init(self):
        self.last_reported_id = -1
        self.delayed_output   = {}
        self.done_id_list     = []

    def register(self, ID, Txt):
        if self.delayed_output.has_key(ID): self.delayed_output[ID] += Txt
        else:                               self.delayed_output[ID] = Txt

    def register_test_end(self, ID, Txt):
        assert self.delayed_output.has_key(ID), \
               "test '%i' ended before it was even started." % ID

        self.delayed_output[ID] += Txt
        assert ID not in self.done_id_list
        self.done_id_list.append(ID)
        self.conditional_flush()

    def conditional_flush(self):
        self.done_id_list.sort()

        deletion_list = []
        for id in self.done_id_list:
            if id != self.last_reported_id + 1: 
                break
            # print out the output that was delayed until it could be printed
            # in propper sequence
            sys.stdout.write(self.delayed_output[id])
            deletion_list.append(id)
            self.last_reported_id = id

        for id in deletion_list:
            del self.delayed_output[id]
            del self.done_id_list[self.done_id_list.index(id)]

output_man = ParallelizedTestOutputManager()

def on_test_sequence_start():
    print_line_separator()
    output_man.init()

def on_test_start(TestInfo, DoNotGroupF=False):
    """GroupElementF = False allows to categorically block a decision wether 
       to treat the test as part of a group or not.
    """
    if DoNotGroupF: GroupedF = False
    else:           GroupedF = TestInfo.group != ""

    entry = TestInfo.related_entry
    if TestInfo.choice_idx != 0:
	output_man.register(TestInfo.execution_id, "")
    else:
	if GroupedF: 
	    output_man.register(TestInfo.execution_id, "    %s\n" % entry.title)
	else:   
	    output_man.register(TestInfo.execution_id, " -- %s\n" % entry.title)

def on_test_group_start(TestInfo):
    GroupName = TestInfo.related_entry.group
    if GroupName != "": 
        output_man.register(TestInfo.execution_id, "\n -- %s:\n\n" % GroupName)

def on_choice_not_available(TestInfo):
    output_man.register(TestInfo.execution_id, 
                        "        (program '%s' does not provide choice '%s')" % \
                        (TestInfo.related_entry.file_name, TestInfo.choice))

def on_missing_GOOD_file(TestInfo, Filename):
    output_man.register(TestInfo.execution_id, "        (missing 'GOOD/%s')\n" % Filename)

def on_test_is_good_already(TestInfo):
    on_test_end(TestInfo, "[ALREADY GOOD]")

def __get_title(TestInfo):
    Program = TestInfo.program
    Choice  = TestInfo.choice
    if Choice != "":
        # print test program name only on first choice
        if TestInfo.choice_idx != 0: Label = " " * len(Program) + " " + Choice
        else:                        Label = Program + " " + Choice
    else:                            Label = Program

    return "        %s " % Label, len(Label)

def on_test_end(TestInfo, Result):
    L            = 63
    TestProgram  = TestInfo.related_entry.file_name
    Choice       = TestInfo.choice

    txt, TitleL = __get_title(TestInfo)
    if TitleL < 72: txt += "." * (L - TitleL)

    txt += "." * (11 - len(Result)) + "[%s]\n" % Result
    output_man.register_test_end(TestInfo.execution_id, txt)

def on_update_program_entry_info(Filename):
    print "Update: call '%s --hwut-info'" % Filename

def on_database_entry_consistency_check_choice_more_than_once(Entry, ChoiceName):
    print "Inconsistency: Choice '%s' appeared more than once for application '%s'." % \
	  (ChoiceName, Entry.file_name)

def on_database_entry_consistency_check_empty_choice_in_multiple_choices(Entry):
    print "Inconsistency: Empty Choice '' appeared together with other choices in '%s'." % \
	    (Entry.file_name)
    print "Inconsistency: Choices: ", repr(map(lambda x: x.name, Entry.choice_list))

def on_update_program_entry_info_all_terminated():
    print  # newline after possible "// update:" messages

def on_copied_OUT_to_GOOD(Dir, Filename):
    L = 63 
    Space    = ("." * (L - len(Filename)))
    print "     %s " % Filename + Space + "[COPIED TO GOOD]"
    return

def print_missing_good_files(DB):
    """DB = map from directory to list of test sequence elements that do 
            not have GOOD files to compare their output against.
    """
    # -- delete empty entries
    for directory, element_list in DB.items():
	if element_list == []: del DB[directory]

    if DB == {}: return

    print "The following tests have no entry in their 'GOOD/' directory:"
    print
    for directory, element_list in DB.items():

	print "DIR:  " + __get_relative_directory(directory)
	# -- make sure that the list is sorted by application name,
	#    then use the 'choice_idx'
	def __sort(A, B):
	    result = cmp(A.program, B.program)
	    if result != 0: return result
	    else:           return cmp(A.choice_idx, B.choice_idx)

	element_list.sort(__sort)
	print
	for element in element_list:
	    if element.choice_idx == 0:
		print "    " + element.program + " " + element.choice
	    else:
		print "    " + " " * len(element.application) + element.choice
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
    print "error: does not exist." 

def on_error_make_failed(Bunch):
    for program in Bunch:
        print "error: make failed on '%s'" % program

def on_make_bunch_of_test_programs(Bunch):
    for program in Bunch:
        print "make: %s" % program

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

def on_make_clean():
    print "make: clean"

def on_warning_source_file_has_executable_rights(Filename):
    """Some files are usually considered source files that are to be compiled.
       If they have executable rights, it might get confusing.
    """
    print "warning: file '%s' has executable rights (normally considered to be a source file)." % Filename

def on_database_not_found(Dir):
    print "warning: no database file for hwut-information found for directory:"
    print "warning: %s" % Dir

def on_database_entry_not_available(ApplicationName):
    print "warning: '%s' in database but no longer available---dismissed." % ApplicationName 

def on_database_entry_not_yet_in_database(ApplicationName):
    print "note: '%s' not yet in database---added." % ApplicationName 

def on_database_contained_entry_multiple_times(ApplicationName):
    print "Warning: '%s' appeared multiple times in database---dismissed." % ApplicationName 

def on_xml_database_parsing_error():
    print "Warning: Parsing error in xml-database of directory '%s'" % __get_relative_directory(os.getcwd())
    print "Warning: Database of this directory is cleared."

def on_xml_database_entry_consistency_check_failed(Entry):
    print "Warning: Entry '%s' in xml-database of directory '%s'" % Entry.file_name
    print "Warning: is inconsistent. Entry is cleared and reset."

def on_file_not_executable_and_not_makeable(file, makeable_file_list):
    print "error: specified file '%s' is not executable and not 'make'-able." % file
    print "error: 'make'-able files are:"
    if makeable_file_list == []:
	print "error: <none>"
    else:
	for file in makeable_file_list:
	    print "error:    " + file
    sys.exit(-1)

def on_temporary_file_cannot_be_deleted(Filename):
    print "         warning: cannot delete temporary file '%s'" % Filename

def on_temporary_file_cannot_be_opened(Filename):
    print "         error: cannot open temporary file '%s'" % Filename
    sys.exit(-1)

def on_error_log_file_cannot_be_opened(Filename):
    print "         error: cannot error log file '%s'" % Filename
    sys.exit(-1)

def on_program_is_not_executable(ApplicationName, OptionList):
    sys.stdout.write("\nerror: Program '%s' is not executable (or does not exists)\n" % ApplicationName + \
                     "error:\n" + \
                     "error: current directory:    " + os.getcwd() + "\n" + \
                     "error: command line options: " + repr(OptionList) + "\n" + \
                     "error:\n" + \
                     "error: -- Is this a script and you forgot to specify your interpreter?\n" + \
                     "error:    If so, type '#! /usr/bin/env my_interpreter' in the first line of your file.\n" + \
                     "error: -- Or, set the PATH variable so that it contains the path to your application!\n")
    sys.exit(-1)

def xml_missing_attribute(Section, Attribute):
    print "xml-error: missing attribute '%s' in section '%s'" % (Attribute, Section)

def on_delete_file_out_of_date(Filename):
    print "Deleted: '%s'. Reason: out of date."

def on_information_required_from_unmade_file(Filename):
    print "Warning: no information from '%s' accessible. File was not built." % Filename

def on_file_deleted(Filename):
    print "Deleted: '%s'" % Filename


def on_unknown_diff_program(Program):
    print "Warning: diff program '%s' unknown to hwut."
