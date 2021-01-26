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
#! /usr/bin/env python
import os
import sys
from StringIO import StringIO

sys.path.insert(0, os.environ["HWUT_PATH"])

from   hwut.code_generation.sm_walker.parser.sm_walker import parse_line


if "--hwut-info" in sys.argv:
    print "Parser: Parse Sm-Walker Line;"
    print "CHOICES: plain, refer-backward, refer-forward;"
    sys.exit(0)

def test(Txt):
    print "Input: {%s}" % Txt
    fh = StringIO(Txt)

    result = parse_line(fh)
    try:  
        pass
        #result = func(fh)
    except:
        print "<error>"
        return

    print "->", result
    print "__________________________________________________________________"


if "plain" in sys.argv:
    test(" me ---| always |---( happyness )--- you ")
    test("me---|always|---(happyness)---you")
    test("me--|always|--(happyness)--you")
    test(" me ---( happyness )--- you ")
    test("me---(happyness)---you")
    test("me--(happyness)--you")

elif "refer-backward" in sys.argv:
    test("  '---| always |---( happyness )---' ")
    test(" '---|always|---(happyness)---'")
    test("'--|always|--(happyness)--'")
    test("  '---( happyness )---' ")
    test(" '---(happyness)---'")
    test("'--(happyness)--'")

elif "refer-forward" in sys.argv:
    test("  .---| always |---( happyness )---. ")
    test(" .---|always|---(happyness)---.")
    test(".--|always|--(happyness)--.")
    test("  .---( happyness )---. ")
    test(" .---(happyness)---.")
    test(".--(happyness)--.")

