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
from hwut.code_generation.generator.parameter         import assign, \
                                                             E_ValueType
from hwut.code_generation.generator.generator         import GeneratorContantLines, \
                                                             get_max_array_length_db
from hwut.code_generation.generator.language.c.auxiliary import get_integer_code
from hwut.code_generation.generator.language.c.header import get_member_string

def implement(txt, Name, SectionList, PrototypeParameterList, ArrayDb):

    function_decleration_txt = get_declerations(Name, SectionList)
    array_txt                = get_array_lines(Name, SectionList)
    function_txt             = get_functions(Name, SectionList, ArrayDb)

    txt = txt.replace("$$SECTION_DECLARATIONS$$", function_decleration_txt)
    txt = txt.replace("$$SECTION_ARRAY$$",        array_txt)
    txt = txt.replace("$$SECTION_N$$",            "%i" % len(SectionList))
    txt = txt.replace("$$SECTION_FUNCTIONS$$",    function_txt)

    return txt

def get_declerations(Name, SectionList):
    return "".join(
         "extern void   %s_%s_init(%s_t* it);\n"          % (Name, i, Name)   
       + "extern int    %s_%s_implement(%s_t* it);\n"     % (Name, i, Name)                      
       + "extern int    %s_%s_is_admissible(%s_t* it);\n" % (Name, i, Name)
        for i in xrange(len(SectionList))
    )

def get_array_lines(Name, SectionList):
    txt = []
    key_offset = 0
    for i, g in enumerate(SectionList):
        txt.append(
             "    { %i, "               % key_offset
           + "%s_%s_init, "             % (Name, i)   
           + "%s_%s_implement, "        % (Name, i)                      
           + "%s_%s_is_admissible },\n" % (Name, i)
        )
        key_offset += g.setting_number()

    return "".join(txt)

def get_functions(GeneratorName, SectionList, ArrayDb):
    return "".join(
        get_implementation(GeneratorName, g, i, ArrayDb, g.parameter_name_to_cursor_index_db) 
                           for i, g in enumerate(SectionList)
    )

def get_implementation(GeneratorName, g, Index, ArrayDb, CursorIndexDb):
    if isinstance(g, GeneratorContantLines):
        txt = ConstantLinesBased.do(GeneratorName, g, ArrayDb)
    else:
        txt = CursorBased.do(GeneratorName, g, ArrayDb, CursorIndexDb)
       
    return txt.replace("$$N$$", "%i" % Index)
 
class ConstantLinesBased:
    @staticmethod
    def do(GeneratorName, g, ArrayDb):
        global _section_txt
        L = len(g.setting_list)

        add_txt  = ConstantLinesBased.struct(GeneratorName, g, ArrayDb.element_n_max_db)
        add_txt += ConstantLinesBased.array(GeneratorName, L, g, ArrayDb)

        txt = _section_txt
        txt = txt.replace("$$INDEX_N$$",       "1")
        txt = txt.replace("$$DIMENSIONS$$",    "%i" % L)
        txt = txt.replace("$$IMPLEMENT$$",     ConstantLinesBased.iterator_to_setting(GeneratorName, g))
        txt = txt.replace("$$IS_ADMISSIBLE$$", "")

        return add_txt + txt

    @staticmethod
    def struct(GeneratorName, g, MaxArrayLengthDb):
        # A struct is required to hold the data:
        member_txt     = get_member_string(g.parameter_list, MaxArrayLengthDb)
        return   "typedef struct {\n" \
               + member_txt \
               + "} %s_constant_line_db_entry_t;\n\n" % GeneratorName

    @staticmethod
    def array(GeneratorName, L, g, ArrayDb):
        def get(P):
            if P.is_array():
                txt = "&%s" % ArrayDb.array_name(P.name, P.constant)
                return txt
            elif P.value_type == E_ValueType.STRING:
                return '"%s"' % P.constant
            elif P.value_type == E_ValueType.INTEGER:
                return get_integer_code(P.constant, P.concrete_type)
            return "(%s)%s" % (P.concrete_type, P.constant)
        txt = [
            "static const %s_constant_line_db_entry_t %s_constant_line_db[%i] = {\n" % \
            (GeneratorName, GeneratorName, g.setting_number())
        ]
        txt.extend(
            "    { %s },\n" % "".join("%s, " % get(p) for p in parameter_list)
            for parameter_list in g.setting_list
        )
        txt.append("};\n")
        return "".join(txt)

    @staticmethod
    def iterator_to_setting(GeneratorName, g):
        txt = [
            "    const $$G$$_constant_line_db_entry_t* line_p = &$$G$$_constant_line_db[it->hwut.cursor.index[0]];\n\n"
        ]
        txt.extend(
            "    %s;\n" % assign(p, "line_p->%s" % p.name)
            for p in g.parameter_list
        )
        return "".join(txt)


class CursorBased:
    @staticmethod
    def do(GeneratorName, g, ArrayDb, CursorIndexDb):
        global _section_txt
        txt = _section_txt
        txt = txt.replace("$$INDEX_N$$",       "%i" % len(g.cursor_dimension_array))
        txt = txt.replace("$$DIMENSIONS$$",    "".join("%i, " % dim for dim in g.cursor_dimension_array))
        txt = txt.replace("$$IMPLEMENT$$",     CursorBased.iterator_to_setting(g, ArrayDb, CursorIndexDb))
        txt = txt.replace("$$IS_ADMISSIBLE$$", CursorBased.is_admissible(g))
        return txt

    @staticmethod
    def iterator_to_setting(g, ArrayDb, CursorIndexDb):
        txt = [
            p.get_setting_by_iterator(ArrayDb, CursorIndexDb.get(p.name)) 
            for p in g.parameter_list_by_precedence()
        ]
        return "".join(txt)

    @staticmethod
    def is_admissible(g):
        begin, end = CursorBased.parameter_frame(g.parameter_list)

        txt = begin
        txt.append("    /* General constraints.   */\n")
        txt.extend("    if( !( %s ) ) return 0;\n" % constraint
                   for constraint in g.constraint_list)
        txt.extend(end)

        return "".join(txt)

    @staticmethod
    def parameter_frame(ParameterList):
        def rvalue(p):
            if p.is_array(): return "(*(it->%s))" % p.name
            else:            return "(it->%s)" % p.name 

        L = max([len(p.name) for p in ParameterList])

        begin = [
            "    /* Make setting parameters available under original name. */\n"
        ]
        begin.extend(
            "#   define %s%s %s\n" % (p.name, " " * (L-len(p.name)), rvalue(p))
            for p in ParameterList
        )
        end = [
            "#   undef %s\n" % p.name for p in ParameterList
        ]
        return begin, end

_section_txt = """
void 
$$G$$_$$N$$_init($$G$$_t* it) 
{
    static const hwut_cursor_index_t  Dimensions[$$INDEX_N$$] = { $$DIMENSIONS$$ };

    hwut_cursor_init(&it->hwut.cursor, $$INDEX_N$$, 
                     &it->hwut.__memory_index_array[0], 
                     &Dimensions[0]);
}

int
$$G$$_$$N$$_implement($$G$$_t* it)
{
$$IMPLEMENT$$
    return 1;
}                      

int  
$$G$$_$$N$$_is_admissible($$G$$_t* it)
{
$$IS_ADMISSIBLE$$
    return 1;
}                      
"""

