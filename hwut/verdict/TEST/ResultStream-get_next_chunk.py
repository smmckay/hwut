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

from hwut.verdict.comparison import StreamResult

from StringIO import StringIO

if "--hwut-info" in sys.argv:
    print "StreamResult: get_next_chunk;"
    print "CHOICES: lines, chunks, mixed;"
    sys.exit()

i = -1
def test(Text):
    global i
    i += 1

    fh = StringIO(Text)
    rs = StreamResult(fh, True, True, None)

    print "Test: %i" % i
    while 1 + 1 == 2:
        chunk = rs.get_next()
        if chunk is None:
            break
        elif type(chunk) == list: 
            print "  {"
            for line in chunk:
                print "    [%s]" % line.replace("\n", "\\n")
            print "  }"
        else:
            print "  [%s]" % chunk

    print "<end>"
    return 


if "lines" in sys.argv:
    test("")
    test("Hallo")
    test("Ich\nEisbaer")
    test("##Ich\nEisbaer")
    test("Ich##\nEisbaer")
    test("##Ich##\nEisbaer")
    test("Ich\n##Eisbaer")
    test("Ich\nEisbaer##")
    test("Ich\n##Eisbaer##")

elif "chunks" in sys.argv:
    test("||||")
    test("||||")
    test("||||\n||||") 
    test("||||\n"
         "Hallo\n"
         "||||")
    test("||||\n"
         "##Hallo\n"
         "||||")
    test("||||\n"
         "##Hallo##\n"
         "||||")
    test("||||\n"
         "Hallo##\n"
         "||||")
    test("||||\n"
         "Hallo##\n"
         "Bonjour\n"
         "||||")
    test("||||\n"
         "Bonjour\n"
         "Hallo##\n"
         "||||")

else:
    test("Bonjour\n"
         "||||\n"
         "Hallo\n"
         "||||")
    test("Bonjour\n"
         "||||\n"
         "Hallo\n"
         "||||\n"
         "Good Morning")
    test("||||\n"
         "Hallo\n"
         "||||\n"
         "Good Morning")
    test("Bonjour\n"
         "||||\n"
         "||||")
    test("Bonjour\n"
         "||||\n"
         "||||\n"
         "Good Morning")
    test("||||\n"
         "||||\n"
         "Good Morning")



