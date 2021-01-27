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

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.verdict.happy_pattern as happy_pattern
from   StringIO import StringIO
import re

if "--hwut-info" in sys.argv:
    print "Comperator: Happy Patterns;"
    print "CHOICES: one, two;"
    sys.exit()

i = -1
def test(A, B, HPL):
    global i
    i += 1
    hpl = [ re.compile(pattern_str) for pattern_str in HPL ]

    print "Test: %i" % i
    print "    A:       [%s]" % A.replace("\n", "\\n")
    print "    B:       [%s]" % B.replace("\n", "\\n")
    print "    verdict: %s"   % happy_pattern.check(hpl, A, B)
    print "<end>"
    return 

if "one" in sys.argv:
    hpl = [ "file.c:[0-9]+:" ]
    print "RE: %s" % hpl
    test("file.c:12:",             "file.c:43:",             hpl)
    test("The file.c:12:",         "The file.c:43:",         hpl)
    test("The file.c:12: is nice", "The file.c:43: is nice", hpl)

    hpl = [ "^file.c:[0-9]+:" ] 
    print "RE: %s (Begin of Line)" % hpl
    test("file.c:12:",             "file.c:43:",             hpl)
    test("The file.c:12:",         "The file.c:43:",         hpl)
    test("The file.c:12: is nice", "The file.c:43: is nice", hpl)

    hpl = [ "file.c:[0-9]+:$" ]
    print "RE: %s (End of Line)" % hpl
    test("file.c:12:",             "file.c:43:",             hpl)
    test("The file.c:12:",         "The file.c:43:",         hpl)
    test("The file.c:12: is nice", "The file.c:43: is nice", hpl)

elif "two":
    hpl = [ "x:[0-9]+:", "([a-z]+)" ]
    print "RE: %s" % hpl
    test("x:12:(murks)", "x:43:(gogo)", hpl)
    test("x:12: (murks)", "x:43:(gogo)", hpl)
    test("(murks)x:12:", "x:43:(gogo)", hpl)

