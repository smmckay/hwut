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
import hwut.verdict.line_category  as line_category
import hwut.verdict.whitespace     as whitespace
import hwut.verdict.happy_pattern  as happy_pattern

from   operator import itemgetter

def parse(fh, FirstLine, ShrinkEmptyLinesF, HappyRegexList):
    line_list = [ FirstLine ]
    while 1 + 1 == 2:
        verdict, line = line_category.do(fh.readline(), True, ShrinkEmptyLinesF)
        if   verdict is None:  
            line_list.append("<<Error: potpourri line block not closed.>>")
            break
        elif verdict == 0:     
            continue
        elif verdict == 1:     
            line_list.append(line)
            break
        elif verdict == 2:     
            line_list.append(__get_line_block(fh, line.rstrip(), ShrinkEmptyLinesF))
        else:                  
            line_list.append(line) # = the stripped line

    return line_list

def compare(Output, Good, ShrinkSpacesF, HappyRegexList):
    """Compares two sets of lines. The order in which the lines appear
    is not important. It must only be sure that all lines appear in both.

    The analogy spots do not have any meaning inside the potpourri!

    RETURNS: 

    [0] Verdict
    [1] Dictionary telling what lines in Output match to what lines
        in Good.

        map: line index in Output --> associated line index in Good.
    """
    def default_solution_db(Output, Good):
        def good_index(Index, Line, good_db):
            stripped_line = Line.strip()
            good_i        = good_db.get(stripped_line)
            if good_i is not None:
                del good_db[stripped_line]
                return good_i
            return None

        result = {}
        if Output[0].strip() == Good[-1].strip() or Output[-1].strip() == Good[0].strip():
            result[0]             = len(Good) - 1
            result[len(Output)-1] = 0
        else:
            result[0]             = 0 
            result[len(Output)-1] = len(Good) - 1

        good_db = dict(
            (line.strip(), i) 
            for i, line in enumerate(Good)
            if i != 0 and i != len(Good) - 1
        )
        result.update(
            (i, good_index(i, line, good_db)) 
            for i, line in enumerate(Output)
            if i != 0 and i != len(Output) - 1
        )
        for output_i, good_i in result.items():
            if good_i is not None: continue
            if not good_db:        break
            good_line, default_good_i = next(iter(sorted(good_db.iteritems(), key=itemgetter(1))))
            del good_db[good_line]
            result[output_i] = default_good_i

        return result

    if Output == Good: 
        return True, default_solution_db(Output, Good)

    LOutput = len(Output)
    LGood   = len(Good)
    if LOutput != LGood: 
        return False, default_solution_db(Output, Good)

    verdict_f,      \
    alternative_db, \
    ultimative_db  = find_alternatives(Output, Good, 
                                       ShrinkSpacesF, HappyRegexList)
    if not verdict_f:
        return False, default_solution_db(Output, Good)

    # At this point, every line in Output has at least one line in Good 
    # that matches.
    if not cut_ultimative_pairs(alternative_db, ultimative_db):
        return False, default_solution_db(Output, Good)

    return get_solution_db(alternative_db, LOutput, LGood)

def find_alternatives(Output, Good, ShrinkSpacesF, HappyRegexList):
    def match(A, B):
        if   A == B:                      return True
        elif ShrinkSpacesF:
            A = whitespace.shrink(A)
            B = whitespace.shrink(B)
            if A == B:                    return True

        # HAPPY PATTERN is a MUST!
        # Otherwise, for example, sequences of file-line numbers could not be 
        # compared effectively.
        return happy_pattern.check(HappyRegexList, A, B)

    ultimative_db  = {} # good index --> output index where it is required
    alternative_db = {}

    # Find for each output line the good lines that match.
    # Give lines a chance to match with happy patterns
    for i, output in enumerate(Output):
        # list of line indices in good that match line 'i'.
        match_list = []
        for k, good in enumerate(Good):
            if k in ultimative_db:   continue # 'k' is already required ultimatively.
            elif match(output, good): match_list.append(k)

        if not match_list:         
            return False, None, None
        elif len(match_list) == 1: 
            good_i                = match_list[0]
            ultimative_db[good_i] = i

        alternative_db[i] = match_list

    return True, alternative_db, ultimative_db

def cut_ultimative_pairs(alternative_db, ultimative_db):
    """RETURNS: False -- if match is impossible.
                True  -- if match remains possible.
    """
    # Cut the 'ultimative pairs' from the options of the remaining.
    change_f = True
    while change_f:
        change_f = False
        for i, match_list in alternative_db.items():
            len_before = len(match_list)

            # Delete all 'k' which are already required ultimatively.
            for good_i, output_i in ultimative_db.iteritems():
                if good_i in match_list and output_i != i: 
                    match_list.remove(k)

            if   len(match_list) == 0: 
                # If the match list is empty, then match verdict = False
                return False

            elif len(match_list) == 1 and len_before != 1: 
                # If there's only one possible match, then it is ultimative.
                good_i                = match_list[0]
                ultimative_db[good_i] = i
                change_f              = True
    return True

def get_solution_db(alternative_db, LOutput, LGood):
    solution_db = dict(
        (i, match_list[0]) 
        for i, match_list in alternative_db.iteritems()
        if len(match_list) == 1
    )

    if LOutput == len(solution_db) and LOutput == LGood: 
        return True, solution_db
            
    plain_alternative_db = dict(
        (i, match_list) 
        for i, match_list in alternative_db.iteritems()
        if len(match_list) > 1
    )

    solution = satisfy(plain_alternative_db)
    if solution is None:
        return False, solution_db

    solution_db.update((i, k) for i, k in solution)

    # All lines where either equal or matched by happy patterns.
    if LOutput == len(solution_db) and LOutput == LGood: 
        return True, solution_db
    else:                           
        return False, solution_db

def __get_line_block(fh, FirstLine, ShrinkEmptyLinesF):
    """Parse a block in between '^----" to "^----" where ^ is the
    begin of line marker.

    RETURNS: Joined content of that block into a string.
    """
    line_list = [ "%s\n" % FirstLine ]
    while 1 + 1 == 2:
        verdict, line = line_category.do(fh.readline(), True, ShrinkEmptyLinesF)
        if   verdict is None:  
            line_list.append("<<Error: potpourri line block not closed.>>")
            break
        elif verdict == 0:     
            continue
        elif verdict == 1:     
            line_list.append("<<Error: end of potpourri before end of line block.>>")
            break
        elif verdict == 2:     
            line_list.append(line.rstrip()) # No newline
            break
        else:                  
            line_list.append("%s\n" % line.rstrip()) # = the stripped line

    return "".join(line_list)

def satisfy(AlternativeDb):
    """Find assignments to parameters based on possible alternatives.

                  AlternativeDb[p] --> [x0, x1, x2, ...]

    where x0, x1, x2, ... are the values which would satisfy parameter 'p' 
    as assignment. Each of the values x0, x1, x2 ... can appear at max. 
    ONCE in the solution.

    TODO: Analys this algorithm for COMPLEXITY!

    RETURNS: 

    None -- There is no solution where each parameter receives an assignment
            from its alternatives.

    List -- A list of pairs (p, x) that tells that 'p' is assigned to 'x'. 
            For each 'p' in the keys of AlternativeDb, there is an 'x' 
            that fits its alternatives.
    """
    L = len(AlternativeDb)
    if len(AlternativeDb) == 0: 
        return []

    # Determine the set of possible assignments in total
    remainder = set()
    for alternatives in AlternativeDb.itervalues():
        remainder.update(alternatives)

    # map: cursor index to parameter index
    # That is 'cursor[i]' defines the setting of parameter 'map_i_to_p[i]'
    map_i_to_p = AlternativeDb.keys()
    cursor     = [0] * L
    # number of values for cursor[i]
    dim        = [ len(AlternativeDb[map_i_to_p[i]]) for i in xrange(L) ]

    i = 0
    while 1 + 1 == 2:
        choice = AlternativeDb[map_i_to_p[i]][cursor[i]]
        if choice not in remainder:
            # Choice not available in remainder. Go back.
            cursor[i] += 1
            while cursor[i] == dim[i]:
                if i == 0: return None # No Solution!
                i -= 1
                # Re-add the choice which has been removed.
                remainder.add(AlternativeDb[map_i_to_p[i]][cursor[i]])
                cursor[i] += 1

        elif i == L - 1:
            # Found Solution!
            return [ 
                (map_i_to_p[i], AlternativeDb[map_i_to_p[i]][cursor[i]]) 
                for i in xrange(L) 
            ] 

        else:
            # Remove the choice for later selections.
            remainder.remove(choice)
            i += 1
            cursor[i] = 0

