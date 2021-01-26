# (C) 2007 Frank-Rene Schaefer
import hwut.common        as common
import hwut.io            as io
import hwut.auxiliary     as aux
import hwut.make          as make
#
import threading
import os
import sys
from hwut.strategies.core import test_info


TestThread_currently_running_n = -1

class TestThread(threading.Thread):
    def __init__(self, TestInfo, CreateOnlyOutputF):
        assert TestInfo.choice == "" or TestInfo.related_entry.choice_list != []

        self.test_info            = TestInfo
        self.create_only_output_f = CreateOnlyOutputF
        self.result_f             = False

        return threading.Thread.__init__(self)

    def run(self):
        is_group_element_f = self.test_info.group != ""
        io.on_test_start(self.test_info, is_group_element_f)

        if self.test_info.present_f: 
            self.result_f = test_executer.do(self.test_info, self.create_only_output_f) 
            result = convert_to_string_result(self.result_f) 
        else:
            result = "MAKE FAILED"

        self.test_info.related_entry.results[self.test_info.choice_idx] = result

        io.on_test_end(self.test_info, result)


def init_home():
    """Set the home directory. All directories passed to the functions of 
       this modules are relative to the home directory.
    """

def get_executable_application_list():
    # -- executable fils in current directory
    executable_file_list = map(aux.strip_dot_slash, aux.find("./", "-perm +ua+x -maxdepth 1"))

    return executable_file_list 
