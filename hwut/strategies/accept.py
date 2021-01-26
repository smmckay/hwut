#! /usr/bin/env python
#
# PURPOSE: Runs all test scripts and reports results.
#
# (C) 2006, 2007 Frank-Rene Schaefer
#
# ABSOLUTELY NO WARRANTY
################################################################################
import os
import stat
import sys

from hwut.directory              import test_info

import hwut.common    as common
import hwut.directory as directory
import hwut.io        as io
import hwut.auxiliary as aux
#
from hwut.strategies.core import CoreStrategy
from hwut.strategies.test import TestExecutionStrategy


class AcceptStrategy(CoreStrategy):
    def __init__(self, Setup):
        assert Setup.grant in ["ALL", "NONE", "INTERACTIVE"]

        self.execution_f      = Setup.execution_f
        self.interaction_info = Setup.grant

        self.directory         = "/dev/null/"
        self.missing_out_files = {}

        self.setup            = Setup
        CoreStrategy.__init__(self, Setup)

    def start_directory(self, Dir):
        self.directory              = Dir
        self.missing_out_files[Dir] = []
        
    def do(self, TestInfoObj):
        assert TestInfoObj.__class__.__name__ == "test_info"
        assert self.interaction_info in ["ALL", "NONE", "INTERACTIVE"]

        if self.interaction_info == "NONE": 
            return "UNTOUCHED"

        # -- if requested execute test programs with choice
        if self.execution_f: 
            TestExecutionStrategy(self.setup).do(TestInfoObj) 
        elif not aux.is_there_an_OUT_file(TestInfoObj):
            io.on_OUT_file_missing_cannot_accept(TestInfoObj)
            self.missing_out_files[self.directory].append(TestInfoObj)
            return "NO GOOD FILE"

        # -- is there a difference in the first place between OUT and GOOD?
        result = aux.compare_result(TestInfoObj)
        if result not in ["NO GOOD FILE", "FAIL"]: return result

        return self._do(TestInfoObj)

    def _do(self, TestInfoObj):
        """This function is used by a derived class, too."""

        # -- copy protocol files of all specified choices
        if self.interaction_info == "INTERACTIVE":
            user_reply = aux.copy_to_GOOD(TestInfoObj, InteractF=True)    
        elif self.interaction_info == "ALL":
            user_reply = aux.copy_to_GOOD(TestInfoObj, InteractF=False)    
        else:
            user_reply = "" # nothing to be done

        if user_reply in ["ALL", "NONE"]:  
            self.interaction_info = user_reply

        if user_reply in ["YES", "ALL"]: return "COPIED TO GOOD"
        else:                            return "UNTOUCHED"

    def end_directory(self):
        return "DONE"

    def end_directory_tree(self):
        io.print_missing_out_files(self.missing_out_files)


