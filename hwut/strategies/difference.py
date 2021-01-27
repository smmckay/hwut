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
import os
import stat
import shutil

import hwut.common                as common
from   hwut.test_db.test          import Test
import hwut.auxiliary.file_system as fs
import hwut.io.messages           as io
import hwut.verdict.comparison    as comparison
#
from   hwut.strategies.accept import AcceptStrategy
from   hwut.strategies.test   import TestExecutionStrategy
#  
from   hwut.verdict.stream_diff_view import StreamDiffView
import hwut.verdict.comparison       as     comparison

class DifferenceDisplayStrategy(AcceptStrategy):

    def __init__(self, Setup):
        assert Setup.grant in ["ALL", "NONE", "INTERACTIVE"]

        self.display_program  = Setup.diff_display_application()
        self.setup            = Setup

        AcceptStrategy.__init__(self, Setup)

    #   _start_directory() <-- AcceptStrategy

    def do(self, TestInfo):
        # -- display only, if:  (1) OUT and GOOD files exist
        #                       (2) content of files differs
        assert isinstance(TestInfo, Test)
        assert self.interaction_info in ["ALL", "NONE", "INTERACTIVE"]

        if TestInfo.description.is_present() == False:
            fs.try_remove(TestInfo.OUT_FileName()) 
            io.on_test_end(TestInfo, "MAKE FAILED")
            return "MAKE FAILED"
        
        # -- If requested, then execute test program.
        if self.setup.execution_f:
            # output is written automatically to 'TestInfo.OUT_FileName()'
            fh_out, dummy = TestInfo.execute()
        else:
            fh_out = TestInfo.OUT_FileHandle()

        if TestInfo.description.temporal_logic_f():
            result = "LOGIC DEP"
        else:
            fh_good = TestInfo.GOOD_FileHandle()
            if   fh_good is None:                          result = "NO GOOD FILE"
            elif comparison.do(fh_out, fh_good, TestInfo): result = "NO DIFFERENCE"
            else:                                          result = "FAIL"

        # -- If requested, then execute test program.
        io.on_test_end(TestInfo, result)

        if   result == "NO DIFFERENCE": return "OK"
        elif result != "FAIL":          return result

        self.generate_tmp_display(TestInfo) 

        # -- Show the differences (maybe user changes some stuff)
        good_before = "%s.before" % TestInfo.GOOD_tmp_FileName()
        good_tmp    = TestInfo.GOOD_tmp_FileName()
        out_tmp     = TestInfo.OUT_tmp_FileName()

        shutil.copy2(good_tmp, good_before)

        os.system("%s %s %s" % (self.display_program.strip(), out_tmp, good_tmp))

        # -- Check wether the user has tampered with the good file using
        #    the merger. 
        # NOTE: The difference display stream may have changed the '.tmp'
        #       file. So, simply comparing good and good.tmp is not enough
        #       to detect whether the user manually edited the file.
        manual_change_f = False
        fh_good_tmp        = fs.open_or_die(good_tmp, "rb")
        fh_good_tmp_before = fs.open_or_die(good_before, "rb")

        verdict_f = comparison.do_plain(fh_good_tmp, fh_good_tmp_before)

        fh_good.close()
        fh_good_tmp.close()

        if not verdict_f:
            fs.rename_file(good_tmp, TestInfo.GOOD_FileName())
            manual_change_f = True

        fs.try_remove(good_tmp)
        fs.try_remove(good_before)

        # -- copy protocol files of all specified choices
        verdict, extra_file_verdict_db = AcceptStrategy._do(self, TestInfo, manual_change_f)
        io.on_test_end(TestInfo, verdict, extra_file_verdict_db)

    def generate_tmp_display(self, TestInfo):
        """Considering the HWUT way of looking at things, this function generates
        temporary files. The two temporary files for OUT and GOOD are designed to
        display the HWUT's criteria transparently when used with a diff-tool such 
        as vimdiff, WinMerge and the like.
        """
        fh_out      = TestInfo.OUT_FileHandle()
        fh_good     = TestInfo.GOOD_FileHandle()
        fh_out_tmp  = TestInfo.OUT_tmp_FileHandle("wb")
        fh_good_tmp = TestInfo.GOOD_tmp_FileHandle("wb")

        sdv = StreamDiffView(fh_out, fh_good, 
                             TestInfo.description.shrink_space_f(), 
                             TestInfo.description.shrink_empty_lines_f(), 
                             TestInfo.description.potpourri_f(), 
                             TestInfo.description.happy_pattern_list())

        sdv.flush(fh_out_tmp, fh_good_tmp)
        fh_out_tmp.close()
        fh_good_tmp.close()
        fh_out.close()
        fh_good.close()
        os.chmod(TestInfo.OUT_tmp_FileName(), stat.S_IREAD | stat.S_IWRITE)
        os.chmod(TestInfo.GOOD_tmp_FileName(), stat.S_IREAD | stat.S_IWRITE)



