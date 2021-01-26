import sys
import os
import time

from   hwut.strategies.core  import CoreStrategy

import hwut.auxiliary as aux
import hwut.common    as common
import hwut.io        as io
import hwut.make      as make


class TestExecutionStrategy(CoreStrategy):

    def __init__(self, Setup, CreateOnlyOutputF=False):
        self.create_only_output_f = CreateOnlyOutputF
        self.directory            = "/dev/null/"
        self.missing_good_files   = {}  # map: directory --> list of test applications
        #                               #      that do not have files in the GOOD/ directory. 

        self.failed_test_list        = [] # initialize here, because some other strategies might
        #                                 # use a shortcut with calling start_directory()
        CoreStrategy.__init__(self, Setup.failed_only_f)

    def start_directory(self, Dir):
        self.directory               = Dir
        self.failed_test_list        = []
        self.missing_good_files[Dir] = []

    def do(self, element):
        assert self.directory != "/dev/null"

        TestProgram = element.related_entry.file_name
        Choice      = element.choice
        ChoiceIdx   = element.choice_idx

        if not element.present_f: 
            self.failed_test_list.append(element)
            return "MAKE FAILED"

        # (*) run the test program
        time_start = time.time()
        test_output = aux.execute_this(aux.ensure_dot_slash(TestProgram), 
                                       [Choice], 
                                       "./OUT/" + aux.get_protocol_filename(TestProgram, Choice))
        time_end = time.time()
        element.related_entry.choice_list[ChoiceIdx].time_to_execute_sec = time_end - time_start

        description_str = TestProgram
        if Choice != "": 
            description_str += " " + Choice

        if not self.create_only_output_f: 
            result = aux.compare_result(element, test_output)  # compare with expectation
            if result == "NO GOOD FILE":
                self.missing_good_files[self.directory].append(element)
        else:
            result = "DONE"                                    # no comparison necessary
            
        if result not in ["OK", "NO GOOD FILE", "DONE"]: 
            self.failed_test_list.append(element)

        element.related_entry.choice_list[ChoiceIdx].result = result
        return result

    def end_directory(self):
        if self.failed_test_list != []: io.print_failure(self.directory, self.failed_test_list)
        else:                           io.print_ok(self.directory)

        # -- for safety: lock all files for good in directory GOOD/
        aux.raise_write_protection("./GOOD")

        io.on_directory_terminated(self.directory)
        self.directory = "/dev/null/"

        if self.failed_test_list == []: return "OK"
        else:                           return "FAIL"

    def end_directory_tree(self):
        io.print_missing_good_files(self.missing_good_files)
