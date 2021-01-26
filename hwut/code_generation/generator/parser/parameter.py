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

from   hwut.code_generation.generator.parameter import ParameterConstant, \
                                       ParameterSelection, \
                                       ParameterRange, \
                                       Range, \
                                       TrivialExpression, \
                                       E_ValueType

import hwut.temporal_logic.parser.lexical_analysis as T

from   collections import namedtuple
import sys

def parse_constant(fh):
    """
            4711 | 0.815 | "hallo" | '{' 0x16, 0xFE, ... '}'
    """
    content, value_type = parse_constant_core(fh)
    if content is None: return None
    return ParameterConstant(value_type, content)

def parse_selection(fh):
    """
        '[' Constant [ ',' Constant ]+ ']'
    """
    pos = fh.tell()
    if not check(fh, "["):
        return None

    constant_list = []
    value_type    = None
    while 1 + 1 == 2:
        constant, new_value_type = parse_constant_core(fh)
        if constant is None:
            print "Error: missing constant."
            sys.exit()

        value_type = value_type_fit(value_type, new_value_type)
        if value_type is None:
            print "Error: value misfit", new_value_type, value_type
            sys.exit()

        constant_list.append(constant)

        if not check(fh, ","): break

    if not check(fh, "]"):
        print "Error: missing closing ']'. Found '%s'" % fh.read(10)
        sys.exit()

    return ParameterSelection(value_type, constant_list)

def parse_range(fh): 
    """
        range_core [in range_core] [step number]

    EXAMPLE:

              |x+5:200| in |0:200| step 2

    """
    step_size = 1
    cut_range = None
    primary_range, value_type = parse_range_core(fh)
    if primary_range is None:
        return None
    if check(fh, "in"):
        cut_range, new_value_type = parse_range_core(fh)
        value_type = value_type_fit(value_type, new_value_type)
    if check(fh, "step"):
        step_size, new_value_type = parse_number(fh)
        if step_size <= 0:
            print "Error: step size must be greater zero. Found %s." % step_size
            sys.exit()
        value_type = value_type_fit(value_type, new_value_type)

    return ParameterRange(value_type, primary_range, cut_range, step_size)
     
def parse_range_core(fh): 
    """
        '|' expression ':' expression '|'
    """
    if not check(fh, '|'): 
        return None, None

    value_type = E_ValueType.INTEGER

    minimum_expr, new_value_type = parse_trivial_expression(fh)
    value_type                   = value_type_fit(value_type, new_value_type)
    if value_type is None:
        print "Error: value misfit", new_value_type, value_type
        sys.exit()

    if not check(fh, ":"):
        print "Error: missing ':' in range expression"
        sys.exit()

    maximum_expr, new_value_type = parse_trivial_expression(fh)
    value_type                   = value_type_fit(value_type, new_value_type)
    if value_type is None:
        print "Error: value misfit", new_value_type, value_type
        sys.exit()
    
    if not check(fh, '|'): 
        print "Error: missing closing '|' for range. found '%s'" % fh.read(1)
        sys.exit()

    return Range(minimum_expr, maximum_expr), value_type

    
def parse_trivial_expression(fh):
    """Trivial expression:  number
                            identifier +,-,*,/ number
    """
    first, value_type = parse_number(fh)
    if first is not None:
        return first, value_type
    
    first      = snap_identifier(fh, "identifier")
    value_type = E_ValueType.FLOAT
    if first is None:
        print "Error: missing number or identifier"
        sys.exit()

    elif check(fh, "+"): op = "+"
    elif check(fh, "-"): op = "-"
    elif check(fh, "*"): op = "*"
    elif check(fh, "/"): op = "/"
    else:
        return TrivialExpression(first, None, None), value_type

    second, value_type = parse_number(fh)
    if second is None:
        print "Error: missing second operand"
        sys.exit()

    return TrivialExpression(first, op, second), value_type
    
    
def parse_user_code(fh):
    """
        '{^' code '^}'
    """
    if not check(fh, "{^"):
        return None

    code = snap_until(fh, "^}")
    if code is None:
        print "Error: missing closing '^}'"
        return None
    elif len(code) == 0:
        print "Error: empty string not allowed."

    return code

def parse_number(fh):
    """Delegate the detection of numbers to 'T.'. First, try to get an integer,
    then a floating point number.
    
    RETURNS: [0] The numeric value
             [1] The value type
    """
    pos = fh.tell()
    skip_whitespace_in_line(fh)
    number = T.integer(fh)

    if number.ok():
        return number.content, E_ValueType.INTEGER
    number = T.number(fh)
    if number.ok():
        return number.content, E_ValueType.FLOAT

    fh.seek(pos)
    return None, None
    
def parse_constant_core(fh):
    """
       4711 | 0.815 | "hallo" | '{' 0x16, 0xFE, ... '}'
    """
    pos = fh.tell()
    skip_whitespace_in_line(fh)

    number, value_type = parse_number(fh)
    if number is not None: return number,         value_type
    string  = T.string(fh)
    if string.ok():        return string.content, E_ValueType.STRING
    value_type, array   = parse_array(fh)
    if array is not None:  
        if   value_type == E_ValueType.INTEGER: return array, E_ValueType.IARRAY
        elif value_type == E_ValueType.FLOAT:   return array, E_ValueType.FARRAY

    fh.seek(pos)
    return None, None

def parse_array(fh):
    """
        '{' number [ ',' number ]+ '}'
    """
    pos = fh.tell()
    if not check(fh, "{"):
        return None, None

    array      = []
    value_type = E_ValueType.INTEGER
    while 1 + 1 == 2:
        number, new_value_type = parse_number(fh)
        if number is None:
            print "Error: missing constant."
            sys.exit()
        value_type = value_type_fit(value_type, new_value_type)
        if value_type is None:
            print "Error: value misfit", new_value_type, value_type
            sys.exit()
        array.append(number)

        if not check(fh, ","): break

    if not check(fh, "}"):
        print "Error: missing closing '}'"
        sys.exit()

    # The value_type is actually not important here. The type is later
    # defined by the assigned concrete type of the programming language.
    return value_type, array

    
def value_type_fit(ValueType, NewValueType):
    """Compares a NewValueType with an existing ValueType. 

    -- If the ValueType has never been set, the NewValueType is simply 
       overtaken. 
    -- If the current and the new type are the same, nothing changes. 
    -- If they only interfer in being integer and float, the value type 
       is set to float. 
    -- Else, if they differ, this is an error.

    RETURNS: New value type -- if everything is ok.
             None           -- if error.
    """
    if ValueType is None:
        return NewValueType

    elif (NewValueType == E_ValueType.FLOAT   and ValueType == E_ValueType.INTEGER) \
      or (NewValueType == E_ValueType.INTEGER and ValueType == E_ValueType.FLOAT):
        return E_ValueType.FLOAT

    elif (NewValueType == E_ValueType.FARRAY  and ValueType == E_ValueType.IARRAY):
        return E_ValueType.FARRAY

    elif NewValueType != ValueType:
        return None
    
    return ValueType

def check(fh, Word):
    pos = fh.tell()
    skip_whitespace_in_line(fh)
    result = T.plain_word(fh, Word)
    if result.error(): fh.seek(pos); return False
    else:              return True

def check_newline(fh):
    if   check(fh, "\n"):   return True
    elif check(fh, "\r\n"): return True
    else:                   return False

def snap_until(fh, Word):
    i   = 0
    txt = ""
    L   = len(Word)
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if len(tmp) == 0:  return None

        txt += tmp
        if tmp == Word[i]:
            if i == L-1:   return txt[:-L]
            i += 1
        elif i != 0:
            i = 0 
            fh.seek(-1, i)

def skip_whitespace_in_line(fh):
    """Skips any whitespace, but not the newline."""
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if   tmp.isspace() and tmp != "\n": 
            continue
        elif len(tmp) == 0: 
            break
        else:
            fh.seek(-1, 1)
            break

def snap_identifier(fh, ElementName):
    identifier = T.identifier(fh)
    if identifier.error():
        # print "Error: (line %i) missing identifier for '%s'." % (line_n, ElementName)
        return None
    else:
        return identifier.content

def parse_user_code(fh):
    """
        '{^' code '^}'
    """
    if not check(fh, "{^"):
        return None

    code = snap_until(fh, "^}")
    if code is None:
        print "Error: missing closing '^}'"
        return None
    elif len(code) == 0:
        print "Error: empty string not allowed."

    return code

