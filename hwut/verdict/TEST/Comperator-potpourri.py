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

sys.path.insert(0, os.environ["HWUT_PATH"])

from hwut.verdict.comparison import Comperator

from StringIO import StringIO

if "--hwut-info" in sys.argv:
    print "Comperator: Potpourri;"
    print "CHOICES: one, two, three;"
    sys.exit()

def show(Name, X):
    first_f = True
    for line in X:
        if first_f: print "    %s:       [%s]" % (Name, line.replace("\n", "\\n"))
        else:       print "             [%s]" % line.replace("\n", "\\n")
        first_f = False

i = -1
def test(A, B):
    global i
    i += 1
    Comperator.init()
    print "Test: %i" % i
    show("A", A)
    show("B", B)
    print "    verdict: %s"   % Comperator.potpourri(A, B)
    print "<end>"
    return 

# Assume that there are no empty line. Empty lines are supposed to be
# filtered before the call to this function.
if "one" in sys.argv:
    test(["a"],   ["a"])
    test(["a"],   ["a "])
    test([" a"],   ["a"])
    test([" a"],   ["a "])
    test(["a a"],   ["a \ta"])
    test(["a"],   ["a\n"])
    test(["a\n"], ["a"])
    test(["a\n"], ["a\n"])
    test(["a"],   ["b"])
    test(["a"],   ["b\n"])
    test(["a\n"], ["b"])
    test(["a\n"], ["b\n"])

elif "two" in sys.argv:
    test(["a"],   ["a", "a"])
    test(["a"],   ["a", "b"])
    test(["a"],   ["a", "b"])
    test(["a", "a"],   ["a"])
    test(["a", "a"],   ["a"])
    test(["a", "b"],   ["a"])
    test(["a", "a"],   ["a", "a"])
    test(["a", "a"],   ["a", "b"])
    test(["a", "b"],   ["a", "b"])

elif "three" in sys.argv:
    test(["a"],   ["a", "a"])
    test(["a"],   ["a", "b"])
    test(["a"],   ["a", "b"])
    test(["a", "a", "a"],   ["a"])
    test(["a", "a", "a"],   ["a"])
    test(["a", "b", "a"],   ["a"])
    test(["a", "a", "a"],   ["a", "a", "a"])
    test(["a", "a", "a"],   ["a", "b", "a"])
    test(["a", "b", "a"],   ["a", "b", "a"])

else:
    pass #test(["a"],   ["a"])
