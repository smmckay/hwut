import os
import hwut.directory as directory
import hwut.common    as common
import hwut.auxiliary as aux
import hwut.io        as io
#
from   hwut.directory       import test_info
from   hwut.strategies.core import CoreStrategy
from   hwut.strategies.test import TestExecutionStrategy

class DifferenceDisplayStrategy(CoreStrategy):

    def __init__(self, Setup):
        assert Setup.grant in ["ALL", "NONE", "INTERACTIVE"]

        self.display_program = Setup.diff_program_name 
        self.execution_f     = Setup.execution_f
        self.interact_f      = Setup.grant != "ALL"
        self.setup           = Setup

        CoreStrategy.__init__(self, Setup.failed_only_f)

    def do(self, TestInfoObj):
        assert TestInfoObj.__class__.__name__ == "test_info"

        ProgramName = TestInfoObj.program
        Choice      = TestInfoObj.choice

        # -- If requested, then execute test program.
        if self.execution_f:
            TestExecutionStrategy(self.setup).do(TestInfoObj) 


        # -- display only, if:  (1) OUT and GOOD files exist
        #                       (2) content of files differs
        result = aux.compare_result(TestInfoObj)

        if result == "FAIL":
            protocol_file_name = aux.get_protocol_filename(ProgramName, Choice)
            out_file  = "OUT/%s"  % protocol_file_name
            good_file = "GOOD/%s" % protocol_file_name

            # -- Show the differences (maybe user changes some stuff)
            try:    os.system("%s %s %s" % (self.display_program, out_file, good_file))
            except: io.on_program_is_not_executable(self.display_program, "")

            # -- Copy protocol files of all specified choices? Only if files are 
            #    finally different.
            interaction_info = aux.copy_to_GOOD(TestInfoObj, self.interact_f)    
            if   interaction_info == "ALL":  self.interact_f = False
            elif interaction_info == "NONE": self.__break_up_f = True

            if interaction_info in ["YES", "ALL"]: result = "COPIED TO GOOD"
            else:                                  result = "UNTOUCHED"

        elif result == "OK":
            result = "NO DIFFERENCE"
        
        return result



