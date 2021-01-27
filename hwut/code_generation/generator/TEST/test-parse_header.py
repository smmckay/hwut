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
from   hwut.code_generation.generator.parser.generator import parse_header


if "--hwut-info" in sys.argv:
    print "Parser:  Parse Generator Header;"
    sys.exit(0)

def test(Txt):
    print "Input: {%s}" % Txt
    fh = StringIO(Txt)
    result = parse_header(fh)
    try:  
        pass
        #result = func(fh)
    except:
        print "<error>"
        return

    print "    -> %s" % "".join("%s; " % str(x) for x in result)

test("int x;")
test("int x; const char const* name;")
test("int x; \\\n        const char const* name;")

