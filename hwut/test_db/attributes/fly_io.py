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
from   hwut.test_db.result          import TestResult
from   hwut.test_db.attributes.core import E_Attr, E_AType
import hwut.io.mini_fly             as     fly
import hwut.common                  as     common

def fly_float_parse(fh):
    value_str = fly.read_string_trivial(fh)
    if value_str == "None": return None
    try:    return float(value_str)
    except: return 0.0

def fly_integer_parse(fh):
    value_str = fly.read_string_trivial(fh)
    if value_str == "None": return None
    try:                    return long(value_str)
    except:                 return 0

def fly_bool_parse(fh):
    value_str = fly.read_string_trivial(fh)
    if   value_str == "False": return False
    elif value_str == "True":  return True
    else:                      return None

def fly_regex_list_write(Value):
    return "%s" % fly.write_list([ x[1] for x in Value ])

def fly_regex_list_parse(fh):
    pattern_str_list = fly.read_list(fh)
    if pattern_str_list is None: return None

    value = [ (common.re_compile(p), p) for p in pattern_str_list ]
    return [ (regex, p) for regex, p in value if regex is not None ]

def fly_result_list_write(Value):
    return "%s" % fly.write_list_list([result.to_string_list() for result in Value], 4)

def fly_result_list_parse(fh):
    list_list = fly.read_list_list(fh, 4)
    if list_list is None: return None

    return [ 
        TestResult.from_string_list(sub_list) for sub_list in list_list
    ]

def fly_float_parse(fh):
    value_str = fly.read_string_trivial(fh)
    if value_str == "None": return None
    try:    return float(value_str)
    except: return 0.0

def fly_integer_parse(fh):
    value_str = fly.read_string_trivial(fh)
    if value_str == "None": return None
    try:                    return long(value_str)
    except:                 return 0

def bool_parse(fh):
    value_str = fly.read_string_trivial(fh)
    if   value_str == "False": return False

parser_db = {
    E_AType.REGEX_LIST:  fly_regex_list_parse,
    E_AType.RESULT_LIST: fly_result_list_parse,
    E_AType.LIST:        fly.read_list,
    E_AType.BOOL:        fly_bool_parse,
    E_AType.FLOAT:       fly_float_parse,
    E_AType.INTEGER:     fly_integer_parse,
    E_AType.STRING:      fly.read_string_trivial
}

writer_db = {
    E_AType.REGEX_LIST:  fly_regex_list_write,
    E_AType.RESULT_LIST: fly_result_list_write,
    E_AType.LIST:        fly.write_list,
    E_AType.BOOL:        fly.write_string_trivial,
    E_AType.FLOAT:       fly.write_string_trivial,
    E_AType.INTEGER:     fly.write_string_trivial,
    E_AType.STRING:      fly.write_string_trivial
}
