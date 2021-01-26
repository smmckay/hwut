import os
import stat
import subprocess

def execute_this(ApplicationName, OptionList=[], OutputFilename="", ErrorOutputFilename="/dev/null"):
    # NOTE: We cannot simply insert "./" by default at the beginning of the 
    #       application name, since also other applications may be called that
    #       are not located in the current directory.
    if OutputFilename == "": OutputFilename = "HWUT.tmp"

    fh = open(OutputFilename, "w")
    fh_err = open(ErrorOutputFilename, "w")
    subprocess.call([ApplicationName] + OptionList, stdout = fh, stderr=fh_err)
    fh.close()
    fh_err.close()

    fh = open(OutputFilename)
    result = fh.read()  
    fh.close()

    if OutputFilename == "HWUT.tmp": os.remove(OutputFilename)
    
    # return list of files
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

def get_hwut_unrelated_files_in_GOOD_and_OUT(Dir):
    """Currently not working."""
    directory.go(Dir)
    program_list = directory.__get_program_list()

def ensure_directory_structure():
    """Makes sure that ./OUT and ./GOOD exist in the current directory."""
    if not os.access("GOOD", os.F_OK): os.mkdir("GOOD")
    if not os.access("OUT", os.F_OK):  os.mkdir("OUT")

def get_TEST_directories():

    # -- find all sub-dirs that are ./TEST-directories
    test_dir_list = find("./", "-mindepth 1  -name TEST -type d")

    # -- take only those directories that end with "/TEST"
    test_dir_list = filter(lambda x: 
	                   len(x) >= len("/TEST") and x[-len("/TEST"):] == "/TEST",
			   test_dir_list)
 
    # -- add the current directory, if it is called 'TEST'
    if os.access("../TEST", os.F_OK): test_dir_list.append("./")
    test_dir_list.sort()

    return test_dir_list

def strip_dot_slash(Filename):
    if len(Filename) > 2 and Filename[:2] == "./": return Filename[2:]
    else:                                          return Filename

def ensure_dot_slash(Filename):
    if len(Filename) > 2 and Filename[:2] != "./": return "./" + Filename
    else:                                          return Filename

