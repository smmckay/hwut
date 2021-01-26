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
from   hwut.strategies.core       import CoreStrategy

import hwut.auxiliary.file_system as fs
import hwut.coverage.lcov         as lcov
import hwut.auxiliary.make        as make
from   hwut.auxiliary.executer.core    import ErrorType
import hwut.common                as common
import hwut.io.messages           as io
import hwut.io.csv                as csv
import hwut.io.coverage_html      as coverage_html
import hwut.io.tap_protocol       as tap

import hwut.verdict.comparison    as comparison
import hwut.temporal_logic.engine as temporal_logic
import hwut.temporal_logic.log    as log

import os
from   copy import deepcopy

class TestExecutionStrategy(CoreStrategy):

    def __init__(self, Setup, CreateOnlyOutputF=False):
        CoreStrategy.__init__(self, Setup)

        self.create_only_output_f = CreateOnlyOutputF
        self._current_dir         = os.devnull
        self.lcov_manager         = lcov.Manager(Setup.coverage_trace_tests_f)

    def do(self, TestInfo):
        assert self._current_dir != os.devnull

        verdict = self.verdict_get(TestInfo)
        if verdict == "OK":
            verdict, \
            extra_file_verdict_db = comparison.do_extra_output_file_list(TestInfo, 
                                                                         verdict)
        else:
            extra_file_verdict_db = {}

        self.on_verdict(TestInfo, verdict, extra_file_verdict_db)

        self.coverage_analysis_on_test_done(TestInfo)

        return verdict
    
    def _start_directory(self, TestSequence):
        self._good_n      = 0
        self._total_n     = 0

        if not self._test_sequence_empty_f: make.simply_this("hwut-begin")

    def _end_directory(self):
        if not self._test_sequence_empty_f: make.simply_this("hwut-end")

        dir_verdict, good_n, total_n = self.determine_directory_verdict()
        self._dir_result_list.append(
            (self._current_dir, dir_verdict, good_n, total_n)
        )

        self._current_dir = os.devnull

        # for safety: lock all files for good in directory GOOD/
        fs.raise_write_protection("./GOOD")

    def _end_directory_tree(self):
        self.coverage_analysis_on_directory_tree_done()

    def verdict_get(self, TestInfo):
        if TestInfo.description.is_present() == False: 
            fs.try_remove(TestInfo.OUT_FileName())

            if TestInfo.description.make_dependent_f(): return "MAKE FAILED"
            else:                                       return "FAIL"

        fs.try_remove_files(TestInfo.extra_output_file_list())

        fh_output, error_type = TestInfo.execute()
        
        assert fh_output is not None

        if error_type != ErrorType.NONE:
            return "%s" % error_type
        elif self.create_only_output_f:   
            return "DONE"
        elif TestInfo.description.temporal_logic_f(): 
            return self.temporal_logic(fh_output, TestInfo)
        else:                             
            return self.traditional(fh_output, TestInfo)

    def on_verdict(self, TestInfo, Verdict, ExtraFileVerdictDb):
        if   Verdict == "OK": 
            self._good_n += 1
        elif Verdict == "NO GOOD FILE":
            self.missing_good_file_list_add(TestInfo)

        self._total_n += 1

        TestInfo.result().verdict = Verdict
        self._result_db.append((self._current_dir, 
                                TestInfo.description, 
                                deepcopy(TestInfo.result())))
        io.on_test_end(TestInfo, Verdict, ExtraFileVerdictDb)

        return Verdict

    def determine_directory_verdict(self):
        if self._total_n == 0:
            verdict = "NONE"
        elif self._total_n != self._good_n:
            failed_list = [
                (description.file_name(), result.choice)
                for dir, description, result in self._result_db
                if  dir == self._current_dir and result.verdict != "OK" and result.verdict != "SKIP"
            ]
            io.print_failure(self._current_dir, failed_list,
                             MultipleDirsF=self._multiple_directory_f)
            verdict = "FAIL"
        else:           
            assert not self.missing_good_file_list()
            io.print_ok(self._current_dir, 
                        len(self.missing_good_file_list()) != 0,
                        MultipleDirsF=self._multiple_directory_f)
            verdict = "OK"

        return verdict, self._good_n, self._total_n

    def traditional(self, fh_output, TestInfo):
        fh_good = TestInfo.GOOD_FileHandle()
        if fh_good is None:                             return "NO GOOD FILE"
        fh_output.seek(0)
        if not fh_output.read(1):                       return "NO OUTPUT"
        fh_output.seek(0)
        if comparison.do(fh_output, fh_good, TestInfo): return "OK"
        else:                                           return "FAIL"

    def temporal_logic(self, fh_output, TestInfo):
        for i, logic_file in enumerate(TestInfo.description.temporal_logic_rule_file_list()):
            log_fh = fs.open_or_die(TestInfo.OUT_FileName() + "--rule-%i" % i + ".log", "wb")
            sub_result = temporal_logic.do(logic_file, fh_output, LogSH=log_fh)
            if sub_result != "OK": return sub_result
            log_fh.close()
        return "OK" # Nothing went wrong => Oll Korrekt

    def coverage_analysis_on_test_done(self, TestInfo):
        if "lcov" in self.setup.coverage_support_set:
            self.lcov_manager.on_test_done(TestInfo, self.coverage_selector)
        
    def coverage_analysis_on_directory_tree_done(self):
        if "lcov" in self.setup.coverage_support_set:
            coverage_db = self.lcov_manager.on_directory_tree_done()
            io.coverage_summary(coverage_db)
            coverage_html.do(coverage_db)
            coverage_html.write_coverage_result(coverage_db)
            csv.write_coverage_result(coverage_db)

        if self.setup.output_tap_f:
            tap.do(self._result_db, "hwut.tap", self.setup.output_tap_subtest_f)
        
