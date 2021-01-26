# (C) 2007 Frank-Rene Schaefer
import os
import sys
import hwut.common as common
import hwut.io     as io
import hwut.aux    as aux
import hwut.make   as make
import hwut.test_executer as test_executer


def do(Dir, CreateOnlyOutputF=False, FailedOnlyF=False):

    entry_list, missing_test_program_files = __init(Dir, FailedOnlyF)

    # LOOP: all groups
    result_f = True
    group_dict = __arrange_in_groups(entry_list)
    for group_name, test_entry_list in group_dict.items():    
        io.on_test_group_start(group_name)

        grouped_f = (group_name != "")
	if __test_group(test_entry_list, CreateOnlyOutputF, grouped_f, missing_test_program_files) == False:
	    result_f = False

    __terminate(result_f, Dir)

    return result_f

def do_single(Dir, ProgramName, Choice, CreateOnlyOutputF=False):

    entry_list, MissingTestProgramFiles = __init(Dir, FailedOnlyF=False, 
	                                         SpecificProgramList=[ ProgramName ])

    result_f = __test_single(entry_list[0], ProgramName, Choice, MissingTestProgramFiles, CreateOnlyOutputF)

    __terminate(result_f, Dir)


def go(Dir):
    os.chdir(common.home_directory)  # need first to go home, since 'dir'
    os.chdir(Dir)                    # is relative to 'home directory', i.e.
    #                                # the directory where hwut was called.

def init_home():
    """Set the home directory. All directories passed to the functions of 
       this modules are relative to the home directory.
    """
    common.home_directory = os.getcwd()

def __test_single(db_entry, ProgramName, Choice, MissingTestProgramFiles, CreateOnlyOutputF):

    if ProgramName in MissingTestProgramFiles:
	if db_entry.choices == []: L = 1
	else:                   L = len(db_entry.choices)
	result_list = [ "MAKE FAILED" ] * L
	io.on_test_end("MAKE FAILED", ProgramName)
	return False

    elif db_entry.choices == []:
	result_f = test_executer.do(ProgramName, "", CreateOnlyOutputF) 
        db_entry.results = [ __convert_to_string_result(result_f) ]
	io.on_test_end(result_f, ProgramName)

	return result_f

    elif Choice != "":
	result  = test_executer.do(ProgramName, Choice, CreateOnlyOutputF)
	try: 
	    choice_idx = db_entry.choices.index()
	except:
	    io.on_choice_not_available(Choice, ProgramName)
	    return False

	result_f = test_executer.do(ProgramName, Choice, CreateOnlyOutputF)
	db_entry.choices[choice_idx] = __convert_to_string_result(result_f)
	return result_f

    else:
	first_f     = True
	result_list = []
	# LOOP: all choices for test program
	for choice in db_entry.choices:
	    result  = test_executer.do(ProgramName, choice, CreateOnlyOutputF)
	    result_list.append(result)
	    io.on_test_end(result, ProgramName, choice, first_f)
	    first_f = False

        db_entry.results = map(__convert_to_string_result, result_list) 

	return not (False in result_list)

def __test_group(test_entry_list, CreateOnlyOutputF, GroupedF, MissingTestProgramFiles):
    """Performs all tests given as 'test_entry_list'. The results of the 
       tests are written into the .results member of the correspondent 
       entry.
    """
    # LOOP: all test programs in group
    result_f = True
    for entry in test_entry_list:
	ProgramName = entry.file_name
	io.on_test_start(GroupedF, entry)
	
        # -- if one test failed, then the test failed. otherwise ok.
	if __test_single(entry, ProgramName, "", MissingTestProgramFiles, CreateOnlyOutputF) == False:
	    result_f = False

    return result_f

def __convert_to_string_result(result):
    """Enter the results in the db-entry."""
    if   result == True:  return "OK"
    elif result == False: return "FAIL"
    else:                 return "<no result>"

def __init(Dir, FailedOnlyF=False, SpecificProgramList=[]):

    go(Dir)
    aux.ensure_directory_structure()
    #
    io.on_directory_enter(Dir, common.HWUT_TITLE_FILE)

    # -- read content of cache file for current directory into the info_db
    common.info_db.read(common.HWUT_CACHE_FILE)

    if FailedOnlyF: file_name_list = __get_failed_program_list()
    else:           file_name_list = __get_program_list(SpecificProgramList)

    # -- make sure that filenames are unique
    file_name_list = __ensure_unique_filenames(file_name_list)

    # -- make test programs, if there is something to be made
    unmade_file_list = []
    if make.is_makefile_present(): 
	unmade_file_list = make.this(file_name_list)

    return common.info_db.extract_entries(file_name_list), unmade_file_list
    
def __terminate(ResultF, Dir):
    #
    io.on_directory_terminated(ResultF, Dir, common.failed_test_list)

    # -- for safety: lock all files for good in directory GOOD/
    aux.raise_write_protection("./GOOD")

    # -- check, if there is a makefile, if so do 'make clean'
    if make.is_makefile_present(): make.clean()

    # -- store changed information to the cache file
    common.info_db.write()

def __get_program_list(FileNameList=[]):
    """Get all executable files in current directory. If a makefile is 
       present, it requests the files to be created via 'make hwut-info'.
    """
    executable_file_list = aux.find("./", "-perm +ua+x")
    makeable_file_list   = make.get_program_list()

    if FileNameList == []: 
	return __ensure_unique_filenames(executable_file_list + makeable_file_list)

    for file in FileNameList:
	file = aux.ensure_dot_slash(file)
	if file not in executable_file_list and file not in makeable_file_list:
	    print "error: specified file '%s' is not executable and not 'make'-able." % file
	    sys.exit(-1)

    return __ensure_unique_filenames(FileNameList)

def __get_failed_program_list():
    """Get list of programs that failed at the last run. 
       Requires the common.info_db object to be adapted to the directory
       under concern.
    """
    if common.info_db.directory != os.getcwd():
	raise "error: info_db was not updated for current directory"

    entry_list = []
    for name, entry in common.info_db.db.items():
	if "FAIL" in entry.results: entry_list.append(name)
	
    test_file_list = []
    if entry_list != []: test_file_list = __get_program_list(entry_list)

    return test_file_list

def __arrange_in_groups(TestEntryList):

    group_map = {}
    for entry in TestEntryList:
	if group_map.has_key(entry.group): group_map[entry.group].append(entry)	    
	else:                              group_map[entry.group] = [ entry ]

    return group_map

def __ensure_unique_filenames(filename_list):
    unique = {}
    for name in filename_list: 
	unique[aux.strip_dot_slash(name)] = True
    return unique.keys()

