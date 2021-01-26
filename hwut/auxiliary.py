import tempfile
import sys
import os
import stat
import subprocess
import hwut.io     as io
import hwut.common as common


def execute_this(ApplicationName, OptionList=[], OutputFilename="", ErrorOutputFilename="/dev/null"):
    # NOTE: We cannot simply insert "./" by default at the beginning of the 
    #       application name, since also other applications may be called that
    #       are not located in the current directory.
    output_filename_generated_on_the_fly_f = False
    if OutputFilename == "": 
        output_filename_generated_on_the_fly_f = True
        #
        fd, OutputFilename = tempfile.mkstemp(".hwut", "TMP")
        fh = os.fdopen(fd, "w")
    else:
        try:    fh = open(OutputFilename, "w")
        except: io.on_temporary_file_cannot_be_opened(OutputFilename)

    try:    fh_err = open(ErrorOutputFilename, "w")
    except: io.on_error_log_file_cannot_be_opened(ErrorOutputFilename)

    try:    subprocess.call([ApplicationName] + OptionList, stdout = fh, stderr=fh_err)
    except: io.on_program_is_not_executable(ApplicationName, OptionList)

    fh.close()
    fh_err.close()

    fh = open(OutputFilename)
    result = fh.read()  
    fh.close()

    if output_filename_generated_on_the_fly_f: 
        try:    os.remove(OutputFilename)
        except: io.on_temporary_file_cannot_be_deleted(OutputFilename)
    
    # return string containing standard output from the test program
    return result

def get_protocol_filename(Program, Choice):
    arg_str = ""
    if Choice != "": arg_str = "--%s" % Choice

    Program = strip_dot_slash(Program)
    
    return Program + arg_str + ".txt"

def find(Dir, OptionStr):
    if OptionStr.find("-type") == -1:     OptionStr = "-type f " + OptionStr
    if OptionStr.find("-mindepth") == -1: OptionStr = "-maxdepth 1 " + OptionStr
    
    file_list_str = execute_this("find", [Dir] + OptionStr.split())
    
    # return list of files
    if file_list_str != "": return file_list_str.split()
    else:                   return []

def raise_write_protection(Dir):
    """Find files in Dir that are not write protected and make them write protected"""
    unprotected_files = find(Dir, "-perm +u+w")    
    for file in unprotected_files:
        io.on_raise_write_protection(Dir, file)
        os.chmod(file, stat.S_IREAD)

def get_hwut_unrelated_files(Dir):
    common.application_db.init()

    test_sequence_element_list = common.application_db.get_test_execution_sequence()

    protocol_file_name_list = map(lambda element: get_protocol_filename(element.program, element.choice),
                                  test_sequence_element_list)

    expected_in_TEST = map(lambda element: element.programm, test_sequence_element_list)

    expected_in_GOOD = map(lambda file_name: "GOOD/" + file_name, protocol_file_name_list)
    expected_in_OUT  = map(lambda file_name: "OUT/" + file_name, protocol_file_name_list)
    expected_in_ADM  = [ "database.xml", "title.txt" ]


    files_in_TEST = map(strip_dot_slash, find("./", "-maxdepth 1  -type f" % TEST_directory_name))
    files_in_GOOD = map(strip_dot_slash, find("./GOOD", ""))
    files_in_OUT  = map(strip_dot_slash, find("./OUT", ""))
    files_in_ADM  = map(strip_dot_slash, find("./ADM", ""))


    result = \
             filter(lambda file_name: file_name not in expected_in_TEST, files_in_TEST) + \
             filter(lambda file_name: file_name not in expected_in_GOOD, files_in_GOOD) + \
             filter(lambda file_name: file_name not in expected_in_OUT, files_in_OUT)   + \
             filter(lambda file_name: file_name not in expected_in_ADM, files_in_ADM)



    return result

def ensure_directory_structure():
    """Makes sure that ./OUT, ./GOOD, and ./ADM exist in the current directory."""
    for directory in ["OUT", "GOOD", "ADM"]:
        if not os.access(directory, os.F_OK): 
            os.mkdir(directory)

def get_TEST_directories():
    TEST_directory_name   = "TEST"
    L_TEST_directory_name = len(TEST_directory_name)

    # -- find all sub-dirs that are ./TEST-directories
    test_dir_list = find("./", "-mindepth 1  -name %s -type d" % TEST_directory_name)

    def __check_end(Name):
        return Name.rfind(TEST_directory_name) == len(Name) - L_TEST_directory_name

    # -- take only those directories that end with "/TEST"
    test_dir_list = filter(__check_end, test_dir_list)
 
    # -- add the current directory, if it is called 'TEST'
    current_directory = os.getcwd()
    if len(current_directory) > 1 and current_directory[-1] in ["/", "\\"]:
        current_directory = current_directory[:-1]
    if __check_end(current_directory): 
        test_dir_list.append("./")

    test_dir_list.sort()

    return test_dir_list

def strip_dot_slash(Filename):
    if len(Filename) > 2 and Filename[:2] == "./": return Filename[2:]
    else:                                          return Filename

def ensure_dot_slash(Filename):
    if len(Filename) > 2 and Filename[:2] != "./": return "./" + Filename
    else:                                          return Filename

def copy_to_GOOD(TestSequenceElement, InteractF=True):      
    """RETURN: 
           ALL  -- user wants all files to be copied.
           NONE -- user wants no single file to be copied

       assume Dir = current directory
    """
    ApplicationName = TestSequenceElement.program
    Choice          = TestSequenceElement.choice
    ProtocolFileName = get_protocol_filename(ApplicationName, Choice)

    reply = "YES"
    if InteractF: 
        reply = io.request_copy_OUT_to_GOOD(ProtocolFileName)

    if reply in ["YES", "ALL"]:

        if os.access("GOOD/%s" % ProtocolFileName, os.F_OK):
            os.chmod("GOOD/%s" % ProtocolFileName, stat.S_IWRITE)

        if not os.access("OUT/%s" % ProtocolFileName, os.F_OK):
            io.on_file_does_not_exist("OUT/%s" % ProtocolFileName)
            return "NO"

        # -- copy file from OUT/ to GOOD/
        fh = open("OUT/%s" % ProtocolFileName, "rb")
        content = fh.read()
        fh.close()
        fh = open("GOOD/%s" % ProtocolFileName, "w")
        fh.write(content)
        fh.close()

        if not os.access("GOOD/%s" % ProtocolFileName, os.F_OK):
            io.on_file_access_error("GOOD/%s" % ProtocolFileName)
            return "NO"

        os.chmod("GOOD/%s" % ProtocolFileName, stat.S_IREAD)

    return reply

def __get_GOOD_output(TestInfo):
    TestProgram = TestInfo.program
    Choice      = TestInfo.choice

    TestProgramProt = get_protocol_filename(TestProgram, Choice) 
    try:
        return open("GOOD/" + TestProgramProt).read()    
    except: 
        io.on_missing_GOOD_file(TestInfo, TestProgramProt)
        return ""

def compare_result(TestInfo, TestOutput=None):
    assert type(TestOutput) == str or TestOutput == None

    if TestOutput == None:
        out_file  = "OUT/%s"  % get_protocol_filename(TestInfo.program, TestInfo.choice)
        try: 
            TestOutput = open(out_file).read()
        except:
            return "NO OUT FILE"

    # (*) compare with expectation
    GoodOutput = __get_GOOD_output(TestInfo)
    if GoodOutput == "": return "NO GOOD FILE"

    # -- avoid confusion with 'carriage return/line feed' on different
    #    operating systems
    result_str   = TestOutput.replace("\r\n", "\n")
    expected_str = GoodOutput.replace("\r\n", "\n")

    if result_str == expected_str: return "OK"
    else:                          return "FAIL"
