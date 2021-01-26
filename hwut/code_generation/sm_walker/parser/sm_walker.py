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
import hwut.code_generation.generator.parser.generator  as     generator
from   hwut.code_generation.generator.parser.parameter  import skip_whitespace_in_line, \
                                                               check, \
                                                               snap_identifier
from   hwut.code_generation.sm_walker.sm_walker         import State, \
                                                               StateTransition, \
                                                               StateMachineWalker,\
                                                               condition_negate
import hwut.temporal_logic.parser.lexical_analysis      as     T
from   hwut.temporal_logic.parser.lexical_analysis      import _get_current_line_n
from   hwut.code_generation.function_stubs.c.core       import skip_whitespace

from   collections import namedtuple
import sys


UserCode = namedtuple("UserCode_tuple", ("file_name", "line_n", "text"))

class TransitionInfo:
    def __init__(self, FromStateName, ToStateName, ConditionName, EventName, PostConditionName):
        self.from_state_name     = FromStateName
        self.condition_name      = ConditionName
        self.event_name          = EventName
        self.post_condition_name = PostConditionName
        self.to_state_name       = ToStateName

    def complete(self, PrevFromStateName, PrevToStateName, CurrFromStateName, CurrToStateName):
        if self.from_state_name == "'":
            if PrevFromStateName is None:
                print "Error: no previous state. Cannot use '-- to refer to last state."
            elif PrevFromStateName == ".":
                print "Error: cannot resolve mutual reference between previous and subsequent state."
            else:
                self.from_state_name = PrevFromStateName

        if self.to_state_name == "'":
            if PrevToStateName is None:
                print "Error: no previous state. Cannot use '-- to refer to last state."
            elif PrevToStateName == ".":
                print "Error: cannot resolve mutual reference between previous and subsequent state."
            else:
                self.to_state_name = PrevToStateName

        if CurrToStateName is not None and self.from_state_name == ".":
            self.from_state_name = CurrFromStateName

        if CurrFromStateName is not None and self.to_state_name == ".":
            self.to_state_name = CurrToStateName

        return self.is_complete()

    def is_complete(self):
        if   self.from_state_name == "'": return False
        elif self.to_state_name   == "'": return False
        elif self.from_state_name == ".": return False
        elif self.to_state_name   == ".": return False
        else:                             return True

    def __str__(self):
        return "".join([
            "{ .from: %s; "    % self.from_state_name,
            ".to: %s; "        % self.to_state_name,
            ".condition: %s; " % self.condition_name,
            ".event: %s; }"    % self.event_name,
        ])

def do(fh, info_db):
    walker = do_walker(fh, info_db)
    walker.event_code_db, \
    walker.condition_code_db = do_specifications(fh)
    return walker
    
def do_walker(fh, info_db):
    init_state_name = None
    prev_from_state = None
    prev_to_state   = None
    on_hold         = []
    state_db        = {}
    while not generator.is_dash_line(fh):
        tmp = fh.read(1)
        if not tmp: print "Error: Premature end of file"; break
        else:       fh.seek(-1, 1)
        if generator.is_empty_line(fh): continue

        info = parse_line(fh)

        if info.complete(prev_from_state, prev_to_state, None, None):
            prepare(state_db, info)
        else:                  
            on_hold.append(info)
            
        i = len(on_hold) - 1
        while i >= 0:
            if on_hold[i].complete(prev_from_state, prev_to_state, 
                                   info.from_state_name, info.to_state_name):
                prepare(state_db, on_hold[i])
                del on_hold[i]
            i -= 1

        if init_state_name is None and info.from_state_name not in ("'", "."):
            init_state_name = info.from_state_name

        prev_from_state = info.from_state_name
        prev_to_state   = info.to_state_name

    if len(on_hold) != 0:
        print "Error: reference to subsequent state by '.', but no such state is defined."

    # Make sure that: init state comes first.
    #                 intermediate states come after all normal states
    def sort_key(x):
        if   x.name == init_state_name: return 0 
        elif not x.intermediate_f:      return 1
        else:                           return 2

    state_list = sorted(state_db.values(), key=sort_key)
    assert state_list[0].name == init_state_name 

    return StateMachineWalker(info_db["name"], 
                              state_list,
                              info_db["user_data_type"], 
                              info_db["max_path_length"], 
                              info_db["max_loop_n"]) 

def do_specifications(fh):
    """Parse:
                ---// EVENTS //----------------------

                      SOMETHING { code ... }
                      ELSE      { code ... }

                ---// CONDITIONS //------------------

                      SOMETHING { code ... }
                      ELSE      { code ... }
    """
    event_code_db     = {}
    condition_code_db = {}
    skip_whitespace(fh)
    while generator.is_dash_line(fh):
        section_name = generator.parse_dash_line_special(fh)
        if section_name == "EVENTS":
            event_code_db     = parse_specifications(fh, "EVENTS")
        elif section_name == "CONDITIONS":
            condition_code_db = parse_specifications(fh, "CONDITIONS")
        elif section_name is not None:
            print "Error: unknown section '%s'" % section_name
            return event_code_db, condition_code_db
        else:
            fh.readline() # skip the dash-line
            break
        skip_whitespace(fh)

    return event_code_db, condition_code_db

def prepare(state_db, info):
    assert info.to_state_name is not None
    assert info.from_state_name is not None
    to_state = state_db.get(info.to_state_name)
    if to_state is None:
        state_db[info.to_state_name] = State(info.to_state_name, [])

    from_state = state_db.get(info.from_state_name)
    if from_state is None:
        from_state = State(info.from_state_name, [])
        state_db[info.from_state_name] = from_state

    if info.post_condition_name is None:
        from_state.transition_list.append(
            StateTransition(info.event_name, info.condition_name, 
                            info.to_state_name)
        )
    else:
        # Transition with post-condition
        #
        #  state ---| condition |---( event )----| post-condition |---- to_state
        #
        # Implement as:
        #
        #  state ---| pre-condition |----( event )---- *intermediate*
        #
        #  *intermediate* ----| post-condition |-------- to_state
        #        '------------| not post-condition |---- state
        #
        intermediate = from_state.get_intermediate_state(state_db) 
        from_state.transition_list.append(
            StateTransition(info.event_name, info.condition_name, 
                            intermediate.name)
        )
        intermediate.transition_list.append(
            StateTransition(None, info.post_condition_name, 
                            info.to_state_name)
        )
        intermediate.transition_list.append(
            StateTransition(None, condition_negate(info.post_condition_name), 
                            from_state.name)
        )
        

def parse_line(fh):
    """Parses a line of the form:

         SOURCE_STATE --| condition |---( event )--- TARGET_STATE

    In any line after the first line the single quote may be used to refer
    to the last state in that position. To refer to the following state at 
    that position to . may be used. That is, the following is possible:

               .--------| x_l_1  |---( START )------.        
         SOURCE_STATE --| x_g_0  |---( STOP )--- TARGET_STATE
               '--------| x_le_0 |---( STOP )-------'

         SOURCE_STATE ---------------( ALARM )------.
               '---------------------( WAKE )-------.
         SOURCE_STATE --| x_g_0  |---( STOP )--- OTHER_STATE

    """
    from_state = snap_state_name(fh)
    if from_state is None:
        print "Error: missing source state."
        fh.seek(pos)
        return None
        
    condition_name, event_name, post_condition_name = snap_transition(fh)

    to_state   = snap_state_name(fh)
    if to_state is None:
        print "Error: missing target state."

    return TransitionInfo(from_state, to_state, condition_name, event_name, post_condition_name)

def snap_transition(fh):
    """Parses a line:

            --| CONDITION |----( EVENT )----| POST_CONDITION |---

    """
    condition_name      = get_step(fh, "||", "condition")
    event_name          = get_step(fh, "()", "event")
    post_condition_name = get_step(fh, "||", "post condition")

    if event_name is None and condition_name is not None and post_condition_name is not None:
        print "Error: pre- and post-conditions without an event does not make sense."
        return None, None

    skip_whitespace_in_line(fh)
    end_marker = generator.snap_line(fh)
    if end_marker is None:
        print "Error: missing dashed line."
    fh.seek(-1, 1)

    return condition_name, event_name, post_condition_name

def get_step(fh, Delimiters, ElementName):
    pos = fh.tell()
    skip_whitespace_in_line(fh)
    end_marker = generator.snap_line(fh)
    if end_marker is None:
        print "Error: missing dashed line."
        sys.exit()
        return None

    elif end_marker != Delimiters[0]: 
        fh.seek(pos)
        return None
    
    skip_whitespace_in_line(fh)
    negated_f = False
    name      = snap_identifier(fh, ElementName)
    if name is None: return None

    if ElementName != "event" and name == "not":
        negated_f = True
        skip_whitespace_in_line(fh)
        name = snap_identifier(fh, ElementName)
        if name is None:
            print "Error: missing %s after 'not'" % ElementName
            return None

    skip_whitespace_in_line(fh)
    if not check(fh, Delimiters[1]):
        print "Error: %s has not been closed by '%s'" % (ElementName, Delimiters[1])
        return None

    if negated_f: return condition_negate(name)
    else:         return name

def snap_state_name(fh):
    """Snaps the name of a state, that is either and identifier or the 
    single quote. The single quote stands for 'previous state name at 
    that position'.
    """
    skip_whitespace_in_line(fh)
    if   check(fh, "'"): return "'"
    elif check(fh, "."): return "."

    return snap_identifier(fh, "state")

def parse_specifications(fh, SectionName):
    """List of:

        IDENTIFIER '{' anything  matching closing '}'
    """

    result = {}
    while 1 + 1 == 2:
        pos = fh.tell()
        
        skip_whitespace(fh)

        marker_f = check(fh, "@")

        skip_whitespace(fh)
        identifier = snap_identifier(fh, "%s identifier" % SectionName)
        # if identifier not in ReferenceDb:
        #    print "Error: identifier '%s' does not belong to '%s'" % SectionName
        if identifier is None:
            fh.seek(pos)
            break

        if marker_f: identifier = "@%s" % identifier

        skip_whitespace(fh)
        if check(fh, "*"):
            content = None # JOKER
        elif check(fh, "{"): 
            line_n  = _get_current_line_n(fh)
            code    = snap_until_matching_bracket(fh, "{", "}")
            content = UserCode(fh.name, line_n, code)
        else:
            print "Error: missing opening '{'"
            return None

        result[identifier] = content

    return result


def snap_until_matching_bracket(fh, Opener, Closer):
    open_n = 1
    txt    = ""
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if not tmp:
            print "Error: missing closing '%s'" % Closer
            return 
        elif tmp == Opener:
            open_n += 1
        elif tmp == Closer: 
            open_n -= 1
            if open_n == 0: return txt
        txt += tmp
                

    
