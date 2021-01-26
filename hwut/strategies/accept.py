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

from hwut.frs_py.string_handling import trim
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

        self.execution_f     = Setup.execution_f
        self.interact_f      = Setup.grant != "ALL"

        CoreStrategy.__init__(self, Setup.failed_only_f)
        
    def do(self, TestInfoObj):
        ProgramName = TestInfoObj.program
        Choice      = TestInfoObj.choice

        # -- if requested execute test programs with choice
        if self.execution_f: 
            TestExecutionStrategy().do(TestInfoObj, CreateOnlyOutputF=True) 

        # -- copy protocol files of all specified choices
        interaction_info = aux.copy_to_GOOD(TestInfoObj, self.interact_f)    
        if   interaction_info == "ALL":  self.interact_f = False
        elif interaction_info == "NONE": self.__break_up_f = True

        if interaction_info in ["YES", "ALL"]: return "COPIED TO GOOD"
        else:                                  return "UNTOUCHED"

    def end_directory(self):
        return "DONE"



