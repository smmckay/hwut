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
from hwut.code_generation.generator.parameter import E_ValueType

def implement(txt, PrototypeParameterList):
    L = max(max([len(p.name) for p in PrototypeParameterList]), len("key"))

    print_txt              = iterator(PrototypeParameterList, L)
    print_table_header_txt = table_header(PrototypeParameterList)
    print_table_line_txt   = table_line(PrototypeParameterList, L)

    txt = txt.replace("$$PRINT$$",              "".join(print_txt))
    txt = txt.replace("$$PRINT_TABLE_HEADER$$", "".join(print_table_header_txt))
    txt = txt.replace("$$PRINT_TABLE_LINE$$",   "".join(print_table_line_txt))

    return txt

def printey(P, L, Suffix):
    if Suffix is None: Suffix = "Separator"
    else:              Suffix = "\"%s\"" % Suffix
    if   P.value_type == E_ValueType.IARRAY:
        return 'hwut_IARRAY_print(it->%s, %s)' % (P.name, Suffix)
    elif P.value_type == E_ValueType.FARRAY:
        return 'hwut_FARRAY_print(it->%s, %s)' % (P.name, Suffix) 
    elif P.value_type == E_ValueType.STRING:
        return 'fprintf(fh, "\\"%s\\"%%s", (%s)it->%s, %s)' % \
               (P.format_string(), P.format_string_cast(), P.name, Suffix)
    else:
        return 'fprintf(fh, "%s%%s", (%s)it->%s, %s)' % \
               (P.format_string(), P.format_string_cast(), P.name, Suffix)

def iterator(ParameterList, L):
    txt = [
        '    fprintf(fh, "    key:%s %%li;\\n", (long)$$G$$_key_get(it));\n' % (" " * (L - 3))
    ]
    txt.extend('    fprintf(fh, "    %s:%s "); %s;\n' \
               % (p.name, " " * (L-len(p.name)), printey(p, L, "\\n")) 
               for p in ParameterList)

    return txt

def table_header(ParameterList):
    itxt = [ '# key%s ' ]
    itxt.extend( 
        '%s%%s ' % p.name
        for p in ParameterList
    )
    seperator_txt = "".join([", Separator" * (len(ParameterList) + 1)])
    return '    fprintf(fh, "%s\\n"%s);' % ("".join(itxt), seperator_txt)

def table_line(ParameterList, L):
    txt = [
        '    fprintf(fh, "%li%s", (long)$$G$$_key_get(it), Separator);\n'
        '    it->hwut.section->implement(it);\n'
    ]
    txt.extend(
        '    %s;\n' % printey(p, L, None)
        for p in ParameterList
    )
    txt.append(
        '    fprintf(fh, "\\n");'
    )
    return txt


