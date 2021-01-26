import os
import hwut.directory as directory
import hwut.common    as common
import hwut.auxiliary as aux
import hwut.io        as io
#
from   hwut.directory       import test_info
from   hwut.strategies.accept import AcceptStrategy
from   hwut.strategies.test   import TestExecutionStrategy

class DifferenceDisplayStrategy(AcceptStrategy):

    def __init__(self, Setup):
        assert Setup.grant in ["ALL", "NONE", "INTERACTIVE"]

        self.display_program  = Setup.diff_program_name 
        self.execution_f      = Setup.execution_f
        self.setup            = Setup

        AcceptStrategy.__init__(self, Setup)

    def do(self, TestInfoObj):
        assert TestInfoObj.__class__.__name__ == "test_info"
        assert self.interaction_info in ["ALL", "NONE", "INTERACTIVE"]

        ProgramName = TestInfoObj.program
        Choice      = TestInfoObj.choice

        # -- If requested, then execute test program.
        if self.execution_f:
            TestExecutionStrategy(self.setup).do(TestInfoObj) 

        # -- display only, if:  (1) OUT and GOOD files exist
        #                       (2) content of files differs
        result = aux.compare_result(TestInfoObj)

        if result == "OK":   return "NO DIFFERENCE"
        if result != "FAIL": return result

        out_file  = "OUT/%s"  % TestInfoObj.protocol_file_name
        good_file = "GOOD/%s" % TestInfoObj.protocol_file_name

        # -- Show the differences (maybe user changes some stuff)
        try:    os.system("%s %s %s" % (self.display_program, out_file, good_file))
        except: io.on_program_is_not_executable(self.display_program, "")

        # -- copy protocol files of all specified choices
        return AcceptStrategy._do(self, TestInfoObj)



