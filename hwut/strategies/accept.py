# SPDX license identifier: LGPL-2.1
#
# Copyright (C) Frank-Rene Schaefer, private.
# Copyright (C) Frank-Rene Schaefer, 
#               Visteon Innovation&Technology GmbH, 
#               Kerpen, Germany.
#
# This file is part of "HWUT -- The hello worldler's unit test".
#
#                  http://hwut.sourceforge.net
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA
#
#------------------------------------------------------------------------------
#! /usr/bin/env python
#
# PURPOSE: Runs all test scripts and reports results.
#
# (C) Frank-Rene Schaefer
#
# ABSOLUTELY NO WARRANTY
################################################################################
import os
import stat
import sys

import hwut.common                as common
import hwut.io.messages           as io
import hwut.io.select             as select
import hwut.verdict.comparison    as comparison
import hwut.auxiliary.path        as aux
import hwut.auxiliary.file_system as fs
#
from hwut.strategies.core import CoreStrategy
from hwut.strategies.test import TestExecutionStrategy


class AcceptStrategy(CoreStrategy):
    def __init__(self, Setup):
        assert Setup.grant in ["ALL", "NONE", "INTERACTIVE"]

        self.interaction_info = Setup.grant

        self.missing_out_files = {}

        CoreStrategy.__init__(self, Setup)

    def _start_directory(self, TestSequence):
        self.missing_out_files[self._current_dir] = []
        
    def do(self, TestInfo):
        assert self.interaction_info in ["ALL", "NONE", "INTERACTIVE"]

        if self.interaction_info == "NONE": 
            io.on_test_end(TestInfo, "UNTOUCHED")
            return "UNTOUCHED"

        elif TestInfo.description.temporal_logic_f():
            io.on_test_end(TestInfo, "LOGIC DEP")
            return "LOGIC DEP"

        # -- if requested execute test programs with choice
        if self.setup.execution_f:
            TestInfo.execute()

        elif not aux.is_there_an_OUT_file(TestInfo):
            io.on_file_missing_OUT_file_during_accept(TestInfo, True) 
            TestInfo.execute()

        # -- is there a difference in the first place between OUT and GOOD?
        fh_out  = TestInfo.OUT_FileHandle()
        fh_good = TestInfo.GOOD_FileHandle(ForgiveF=True)
        if     fh_out  is not None \
           and fh_good is not None \
           and comparison.do(fh_out, fh_good, TestInfo):
           total_verdict, \
           extra_files_verdict_db = comparison.do_extra_output_file_list(TestInfo, "DONE") 
           if total_verdict == "OK":
                # Test was Ok, nothing to be done. 
                io.on_test_end(TestInfo, "OK", extra_files_verdict_db)
                return

        verdict, extra_file_verdict_db = self._do(TestInfo)
        io.on_test_end(TestInfo, verdict, extra_file_verdict_db)

    def _do(self, TestInfo, ManualChangePreceededF=False):
        """This function is used by a derived class, too."""

        extra_files_verdict_db = None
        # -- copy protocol files of all specified choices
        if self.interaction_info == "INTERACTIVE":
            user_reply,            \
            extra_files_verdict_db = copy_OUT_to_GOOD(TestInfo, InteractF=True)    
        elif self.interaction_info == "ALL":
            user_reply,            \
            extra_files_verdict_db = copy_OUT_to_GOOD(TestInfo, InteractF=False)    
        else:
            user_reply = "" # Nothing to be done

        if user_reply in ["ALL", "NONE"]:  
            self.interaction_info = user_reply

        if user_reply not in ["YES", "ALL"]: 
            if ManualChangePreceededF: 
                TestInfo.adapt_GOOD_file_crc()
                return "MANUAL MERGE", extra_files_verdict_db
            else:
                return "UNTOUCHED", extra_files_verdict_db

        # From now on, the entry is considered to be 'Good'
        TestInfo.result().time_to_execute_sec = 0.0
        TestInfo.result().verdict             = "OK"
        if extra_files_verdict_db is None:
            extra_files_verdict_db = dict(
                (file_name, "NO")
                for file_name in TestInfo.extra_output_file_list()
            )

        return "COPIED TO GOOD", extra_files_verdict_db

    def _end_directory(self):
        self._dir_result_list.append([self._current_dir, "DONE", -1, -1])
        return None

def copy_OUT_to_GOOD(TestInfo, InteractF=True):      
    """RETURN: 
           ALL  -- user wants all files to be copied.
           NONE -- user wants no single file to be copied

       assume Dir = current directory
    """
    OUT_FileName  = TestInfo.OUT_FileName()
    GOOD_FileName = TestInfo.GOOD_FileName()

    extra_files_verdict_db = None

    reply = "YES"
    if InteractF: 
        reply = select.request_copy_OUT_to_GOOD(OUT_FileName)

    # NOTHING --> return immediately
    if reply not in ["YES", "ALL"]: 
        return reply, extra_files_verdict_db

    if os.access(GOOD_FileName, os.F_OK):
        fs.chmod(GOOD_FileName, stat.S_IWRITE)

    if not os.access(OUT_FileName, os.F_OK):
        io.on_file_does_not_exist(OUT_FileName)
        return "NO",  extra_files_verdict_db

    # -- move file from OUT/ to GOOD/
    try: 
        os.rename(OUT_FileName, GOOD_FileName)
    except:
        return "NO", extra_files_verdict_db

    if not os.access(GOOD_FileName, os.F_OK):
        io.on_file_access_error(GOOD_FileName)
        return "NO", extra_files_verdict_db

    fs.chmod(GOOD_FileName, stat.S_IREAD)

    # -- adapt the crc32 value for the given choice
    TestInfo.adapt_GOOD_file_crc()

    # -- copy extra output files into GOOD directory
    return extra_output_file_list_verdicts_copy(TestInfo)

def extra_output_file_list_verdicts_copy(TestInfo):
    """A test may specify extra files which are output and need to be 
    compared. Those files are compared binarily.
    """
    total_verdict = "YES"
    verdict_db    = {}
    for file_name in TestInfo.extra_output_file_list():
        good_file_name = TestInfo.GOOD_ExtraFileName(file_name)

        try: 
            os.rename(file_name, good_file_name)
            verdict = "COPIED TO GOOD"
        except:
            verdict = "NO"

        verdict_db[file_name] = verdict
        if verdict != "COPIED TO GOOD": total_verdict = "NO"

    return total_verdict, verdict_db
                
