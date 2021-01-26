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
# For further information see http://www.genivi.org/. 
#------------------------------------------------------------------------------
"""PURPOSE: 

The 'Comperator' provides a set of functions to compare lines or
potpourri (lines where the sequence is unimportant).

The Comperator needs to be initialized with 

           Comperator.init(...)

before the member functions can be applied.

           Comperator.lines(A, B)  compares two lines A and B
           Comperator.potpourri(A, B)  compares two lines A and B

(C) Frank-Rene Schaefer
_______________________________________________________________________________
"""
import hwut.verdict.whitespace      as     whitespace
import hwut.verdict.potpourri       as     potpourri
import hwut.verdict.happy_pattern   as     happy_pattern

class Comperator:
    analogy_db    = None
    happy_re_list = None
    es_open       = None
    es_close      = None

    @classmethod
    def init(cls, AnalogyOpen="((", AnalogyClose="))", HappyPatternList=[], ShrinkSpacesF=True, 
             BackslashIsSlashF=True):
        cls.analogy_db           = {}
        cls.es_open              = AnalogyOpen
        cls.es_close             = AnalogyClose
        cls.happy_re_list        = HappyPatternList 
        cls.shrink_spaces_f      = ShrinkSpacesF
        cls.backslash_is_slash_f = BackslashIsSlashF

        assert cls.es_close is None or len(cls.es_close) != 0
        assert cls.es_open  is None or len(cls.es_open) != 0

    @classmethod
    def lines(cls, Output, Good):
        """Compare two single lines. 

        'lines_core()' compares two lines considering also analogy spots. 
        If that function finds a definite verdict, the verdict is returned.
        Otherwise, the happy pattern check is applied, to give the two lines
        a second chance.

        RETURNS: True  -- if Output == Good
                 False -- else
        """
        verdict_f, new_analogy_db = cls.lines_core(Output, Good)

        # Add the new analogies
        cls.analogy_db.update(new_analogy_db)

        if verdict_f == True: return True
    
        output = cls.analogy_db_replace(Output)
        if happy_pattern.check(cls.happy_re_list, output, Good):
            return True

        # Remove the newly added analogies, because the line did not 
        # work anyway.
        for equivalent in new_analogy_db.iterkeys():
            del cls.analogy_db[equivalent]

        return False

    @classmethod
    def potpourri(cls, Output, Good):
        """Compare to list of lines, where the sequence is unimportant.

        'potpourri_core()' finds how lines in Output and Good can be associated.
        If no solution is found, than the chunks cannot be considered equal.
        Otherwise they can.

        RETURNS: True  -- if Output == Good
                 False -- else
        """
        verdict_f, solution_db = potpourri.compare(Output, Good, 
                                                   cls.shrink_spaces_f, 
                                                   cls.happy_re_list)
        return verdict_f

    @classmethod
    def cut_analogy_spot(cls, text):
        """RETURNS: [0] -- Analogy spot.
                        -- None, if not spot was found.
                    [1] 'text' with the analogy spot cut out.
        """
        if cls.es_open is None or cls.es_close is None:
            return None, text
        i0 = text.find(cls.es_open)
        if i0 == -1: return None, text
        i1 = text.find(cls.es_close, i0)
        if i1 == -1: return None, text
        
        return text[i0 + len(cls.es_open):i1], \
               text[:i0] + text[i1 + len(cls.es_close):]

    @classmethod
    def analogy_db_replace(cls, Line):
        line = Line
        for equivalent, original in sorted(cls.analogy_db.iteritems(), 
                                           key=lambda x: len(x[0])):
            line = line.replace(equivalent, original)
        return line
        
    @classmethod
    def analogy_db_replace_inverse(cls, Line):
        line = Line
        for equivalent, original in sorted(cls.analogy_db.iteritems(), 
                                           key=lambda x: len(x[0])):
            line = line.replace(original, equivalent)
        return line
        
    @classmethod
    def lines_core(cls, Output, Good):
        """Compares two lines 'Output' and 'Good'. It compares them with some
        tolerances. 
            
          (1) If they do not match, then all whitespace is reduced to a
              minimum and the bordering whitespace is omitted. 
          (2) If they do not match, then '\\' are treated as '\'.
          (3) If they do not match, then 'analogy spots' are considered.
              Those are spots where expectation and output may differ, but 
              differ consistently.

        Example of 'analogy spot':

         .-Output-----------------------.  .-Good-----------------------.
         |                              |  |                            |
         |     pointer: ((0x80BF323))   |  |   pointer: ((0x7000012))   |
         |     ...                      |  |   ...                      |
         |         ((0x80BF323))        |  |        ((0x7000012))       |
         '------------------------------'  '----------------------------'

        Output is, it is not required that 0x80BF323 is equal to 0x7000012, 
        but whenever 0x7000012 appears in Good, then Output shall always
        contain the same equivalent, i.e. 0x80BF323.

        RETURNS: 

          [0] Verdict (True, if lines are equal. False, if not).

          [1] Dictionary of new analogies required for both lines to be equal.
             
              map:    equivalent in Output --> original in Good.
        """
        spot, good = cls.cut_analogy_spot(Good)
        # "Output == Good" is only enough, if there is no analogy spot!
        if spot is None and Output == Good: return True, []   

        output = Output
        good   = Good
        if cls.shrink_spaces_f:
            output = whitespace.shrink(Output)
            good   = whitespace.shrink(Good)
            # "output == good" is only enough, if there is no analogy spot!
            if spot is None and output == good: return True, []   

        if cls.backslash_is_slash_f:
            output = cls.backslashinessify(output)
            good   = cls.backslashinessify(good)
            # "output == good" is only enough, if there is no analogy spot!
            if spot is None and output == good: return True, []

        new_analogy_db = {}
        while 1 + 1 == 2:
            # "output == good" is only enough, if there is no analogy spot!
            original, good = cls.cut_analogy_spot(good)
            if original is None:     
                return output == good, new_analogy_db
                
            equivalent, output = cls.cut_analogy_spot(output)
            if equivalent is None:
                return False, new_analogy_db

            elif equivalent in cls.analogy_db:
                if cls.analogy_db[equivalent] != original: 
                    return False, new_analogy_db

            elif equivalent in new_analogy_db:
                if new_analogy_db[equivalent] != original: 
                    return False, new_analogy_db
            else:
                new_analogy_db[equivalent] = original

    @classmethod
    def backslashinessify(cls, Text):
        """Adapt text so that pathnames on different platforms are treated
        the same. That is 

                   "\"     --> "/"
                   n * "/" --> "/"
                   "./"    --> ""      

        NOTE: "../" is not equal to the empty string.
        """
        text = Text

        # (1) '\' is equal to '/'
        if text.find("\\") != -1:
            text = text.replace("\\", "/")

        # quick exit ...
        if text.find("/") == -1: return text

        # (2) Multiple slashes '///' are equal to a single slash '/'.
        while text.find("//") != -1:
            text = text.replace("//", "/")

        # (3) './' but not '../' is equal to the empty string.
        i = 0
        while 1 + 1 == 2:
            i = text.find("./", i)
            if i == -1: 
                break
            elif i == 0 or text[i-1] != ".":
                text = text[:i] + text[i+2:]
                i += 2
            else:
                i += 1

        return text

