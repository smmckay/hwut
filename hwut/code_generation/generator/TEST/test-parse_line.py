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
from   hwut.code_generation.generator.parser.generator import parse_line


if "--hwut-info" in sys.argv:
    print "Parser: Parse Generator Line;"
    sys.exit(0)

def test(Txt):
    print "Input: {%s}" % Txt
    fh = StringIO(Txt)
    parameter_db = [
        ObjectSpec("int",         "x"),
        ObjectSpec("float",       "y"),
        ObjectSpec("const char*", "z"),
    ]
    for p in parameter_db:
        p.global_value_type = None

    result = parse_line(fh, parameter_db)
    try:  
        pass
        #result = func(fh)
    except:
        print "<error>"
        return

    print "->"
    print "Parameters:  %s" % "".join("%s; " % str(x) for x in result[0])
    print "Constraints: %s" % "".join("%s; " % str(x) for x in result[1])
    print "__________________________________________________________________"

# Varry number of parameters
test("1;")
test("1;2;")
test("1; 2;")
test("1; 2; 3;")

# Varry type of parameters
test("0o7;")                           # Constants  integer
test("1.0;")                           #            float
test("\"x\";")                         #            string
test("{0x00, 0x42, 0x50, 0xFF};")      #            array
test("[1,2,3];")                       # Selection
test("|1:2|;")                         # Range      step = default
test("|1:2| step 0.5;")                     #            step specific
test("|x-2:x+2| in |2:65536| step 1;") # Focus Range
test("|x-2:x+2| in |0x00:0xFF|;")

