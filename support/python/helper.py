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
import sys

def info(Title, ChoiceList=None):
    if len(sys.argv) < 2 or sys.argv[1] != "--hwut-info": return

    print Title
    if ChoiceList != None:
        txt = [ "CHOICES: " ]
        for choice in ChoiceList:
            txt.append("%s" % choice)
            txt.append(",")
        print "".join(txt[:-1]) + ";" 
    sys.exit(0)

def choice(ChoiceName):
    if len(sys.argv) >= 2 and sys.argv[1] == ChoiceName: return True
    return False

def table(TableName, List, *Names):
    NameN = len(Names)
    # Determine Max Lengths
    L = map(lambda x: len(x) + 1, Names)
    for element in List:
        for i, name in enumerate(Names):
            value = element.__dict__[name]
            if type(value) not in [str, unicode]: value = repr(value)
            if L[i] < len(value): L[i] = len(value)

    def space(ColumnN, Text):
        return " " * (L[ColumnN] - len(Text))
    
    if TableName != "": txt = ["%s:" % TableName + "\n"]
    else:               txt = []

    for i, name in enumerate(Names):
        txt.append(name + ":" + space(i, name + ":") + " ")
    txt.append("\n")

    for element in List:
        for i, name in enumerate(Names):
            value = element.__dict__[name]
            if type(value) not in [str, unicode]: value = repr(value)
            txt.append(value + space(i, value) + " ")
        txt.append("\n")
    return "".join(txt)
