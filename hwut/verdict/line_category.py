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
# DEBUG_fh = open("tmp.log", "wb")

def do(Line, PotpourriF, ShrinkEmptyLinesF):
    """Verdict: 0 -- empty line or comment
                1 -- begin of potpourri
                2 -- end of potpourri
                3 -- normal line
    """
    if not Line: return None, None # end of file
    # DEBUG_fh.write("# [%s] %s" % (Line, ShrinkEmptyLinesF))

    line = Line.strip()
    L    = len(line)

    if not line:
        if ShrinkEmptyLinesF:                  verdict = 0 # empty line
        else:                                  verdict = 3 # normal line
    elif line.find("##") == 0:                 verdict = 0 # comment
    elif L >= 2 and line.rfind("##") == L - 2: verdict = 0 # comment
    elif PotpourriF:   
        if   line.find("||||") == 0:  verdict = 1 # begin/end of potpourri
        elif line.find("----") == 0:  verdict = 2 # begin/end of potpourri line block
        else:                         verdict = 3 # normal line
    else:                             verdict = 3 # normal line

    # Prepare result line in unified format.
    if Line and Line[-1] == '\n': 
        if len(Line) > 2 and Line[-2] == '\r': line = Line[:-2] # Windows/DOS
        else:                                  line = Line[:-1] # Unix, Mac, etc.
    else:                
        line = Line

    return verdict, line

