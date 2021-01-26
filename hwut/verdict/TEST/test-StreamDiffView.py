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

from hwut.verdict.stream_diff_view import StreamDiffView

from StringIO  import StringIO
from itertools import izip

if "--hwut-info" in sys.argv:
    print "StreamDiffView;"
    print "CHOICES: line, lines, potpourri, potpourri-2, potpourri-bad;"
    print "NO-POTPOURRI;" # Avoid misunderstandings
    print "NO-SHRINK;"    # Avoid misunderstandings
    sys.exit()

def print_lines(La, Lb):
    assert La is not None
    assert Lb is not None

    if La.find("\n") == -1:
        print "|%-32s|%-32s|" % (La, Lb)
    else:
        for a, b in izip(La.splitlines(), Lb.splitlines()):
            print "|%-32s|%-32s|" % (a, b)
            

def test(A, B):
    StreamDiffView.init()
    stream = StreamDiffView(StringIO(A), StringIO(B), True, True, True, None)

    print " " + ("_" * 32) + " " + ("_" * 32)
    for a, b in stream.iterable():
        assert isinstance(a, (str, unicode)), "-- a: %s --" % a
        assert isinstance(b, (str, unicode))
        print_lines(a, b)

    print "'" + ("-" * 32) + "+" + ("-" * 32) + "'"
        
if "line" in sys.argv:
    test("hello world", "hello world")
    test("hello world", "hillo world")
    test("   hello    world", "hillo world")
    test("((hi))   ((world)) ((hi))", 
         "((hallo)) ((welt)) ((hallo))")

if "lines" in sys.argv:
    test("hello world\n"
         "\n"
         "bonjorno\n", 
         "hello world\n"
         "bonjorno\n")
    test("hello world\n"
         "bonjorno\n", 
         "hello world\n"
         "\n"
         "bonjorno\n")
    test("((hi))   ((world)) ((hi))\n" 
         "   ((X)) ((world)) ((hi))", 
         "((hallo)) ((welt)) ((hallo))\n"
         "((haha)) ((welt)) ((hallo))")

elif "potpourri-bad" in sys.argv:
    test("", 
         "||||\n" "  otto\n" "||||\n")
    test("||||",
         "||||\n" "  otto\n" "||||\n", )
    test("  congo\n" "||||",
         "||||\n" "  otto\n" "||||\n", )

    test("||||\n" "  otto\n" "||||\n", 
         "  congo\n" "||||")
    test("||||\n" "  otto\n" "||||\n", 
         "||||")
    test("||||\n" "  otto\n" "||||\n", 
         "")

elif "potpourri" in sys.argv:
    test("||||\n" "  otto\n" "  fritz\n" "  congo\n" "||||\n", 
         "||||\n" "  congo\n" "  otto\n" "  fritz\n" "||||")
    test("||||\n" "  otto\n" "  fritz\n" "  congo\n" "||||", 
         "||||\n" "  congo\n" "  otto\n" "  FRANZ\n" "||||")
    test("|||| Bongo\n"     "  otto\n"  "  fritz\n" "  congo\n" "|||| Mangifrek", 
         "|||| Mangifrek\n" "  congo\n" "  otto\n"  "  FRANZ\n" "|||| Molongo")
    test("|||| Mangifrek\n" "  otto\n"  "  fritz\n" "  congo\n" "|||| Bongo", 
         "|||| Molongo\n"   "  congo\n" "  otto\n"  "  FRANZ\n" "|||| Mangifrek")
    test("|||| Mangifrek\n" "  otto\n"  "  fritz\n" "  congo\n" "|||| Bongo", 
         "|||| Mangifrek\n" "  congo\n" "  otto\n"  "  FRANZ\n" "|||| Molongo")
    test("|||| Bongo\n"     "  otto\n"  "  fritz\n" "  congo\n" "|||| Mangifrek", 
         "|||| Molongo\n"   "  congo\n" "  FROTZ\n" "  otto\n"  "  FRANZ\n" "|||| Mangifrek")
    test("|||| Bongo\n"     "  otto\n"  "  fritz\n" "  congo\n" "|||| Mangifrek", 
         "|||| Molongo\n"   "  congo\n" "  otto\n"  "  FRANZ\n" "|||| Mangifrek")

elif "potpourri-2" in sys.argv:
    test("|||| Bongo\n"     
         "----\n"
         "  otto\n"  
         "  congo\n" 
         "----\n"
         "|||| Mangifrek", 
         "|||| Molongo\n"   
         "----\n"
         "  otto\n"  
         "  congo\n" 
         "----\n"
         "|||| Mangifrek")
    test("|||| Bongo\n"     
         "----\n"
         "  elisa\n"  
         "  heidlinde\n" 
         "----\n"
         "----\n"
         "  max\n" 
         "  otto\n"  
         "----\n"
         "|||| Mangifrek", 
         "|||| Molongo\n"   
         "----\n"
         "  max\n" 
         "  otto\n"  
         "----\n"
         "----\n"
         "  elisa\n"  
         "  heidlinde\n" 
         "----\n"
         "|||| Mangifrek")
    test("|||| Bongo\n"     
         "----\n"
         "  melisa\n"  
         "  heidlinde\n" 
         "----\n"
         "----\n"
         "  max\n" 
         "  otto\n"  
         "----\n"
         "|||| Mangifrek", 
         "|||| Molongo\n"   
         "----\n"
         "  max\n" 
         "  otto\n"  
         "----\n"
         "----\n"
         "  heidlinde\n" 
         "  melisa\n"  
         "----\n"
         "|||| Mangifrek")


#test("||||\n" "  otto\n" "  fritz\n" "  congo\n" "||||", 
#     "||||\n" "  congo\n" "  otto\n" "  FRANZ\n" "||||")


