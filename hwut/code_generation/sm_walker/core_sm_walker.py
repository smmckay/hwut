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
from   hwut.code_generation.generator.parser.parameter    import check, \
                                                                 snap_identifier

def parse(fh):

    state_db = {}
    while 1 + 1 == 2:
        if is_end_of_file(fh): break

        from_state, \
        event_name, \
        condition_name, \
        to_state        = read_transition_line(fh)

        state = state_db.get(from_state)
        if state is None:
            state = State(from_state)
            state_db[from_state] = state

        state.transition_list.append(StateTransition(event_name, condition_name, to_state))

    return state_db.values()

 

def read_transition_line(fh)
    """Parses a transition:

    """
    from_state = snap_identifier(fh)
    event_name, condition_name = snap_transition(fh)
    to_state   = snap_identifier(fh)

    return from_state, event_name, condition_name, to_state

    

def snap_line(fh):
    """Snaps at least two '-' signs, but as many as there are.
    """
    pos = fh.tell()
    if not word(fh, "--"):
        return False

    while fh.read(1) == "-":
        tmp = fh.read(1)
        if tmp == "-":              continue
        elif not tmp: fh.seek(pos): return False

    fh.seek(-1, 1)
    return True

def snap_line_to(fh, Delimiter):
    pos = fh.tell()
    if   not snap_line(fh):        return False
    elif not check(fh, Delimiter): fh.seek(pos); return False
    else:                          return True

def snap_line_from(fh, Delimiter):
    pos = fh.tell()
    if   not check(fh, Delimiter): return False
    elif not snap_line(fh):        fh.seek(pos); return False
    else:                          return True

def snap_step(fh, Delimiters):
    if not snap_line_to(fh, Delimiters[0]):
        return None

    event_name = snap_identifier(fh)
    if event_name is None:
        print "Error: missing name after '--%s'" % Delimiters[0]

    if not check(fh, Delimiters[1]):
        print "Error: missing closing '%s'" % Delimiters[1]
        return None

    return event_name


def snap_transition(fh):
    """Parses a line:

            --( EVENT )----< CONDITION >-- 

    """
    event_name     = snap_step(fh, "()")
    condition_name = snap_step(fh, "<>")

    if not snap_line(fh):
        print "Error: missing -- line at end."
        return None, None

    return event_name, condition_name

