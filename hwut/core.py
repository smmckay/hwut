import hwut.io        as io
import hwut.common    as common
import hwut.auxiliary as aux
import hwut.directory as directory
#
import os
import sys

def run(setup, strategy):
    if setup.program_name != "": do(setup.program_name, setup.choice, strategy)
    else:                        do_directory_tree(strategy)
    sys.exit(0)

def do(ProgramName, ChoiceSpecification, Strategy):
    """
    """
    assert type(ProgramName) == str and ProgramName != ""
    assert type(ChoiceSpecification) == str
    __assert_strategy(Strategy)

    ProgramName = aux.strip_dot_slash(ProgramName)

    # -- read content of cache file for current directory into the application_db
    test_list = common.application_db.get_test_execution_sequence([ProgramName], 
                                                                  SpecificChoice=ChoiceSpecification)
    if test_list == []:
        io.on_file_does_not_exist(ProgramName)

    do_list(test_list, Strategy)

def do_list(TestExecutionSequence, Strategy): 
    """This is the mother of all HWUT related functionality. All tests
       pass by this function. It executes a list of files (or all) in
       the current directory. 
    """
    assert type(TestExecutionSequence) == list
    assert map(lambda element: element.__class__.__name__, TestExecutionSequence) \
           == [ "test_info" ] * len(TestExecutionSequence)
    __assert_strategy(Strategy)

    Directory = os.getcwd()

    aux.ensure_directory_structure()

    io.on_directory_enter(Directory, Strategy.get_referred_date())

    # NOTE: If TestExecutionSequence != [], then the common.application_db must have
    #       been initialized, otherwise no test sequence could have been extracted.
    if TestExecutionSequence == []:
        TestExecutionSequence = common.application_db.get_test_execution_sequence()

    io.on_test_sequence_start()

    Strategy.start_directory(Directory)

    current_group = None
    for element in TestExecutionSequence:    
        if Strategy.break_up_requested(): break

        if current_group != element.group: 
            current_group = element.group
            io.on_test_group_start(element)

        io.on_test_start(element)
        if element.last_result == "OK" and Strategy.handle_only_failed_experiments():
            io.on_test_is_good_already(element)
            continue
        else:
            result = Strategy.do(element) 
            io.on_test_end(element, result)

    if Strategy.xml_database_write_permission(): 
        common.application_db.write()

    return Strategy.end_directory()

def do_directory_tree(Strategy):
    __assert_strategy(Strategy)

    # -- store the directore from where HWUT was called.
    home_directory = os.getcwd()
    io.__home_directory = home_directory

    # -- get list of subdirectories that contain test applications, sort them.
    def __sort(DirA, DirB):
        directory_path_list_A = DirA.split("/")
        directory_path_list_B = DirB.split("/")

        LA = len(directory_path_list_A)
        LB = len(directory_path_list_B)
        for i in range(min(LA, LB)):
            cmp_result = cmp(directory_path_list_A[i], directory_path_list_B[i])
            if cmp_result != 0: return cmp_result
        else:
            return cmp(LA, LB)

    hwut_related_directory_list = aux.get_TEST_directories()
    hwut_related_directory_list.sort(__sort)

    # -- iterate over the list of directories that contain test applications
    Strategy.start_directory_tree(hwut_related_directory_list)

    result_list = []
    for dir in hwut_related_directory_list:
        # -- enter the concerned directory
        os.chdir(home_directory)  # need first to go home, since 'dir'
        os.chdir(dir)             # is relative to 'home directory', i.e.

        # -- run all tests of directory
        result = do_list([], Strategy)

        # -- if there is a result, append it to the list
        if result != None: result_list.append([dir, result])

    # -- print result
    io.print_summary(result_list)

    Strategy.end_directory_tree()


def __assert_strategy(Strategy):
    assert "do"                             in dir(Strategy)
    assert "break_up_requested"             in dir(Strategy)
    assert "handle_only_failed_experiments" in dir(Strategy)
    assert "end_directory"                  in dir(Strategy)
    assert "start_directory"                in dir(Strategy)
    assert "end_directory_tree"             in dir(Strategy)
    assert "start_directory_tree"           in dir(Strategy)
