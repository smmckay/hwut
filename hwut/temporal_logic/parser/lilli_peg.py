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
import hwut.temporal_logic.parser.lexical_analysis as lex
from hwut.temporal_logic.classes.statement_element    import SourceCodeOrigin, reject, Fork, NodeNull
from hwut.temporal_logic.classes.action_function_call import *
from hwut.temporal_logic.classes.primary              import *
from hwut.temporal_logic.classes.action               import *


import sys
import types

DEBUG = False

class Repeat:
    def __init__(self, TokenList, MinN=0, MaxN=-1):
        if MaxN != -1 and MaxN < MinN:
            return SyntaxError("Max. repetition number '%i' lesser than min. repetition number '%i'." \
                               % (MaxN, MinN))
        self.token_list = TokenList
        self.max_n      = MaxN
        self.min_n      = MinN

    def repeated_token_list(self):
        return self.token_list

class Chain:
    def __init__(self, HeadTokenList, TailTokenList, MinN=0, MaxN=-1):
        assert type(HeadTokenList) == list
        assert type(TailTokenList) == list
        assert type(MinN) == int
        assert type(MaxN) == int
        if MaxN != -1 and MaxN < MinN:
            return SyntaxError("Max. repetition number '%i' lesser than min. repetition number '%i'." \
                               % (MaxN, MinN))
        self.head_token_list = HeadTokenList
        self.tail_token_list = TailTokenList
        self.max_n = MaxN
        self.min_n = MinN

    def repeated_token_list(self):
        return self.tail_token_list

class Regress:
    def __init__(self, First, OperatorList, Follow):
        self.first         = First
        self.operator_list = OperatorList
        self.follow        = Follow
        self.name          = "Term"

def __snap_repetition(sh, pos, Name, repeat):
    TokenListSpec = repeat.repeated_token_list()
    MinN          = repeat.min_n
    MaxN          = repeat.max_n

    sub_result_list = []
    while 1 + 1 == 2:
        result = _sequence(sh, Name + ":Repeat", TokenListSpec, None)
        if result.error(): break
        sub_result_list.append(result)

    N = len(sub_result_list)
    if N < MinN:                
        result.add_for_what("Min. number of repetitions not reached.")
        return result
    if MaxN != -1 and N > MaxN: 
        result.add_for_what("Max. number of repetitions exceeded.")
        return result

    return Fork(sub_result_list)

def __snap_headed_repetition(sh, pos, Name, repeat):
    result_1 = _sequence(sh, Name + ":Chain", repeat.head_token_list, Fork)
    if result_1.error():
        if repeat.min_n != 0: return result_1    # Error
        else:                 return Fork([])

    # The first one has been dealt with already
    repeat.min_n -= 1
    result_2 = __snap_repetition(sh, pos, Name, repeat)
    repeat.min_n += 1
    if result_2.error():      return result_2          # Error

    result_list = [ result_1.sub_node_list[0] ] 
    for result in result_2.sub_node_list:
        result_list.append(result)
    return Fork(result_list)

def __snap_option(sh, pos, Name, option_set):
    sub_pos = sh.tell()
    # Optional Token (one of a list)
    for option in option_set:
        if option is None: continue
        elif type(option) == str:                result = lex.word(sh, option)
        elif type(option) == types.FunctionType: result = option(sh) 
        else:                                    assert False
        if result.ok(): return result
    else:
        if None in option_set: # Nothing is acceptable
            return NodeNull()
        else:                  # None of the options fit into the play
            return reject(sh, pos, option_set)

def __snap_regress(sh, pos, Name, comb):
    expr = comb.first(sh)
    if expr.error(): 
        return expr

    sub_pos = sh.tell()
    op = lex.word_options(sh, comb.operator_list)
    if op.error():  
        return expr

    while 1 + 1 == 2:
        expr2 = comb.follow(sh)
        if expr2.error():
            sh.seek(sub_pos)
            return expr

        expr = Action_BinaryOp([expr, op, expr2])

        sub_pos = sh.tell()
        op = lex.word_options(sh, comb.operator_list)
        if op.error():  return expr

class ErrorFrame:
    """Maintain information about occurring errors for one particular
    parsing frame.
    """
    deepest_error = None
    def __init__(self):
        self.longest_match  = -1
        self.candidate_list = None

    def register(self, result):
        if result.stream_position() > self.longest_match:
            self.longest_match  = result.stream_position()
            self.candidate_list = [ result ]
        elif result.stream_position() == self.longest_match:
            self.candidate_list.append(result)
    
    def close(self):
        # Generate a combined error message of all reclaimed things.
        if    ErrorFrame.deepest_error is None \
           or ErrorFrame.deepest_error.stream_position() < self.longest_match:
            ErrorFrame.deepest_error = self.candidate_list[0]
            for candidate in self.candidate_list[1:]:
                ErrorFrame.deepest_error.extend_missing(candidate.missing)

class NodeCache(dict):
    """A database of nodes and at what stream position they matched. The goal is
    to cut down analysis time. When a broader rule fails, it does not have to 
    investigate all rules in the tree again.
    """
    def enter(self, sh, Name, StartPos, Result):
        """Register that at the position 'StartPos' a token 'Result' has been
        identified successfully. The token ends at position 'sh.tell()'
        """
        entry = dict.get(self, Name)
        if entry is None: entry = {}; self[Name] = entry
        entry[StartPos] = (Result, sh.tell())
        return Result

    def get(self, sh, Name):
        """See, if for the rule with the given Name, there is a result that has 
        been registered at the current position 'sh.tell()'.
        """
        entry = dict.get(self, Name)
        if entry is None:     return None
        sub_entry = entry.get(sh.tell())
        if sub_entry is None: return None
        sh.seek(sub_entry[1])
        return sub_entry[0]

    def clear(self):
        dict.clear(self)

node_cache = NodeCache()

__depth = 0
def _sequence(sh, Name, TokenList, result_container, AdditionalArgList=None):
    global __depth
    pos         = sh.tell()
    result_list = []

    def on_error(sh, pos, index, Name):
        sh.seek(pos)
        result.set_error_token_index(index)
        result.add_for_what(Name)
        return result

    def handle_result(result_container):
        if result_container is None: 
            return result_list[0]

        elif type(result_container) == str:
            return Fork(result_list, Name=result_container)

        elif type(result_container) == types.InstanceType:
            result_container.set_argument_list(result_list)
            return result_container

        elif type(result_container) == types.ClassType:
            if AdditionalArgList is None: return result_container(result_list)
            else:                         return result_container(AdditionalArgList + result_list)

        assert False

    __depth += 1

    if DEBUG:
        print ("    " * __depth) + Name + ":%i: " % pos + __repr_token_list(TokenList)
        pos = sh.tell()
        print ("    " * __depth + " " * len(Name)) + "[%s ...]" % sh.read(32)
        sh.seek(pos)

    for index, element in enumerate(TokenList):
        if   element.__class__ == Repeat:         result = __snap_repetition(sh, pos, Name, element)
        elif element.__class__ == Chain:          result = __snap_headed_repetition(sh, pos, Name, element)
        elif element.__class__ == Regress:        result = __snap_regress(sh, pos, Name, element)
        elif element.__class__ == list:           result = __snap_option(sh, pos, Name, element)
        elif type(element) == str:                lex.skip_whitespace(sh); result = lex.word(sh, element)
        elif type(element) == types.FunctionType: lex.skip_whitespace(sh); result = element(sh)
        else:                                     assert False

        assert type(result) in (types.ClassType, types.InstanceType), \
               "Error: received result '%s' (%s) for %s." % (repr(result), repr(type(result)), Name)

        if not result.ok():        
            __depth -= 1
            if DEBUG:
                print ("    " * __depth) + ": FAIL on %i" % index, repr(element)
            return on_error(sh, pos, index, Name)
    
        elif type(element) != str: 
            result_list.append(result)

    __depth -= 1
    if DEBUG:
        print ("    " * __depth) + ": OK"

    return handle_result(result_container)

def _alternatives(sh, *Alternatives):
    """Alternatives: A list of tuples of size 1 or 2 containing alternatives of 
                     sequences to be matched. 

       For each element in Alternatives, it holds that:

            element[0] is the sequence to be matched against.
            element[1] contains the result container.

       optionally 

            element[2] contains the additional argument list.
    """
    global node_cache
    def get(Element):
        if len(Element) <= 2: return Element[0], Element[1], None
        else:                 return Element[0], Element[1], Element[2]

    start_pos = sh.tell()

    Name   = sys._getframe(1).f_code.co_name # Name of calling function/rule
    result = node_cache.get(sh, Name)
    if result is not None: return result
    
    error_frame = ErrorFrame()

    for element in Alternatives:
        token_list, result_container, additional_argument_list = get(element)
        
        result = _sequence(sh, Name, token_list, result_container, 
                           additional_argument_list)

        if result.ok(): return node_cache.enter(sh, Name, start_pos, result)
        else:           error_frame.register(result)

    error_frame.close()

    return node_cache.enter(sh, Name, start_pos, error_frame.candidate_list[0])

def get_syntax_error():
    global __deepest_error
    return ErrorFrame.deepest_error

def __repr_token_list(TokenList):
    txt = ""
    for element in TokenList:
        if   type(element) == str:                txt += repr(element) + " "
        elif type(element) == types.FunctionType: txt += element.func_name + " "
        elif type(element) == list:               txt += "[" + __repr_token_list(element) + "] "
        else:                                     txt += "Repeat"
    return txt

