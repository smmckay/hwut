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

def check(HappyRegexList, Output, Good):
    """Happy pattern check finds out if the lines Output and Good 
    might still be the same because the match happy patterns in the
    same fashion. 

    EXAMPLE: 

      Happy patterns: Simple.cpp:[0-9]:
                      "[a-z]"

      Then, the two lines:

         (1) [Simple.cpp:921: Error unknown expression (hugo)]
         (2) [Simple.cpp:1021: Error unknown expression (otto)]

      Are considered equal, because the first happy pattern allows
      any number following the file name in between two ':'. The 
      second happy pattern allows any name in quotes. Both happy
      patterns appear in the same position in the line.

    ASSUME: Both lines are 'whitespace shrinked'.

    RETURNS: Output and Good match one or more of the happy patterns
             consistently.
    """
    def cut(text, Begin, End):
        first  = text[:Begin]
        second = text[End:]
        result = first + second
        return result

    output = Output
    good   = Good
    for happy in HappyRegexList:
        x = happy.search(output)
        if x is None: continue
        y = happy.search(good)
        if y is None: continue
        if x.start() != y.start(): return False
        output = cut(output, x.start(), x.end())
        good   = cut(good,   y.start(), y.end())

        if output == good: return True

    return output == good

