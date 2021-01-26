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

This class provides streams that can be used in a diff-tool (vimdiff, WinMerge, 
Kdiff3, etc.). The streams are configured in a way so that the diff-tools
display HWUT's way of looking at things. 

For that the output and the nominal output (Good) is interpreted. The display, 
though, is valid 'hwut syntax'. So that merging or copying from output to 
good is still possible. The streams are configured in a way so that the diff-tools
display HWUT's way of looking at things. 

For that the output and the nominal output (Good) is interpreted. The display, 
though, is valid 'hwut syntax'. So that merging or copying from output to 
good is still possible.

Implementation of a stream-like structure. The member

             .get_next()

delivers PAIRS of blocks (A, B) where 'A' is the next block to be sent to the
output stream. 'B' is the next block to be sent to the 'good' stream.

The end of the stream is reported by a return value of 'None, None'.

(C) Frank-Rene Schaefer
_______________________________________________________________________________
"""
from   hwut.verdict.stream_result import StreamResult
from   hwut.verdict.comperator    import Comperator
import hwut.verdict.potpourri     as     potpourri
import hwut.verdict.whitespace    as     whitespace


class StreamDiffView(Comperator):
    """Provides a diff-stream for output and good that can be viewed 
    conveniently with 'diff-tools'. 

    Only real errors will appear different!
    """
    def __init__(self, fh_output, fh_good, ShrinkSpacesF, ShrinkEmptyLinesF, PotpourriF, HappyRegexList):
        assert fh_output is not None
        assert fh_good is not None
        assert isinstance(ShrinkSpacesF, bool)
        assert isinstance(ShrinkEmptyLinesF, bool)

        self.output         = StreamResult(fh_output, ShrinkEmptyLinesF, PotpourriF, HappyRegexList)
        self.good           = StreamResult(fh_good, ShrinkEmptyLinesF, PotpourriF, HappyRegexList)
        self.shrink_space_f = ShrinkSpacesF
        
    def treat_lines(self, Output, Good):
        """Output, Good are lines.
        """
        if self.__class__.lines(Output, Good):
            return Output, whitespace.fit(Good, Output)
        return Output, Good

    def treat_potpourri(self, Output, Good):
        """Output, Good are lists of lines.
        """
        # Good and Output must at least contain two lines containing
        # the markers '||||'! 
        assert type(Output) == list and len(Output) >= 2
        assert type(Good) == list and len(Good) >= 2
        
        verdict_f, solution_db = potpourri.compare(Output, Good, self.shrink_space_f, self.happy_re_list)
        if verdict_f == True:
            return zip(Output, Output)

        matched_good   = set(solution_db.itervalues())
        unmatched_good = set(i for i in xrange(len(Output)) if i not in matched_good)

        def consider_borders(solution_db, Lo, Lg):
            def select(*Options):
                for option in Options:
                    if option in unmatched_good:
                        if option is not None: unmatched_good.remove(option)
                        return option
            
            if 0 not in solution_db:
                solution_db[0] = select(0, Lg - 1, None)    

            if Lo - 1 not in solution_db:
                solution_db[Lo - 1] = select(Lg - 1, 0, None)    

        def fill_unmatched_output(solution_db, Lo, unmatched_good):
            for i in xrange(Lo):
                if i in solution_db: continue
                # Find best matching of the unmatched good.
                match_k = unmatched_good.pop() # TODO: find a better way to get best match!
                solution_db[i] = match_k

        Lo = len(Output)
        Lg = len(Good)

        consider_borders(solution_db, Lo, Lg)
        fill_unmatched_output(solution_db, Lo, unmatched_good)

        def append(result, A, B):
            a_line_n = A.count("\n")
            b_line_n = B.count("\n")
            if   a_line_n > b_line_n: B += "\n" * (a_line_n - b_line_n)
            elif b_line_n > a_line_n: A += "\n" * (b_line_n - a_line_n)
            result.append((A, B))

        NO_MATCH = "|  ??  |"
        result   = []
        for output_i, good_i in sorted(solution_db.iteritems(), key=lambda x: x[0]):
            output_line = Output[output_i]
            if good_i is None or good_i >= len(Good): good_line = NO_MATCH
            else:                                     good_line = Good[good_i]
            append(result, output_line, good_line)

        for good_i in sorted(unmatched_good):
            append(result, NO_MATCH, Good[good_i])
            
        return result

    def iterable(self):
        def safe(verdict, Text):
            if verdict == 1: return "".join(Text)
            else:            return Text

        while 1 + 1 == 2:
            # Comments in output: mirror them to good 
            while 1 + 1 == 2:
                out_verdict, output_line = self.output.get_plain_next()
                # Empty lines and comments can be flushed on both sides.
                if out_verdict != 0: break
                yield output_line, output_line

            # Comments in good: drop and forget
            while 1 + 1 == 2:
                good_verdict, good_line = self.good.get_plain_next()
                if good_verdict != 0: break
                # Drop comments and empty lines in good files.

            # End of output --> flush remaining good lines
            if out_verdict is None: 
                # End of output has been reached. Flush remaining good lines.
                while good_verdict is not None:
                    yield "", safe(good_verdict, good_line)
                    good_verdict, good_line = self.good.get_plain_next()
                return  # The End

            # End of good --> flush remaining output lines
            elif good_verdict is None:
                while out_verdict is not None:
                    yield safe(out_verdict, output_line), ""
                    out_verdict, output_line = self.output.get_plain_next()
                return # The End

            # Potpourri --> treat.
            elif out_verdict == 1 and good_verdict == 1: 
                result = self.treat_potpourri(output_line, good_line)
                for output_line, good_line in result:
                    yield output_line, good_line

            else:
                output_line = safe(out_verdict, output_line)
                good_line   = safe(good_verdict, good_line)

                good_line    = self.__class__.analogy_db_replace(good_line)
                output_line, \
                good_line    = self.treat_lines(output_line, good_line)
                good_line    = self.__class__.analogy_db_replace_inverse(good_line)
                yield output_line, good_line
        
        assert False

    def flush(self, fh_out, fh_good):

        for content in self.iterable():
            if content is None: 
                return
            elif type(content) == list:
                for output_line, good_line in content:
                    fh_out.write(output_line)
                    fh_good.write(good_line)
                fh_out.write("\n")
                fh_good.write("\n")
            else:
                output, good = content
                fh_out.write("%s\n" % output)
                fh_good.write("%s\n" % good)
        return 

