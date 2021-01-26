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


def get_executable_application_list(AcceptedExtensionList=[]):
    ExtensionListOfFilesToBeCompiled = [".c", ".cpp", ".c++", ".p", ".h", 
                                        ".bak", 
                                        "~", 
                                        "makefile", "Makefile", 
                                        "stackdump"]

    CriticalExtensionList = filter(lambda x: x not in AcceptedExtensionList, 
                                   ExtensionListOfFilesToBeCompiled)

    # -- executable fils in current directory
    executable_file_list = map(aux.strip_dot_slash, aux.find_executables())


    result                  = []
    unusual_executable_list = []
    for file_name in executable_file_list:

        LF = len(file_name)
        if LF == 0: continue

        for extension in CriticalExtensionList:
            LE = len(extension)
            found_idx = file_name.rfind(extension)
            if found_idx != -1 and found_idx == LF - LE: 
                unusual_executable_list.append(file_name)
                break
        else:
            result.append(file_name)

    if unusual_executable_list != []:
        io.on_found_unusual_executables(unusual_executable_list)

    return result 
