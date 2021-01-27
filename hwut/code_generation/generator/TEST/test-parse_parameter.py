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
#! /usr/bin/env python
import os
import sys
from StringIO import StringIO

sys.path.insert(0, os.environ["HWUT_PATH"])

from   hwut.code_generation.function_stubs.c.core      import ObjectSpec
from   hwut.code_generation.generator.parameter        import *
from   hwut.code_generation.generator.parser.parameter import *


if "--hwut-info" in sys.argv:
    print "Parser:  Parameter* classes;"
    print "CHOICES: constant, selection, range, focus;"
    sys.exit(0)

def test(Txt, func):
    print "Input: {%s}" % Txt
    fh = StringIO(Txt)
    result = func(fh)
    result.specify(0, "no_name", None)
    try:  
        pass
        #result = func(fh)
    except:
        print "<error>"
        return

    print "    -> %s" % result

if "constant" in sys.argv:
    test("5",                    parse_constant)
    test("0x47",                 parse_constant)
    test("0o777",                parse_constant)
    test("0b01011010",           parse_constant)
    test("0.1",                  parse_constant)
    test('"Otto"',               parse_constant)
    test('{ 0 }',                parse_constant)
    test('{ 0x10, 0x50, 0x42 }', parse_constant)
    test('{ 0.0 }',              parse_constant)
    test('{ 0.1, 0.2, 0.3 }',    parse_constant)

elif "selection" in sys.argv:
    test("[3]",             parse_selection)
    test("[3, 2]",          parse_selection)
    test("[3, 2, 1]",       parse_selection)
    test("[3.1]",           parse_selection)
    test("[3.1, 2.1]",      parse_selection)
    test("[3.1, 2.1, 1.1]", parse_selection)
    test("[3.1, 2,   1]",   parse_selection)
    test("[3,   2.1, 1.1]", parse_selection)

elif "range" in sys.argv:
    test("|5:10|",   parse_range)
    test("|5:10| step 5", parse_range)
    test("|5.1 : 10.1| step 0.5", parse_range)
    test("|0x10: 0x7F| step 0x4", parse_range)

elif "focus" in sys.argv:
    test("|x:x|",                   parse_range)
    test("|x-0x10:x+0x10|",         parse_range)
    test("|x-0x10:x+0x10| step 2|", parse_range)
    test("|x-0x10:x+0x10| in |0x04:65536| step 2", parse_range)
    test("|x-0x10:x+0x10| in |0x04:0xFF|  step 2", parse_range)
