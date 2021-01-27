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
import sys

import hwut.verdict.whitespace    as     whitespace
from   hwut.verdict.stream_result import StreamResult
from   hwut.verdict.comperator    import Comperator

def do(fh_output, fh_good, TestInfo): 
    """Compares the two streams 'fh_output' and 'fh_good'. 

    RETURNS: True  -- if the content of both is equal (according to HWUT's
                      way of looking at things).
             False -- else.

    CRITERIA: 

      -- Any number of empty lines is ignored. 
      -- Lines starting or ending with '##' as first or last non
         whitespace are ignored.
      -- Any beginning or ending whitespace is omitted.
      -- Any sequence of whitespace in a line ('\t' or ' ') is considered
         as a single whitespace.
      -- Analogy spots of the for '((something))' require only that
         the text in between '((' and '))' is consistent, not necessarily
         the same. 
      -- Lines in between '||||' and '||||' do not have a designated order
         of appearance. No analogy spots in these regions allowed!
    """
    descr = TestInfo.description
    AnalogyOpen       = descr.analogy_open_str() 
    AnalogyClose      = descr.analogy_close_str() 
    HappyRegexList    = descr.happy_pattern_list() 
    PotpourriF        = descr.shrink_space_f() 
    ShrinkSpacesF     = descr.shrink_space_f() 
    ShrinkEmptyLinesF = descr.shrink_empty_lines_f()
    BackslashIsSlashF = descr.backslash_is_slash_f()

    Comperator.init(AnalogyOpen, AnalogyClose, HappyRegexList, ShrinkSpacesF, 
                    BackslashIsSlashF)

    sr_output = StreamResult(fh_output, ShrinkEmptyLinesF, PotpourriF, 
                             HappyRegexList)
    sr_good   = StreamResult(fh_good, ShrinkEmptyLinesF, PotpourriF, 
                             HappyRegexList)
    
    while 1 + 1 == 2:
        good_pos   = sr_good.fh.tell()
        output_pos = sr_output.fh.tell()
        good       = sr_good.get_next()
        output     = sr_output.get_next()

        if output is None and good is None:
            return True
        if output is None:             
            sr_good.fh.seek(good_pos)             # If the remainder is empty 
            return sr_good.remainder_is_empty()   # or only comment, forgive.
        elif good is None:             
            sr_output.fh.seek(output_pos)         # If the remainder is empty 
            return sr_output.remainder_is_empty() # or only comment, forgive.
        elif type(output) != type(good): 
            return False
        elif type(good) == list: 
            if not Comperator.potpourri(output, good): return False
        else:
            if not Comperator.lines(output, good):     return False

    assert False

def do_plain(fh_a, fh_b):
    """RETURNS: True  -- if the file contents are the same.
                False -- if not.
    """
    while 1 + 1 == 2:
        chunk_a = fh_a.readline(8192)
        chunk_b = fh_b.readline(8192)
        if   chunk_a != chunk_b: return False
        elif len(chunk_a) == 0:  return True   # Both reached end of stream.

            
def do_extra_output_file_list(TestInfo, TestVerdict):
    """A test may specify extra files which are output and need to be 
    compared. Those files are compared binarily.
    """
    def binary_comparison(FileName):
        try:    out_fh = open(FileName, "rb")
        except: return "NOT FOUND" 
        try:    good_fh = open(TestInfo.GOOD_ExtraFileName(FileName), "rb")
        except: return "NO GOOD FILE" 

        verdict_f = (out_fh.read() == good_fh.read())

        out_fh.close()
        good_fh.close()
        if not verdict_f: return "FAIL"
        else:             return "OK"

    total_verdict = TestVerdict
    verdict_db    = {}
    for file_name in TestInfo.extra_output_file_list():
        verdict = binary_comparison(file_name)
        verdict_db[file_name] = verdict
        if verdict != "OK": total_verdict = "FAIL"

    return total_verdict, verdict_db
                
