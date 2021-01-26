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
from   hwut.common                              import HWUT_PATH
import hwut.auxiliary.file_system               as fs
from   hwut.code_generation.generator.parameter import E_ValueType
from   hwut.code_generation.generator.generator import get_max_array_length_db

from operator import attrgetter

def do(GeneratorName, SectionList, ArrayDb):
    if   len(GeneratorName) == 0: return None
    elif len(SectionList) == 0:   return None

    max_index_number = max([
        len(section.cursor_dimension_array)
        for section in SectionList
    ])

    parameter_list = SectionList[0].parameter_list    
    if len(parameter_list) == 0: return ""

    array_txt  = array_type_definitions(GeneratorName, parameter_list, 
                                        ArrayDb.element_n_max_db)
    member_str = get_member_string(parameter_list, 
                                   ArrayDb.element_n_max_db)
    length     = len(GeneratorName)
    space0     = max(5 - length, 0)
    space1     = max(length -5, 0)

    template_file_name = HWUT_PATH + "/hwut/code_generation/generator/language/c/templates/source.hg"

    txt = fs.read_or_die(template_file_name)
    txt = txt.replace("$$ARRAY_DEF$$", array_txt)
    txt = txt.replace("$$MEMBERS$$",   member_str)
    txt = txt.replace("$$MAX_INDEX_NUMBER$$", "%i" % max_index_number)
    txt = txt.replace("$Z$",           " " * space0)
    txt = txt.replace("$S$",           " " * space1)
    txt = txt.replace("$$G$$",         GeneratorName)

    return txt

def get_member_string(ParameterList, MaxArrayLengthDb):
    L = max([len(p.member_type) for p in ParameterList])

    def get(P):
        return "%s %s$S$%s;" % (P.member_type, " " * (L - len(P.member_type)), P.name)

    return "".join("    %s\n" % get(p) for p in ParameterList)

def array_type_definitions(GeneratorName, ParameterList, MaxArrayLengthDb):
    txt = []
    for p in ParameterList:
        if not p.is_array(): continue
        txt.extend([
            "typedef struct {\n"
            "    long %slength;\n" % (" " * (len(p.element_type) - 4)),
            "    %s data[%i];\n" % (p.element_type, MaxArrayLengthDb[p.name]),
            "} %s;\n" % p.concrete_type
        ])

    return "".join(txt)
        
