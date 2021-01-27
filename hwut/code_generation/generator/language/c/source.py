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
import pathlib

import hwut.auxiliary.file_system                         as fs
from   hwut.common                                        import HWUT_VERSION
from   hwut.code_generation.generator.parameter           import E_ValueType
import hwut.code_generation.generator.language.c.section  as     section
import hwut.code_generation.generator.language.c.printer  as     printer

from operator import attrgetter

def do(GeneratorName, SectionList, ArrayDb, FileStem):

    if   len(GeneratorName) == 0: return None
    elif len(SectionList) == 0: return None

    PrototypeParameterList = SectionList[0].parameter_list
    if len(PrototypeParameterList) == 0: return None

    template_file_path = pathlib.Path(__file__).parent.joinpath('templates', 'source.cg').__fspath__()
    txt = fs.read_or_die(template_file_path)

    txt = txt.replace("$$HWUT_VERSION$$", "%s" % HWUT_VERSION)
    txt = txt.replace("$$FILESTEM$$", FileStem)
    txt = txt.replace("$$THE_ARRAYS$$", ArrayDb.implement())
    txt = txt.replace("$$KEY_MAX$$", "%i" % get_key_max(SectionList))
    txt = section.implement(txt, GeneratorName, SectionList, PrototypeParameterList, ArrayDb)
    txt = printer.implement(txt, PrototypeParameterList)
    txt = spaces_implement(txt, GeneratorName)
    txt = txt.replace("$$G$$", GeneratorName)

    return txt

def get_key_max(SectionList):
    """RETURNS: The maximum key value for the iterator.
    """
    return sum(section.setting_number() for section in SectionList) - 1

def straighten_open_line_pragmas(txt):
    # Replace the open line pragmas
    def straighten(line, LineN):
        if line == '#line "<original>" 0':
            return '#line "hwut_generator-%s.c" %i' % (GeneratorName, LineN)
        return "%s\n" % line

    return "".join([
        straighten(line, line_n)
        for line_n, line in enumerate(txt.splitlines(), start=1)
    ])

def get_cursor_txt():
    cursor_file_path = pathlib.Path(__file__).parent.joinpath('templates', 'cursor.cg').__fspath__()
    content = fs.read_or_die(cursor_file_path)
    return "".join([
        '#line "%s" 0\n' % cursor_file_path,
        content,
        '#line "<original>" 0\n',
    ])

def source_index_offset_list(SectionList):
    offset_list = []
    offset      = 0
    for g in SectionList:
        offset += g.setting_number()
        offset_list.append(offset)

    return "".join("%s, " % offset in offset_list)

def spaces_implement(txt, GeneratorName):
    length = len(GeneratorName)
    space0 = max(5 - length, 0)
    space1 = max(length - 5, 0)

    txt = txt.replace("$Z$", " " * space0)
    txt = txt.replace("$S$", " " * space1)
    txt = txt.replace("$L$", " " * length)

    return txt

