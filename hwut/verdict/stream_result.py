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
"""PURPOSE: 

Implementation of a stream-like structure. The member

             .get_next()

delivers the next contiguous set of lines to be considered. Comparisons are 
supposed to happen in sequential order. If the function returns a list, this
mean that the content is a 'potpourri'. Potpourries are sets of lines where
the sequence is unimportant.

The end of the stream is reported by a return value of 'None'.

(C) Frank-Rene Schaefer
_______________________________________________________________________________
"""
import hwut.verdict.line_category as line_category
import hwut.verdict.potpourri     as potpourri

class StreamResult:
    """Accepts stream and transforms it into a sequence of 'lines' or 'chunks'
    which can then be used to compare 'output' with 'good output'.
    """
    def __init__(self, fh, ShrinkEmptyLinesF, PotpourriF, HappyRegexList):
        assert fh is not None
        assert isinstance(ShrinkEmptyLinesF, bool)
        assert isinstance(PotpourriF, bool)

        self.fh = fh
        self.shrink_empty_lines_f = ShrinkEmptyLinesF
        self.happy_re_list        = HappyRegexList
        self.potpourri_f          = PotpourriF

    def remainder_is_empty(self):
        """RETURNS: True  -- if there were only empty lines until end of tile.
                    False -- else.
        """
        pos     = self.fh.tell()
        result  = False
        verdict = 0
        while verdict == 0:
            verdict, line = line_category.do(self.fh.readline(), self.potpourri_f, self.shrink_empty_lines_f)
            if verdict is None: # End of stream reached while there were only
                result = True   # empty lines (verdict == 0)

        self.fh.seek(pos)
        return result

    def get_next(self):
        """Reads the next 'chunk' from the input. This may be a line,
        a list of lines, or 'None'.
 
        RETURNS: 

        string    -- if the found chunk was a single raw line. 
        [strings] -- list of lines where the order of the lines is indifferent.
        None      -- if all remaining lines where either empty or comments. 
        """
        while 1 + 1 == 2:
            verdict, line = line_category.do(self.fh.readline(), self.potpourri_f, self.shrink_empty_lines_f)
            if   verdict is None: return None
            elif verdict == 0:    continue
            elif verdict == 1:    return potpourri.parse(self.fh, line, self.shrink_empty_lines_f, self.happy_re_list)
            elif verdict == 2:    return line # potpourri line block
            else:                 return line # = the stripped line
        
        assert False

    def get_plain_next(self):
        """Get the plain next line along with the verdict on it. If the verdict
        is 'begin of potpourri' ##{{ or 'end of potpourri' then the stream is 
        reset to the position where it was found. This way, 'get_next()' can
        snap the potpourri as a whole.
        """
        pos            = self.fh.tell()
        line           = self.fh.readline()
        verdict, dummy = line_category.do(line, self.potpourri_f, self.shrink_empty_lines_f)

        if verdict == 1: # potpourri open
            return verdict, potpourri.parse(self.fh, line, self.shrink_empty_lines_f, self.happy_re_list)
        else:
            # Make sure that the trailing '\n' is deleted
            return verdict, line.replace("\n", "")
        

