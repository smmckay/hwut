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

from hwut.verdict.comparison import Comperator

from StringIO import StringIO

if "--hwut-info" in sys.argv:
    print "Comperator: Lines;"
    print "CHOICES: plain, messy-analogy-spots, analogy-spots, analogy-spots-2;"
    sys.exit()

i = -1
def test(A, B):
    global i
    i += 1
    Comperator.init()
    print "Test: %i" % i
    print "    A:       [%s]" % A.replace("\n", "\\n")
    print "    B:       [%s]" % B.replace("\n", "\\n")
    print "    verdict: %s"   % Comperator.lines(A, B)
    print "<end>"
    return 

EquivalenceSpotOpen  = "(("
EquivalenceSpotClose = "))"
def testli(A, B):
    global i
    global EquivalenceSpotOpen
    global EquivalenceSpotClose
    i += 1

    Comperator.init(EquivalenceSpotOpen, EquivalenceSpotClose)
    print "Test: %i" % i
    for line_n, info in enumerate(zip(A, B)):
        line_a, line_b = info
        print "(%i) A:       [%s]" % (line_n, line_a.replace("\n", "\\n"))
        print "    B:       [%s]" % (line_b.replace("\n", "\\n"))
        print "    verdict: %s"   % (Comperator.lines(line_a, line_b))

    print "analogy_db: (%i)" % len(Comperator.analogy_db)
    for key, value in Comperator.analogy_db.iteritems():
        print "   %-10s => %s" % (key,value)
    print "<end>"
    return 



if "plain" in sys.argv:
    test("",   "")
    test("\n", "\n")
    test("",   "\n")
    test("\n", "")
    test("a",   "a")
    test("a",   "a\n")
    test("a\n", "a")
    test("a\n", "a\n")
    test("a",   "b")
    test("a",   "b\n")
    test("a\n", "b")
    test("a\n", "b\n")

elif "messy-analogy-spots" in sys.argv:
    test("((",    "")
    test("((",    "((")
    test("((",    "))")
    test("((",    "(())")
    test("((",    "((a))")
    test("))",    "")
    test("))",    "((")
    test("))",    "))")
    test("))",    "(())")
    test("))",    "((a))")
    test("(())", "")
    test("(())", "((")
    test("(())", "))")
    test("(())", "(())")
    test("(())", "((a))")
    test("((a))", "")
    test("((a))", "((")
    test("((a))", "))")
    test("((a))", "(())")

    test("1((a))", "11((a))")
    test("))((", "))((")
    test("))((1", "))((2")

elif "analogy-spots" in sys.argv:
    testli(["((otto))", "((otto))"], 
           ["((fritz))", "((fritz))"])
    testli(["((otto))", "((otto))"], 
           ["((fritz))", "((otto))"])
    testli(["((otto))((otto))"], 
           ["((fritz))((fritz))"])
    testli(["((otto))((otto))"], 
           ["((fritz))((otto))"])
    testli(["Einst wandelte ((Heidlinde)) mit Ihrem Ehegatten ((Otto))\n",
            "durch die sonnigen Gaerten von ((Pforzheim)). Da kam ein\n",
            "Drache und frass ((Otto)) und ((Heidlinde)) und die ganze\n",
            "Stadt ((Pforzheim)) schaute zu."], 
           ["Einst wandelte ((Frieda)) mit Ihrem Ehegatten ((Kunibert))\n",
            "durch die sonnigen Gaerten von ((Muenster)). Da kam ein\n",
            "Drache und frass ((Kunibert)) und ((Frieda)) und die ganze\n",
            "Stadt ((Muenster)) schaute zu."]) 
    testli(["Hugo ((otto))",  "((otto))"], 
           ["Otto ((maxi))", "((maxi))"])
    testli(["((otto)) Hugo",  "((otto))"], 
           ["((maxi)) Franz", "((maxi))"])
    testli(["((otto))", "Olli ((otto))"], 
           ["((maxi))", "Hugo ((maxi))"])
    testli(["((otto))", "((otto)) Olli"], 
           ["((maxi))", "((maxi)) Hugo"])

elif "analogy-spots-2" in sys.argv:
    # A second test where the analogy spot boundaries are customized
    EquivalenceSpotOpen  = "~"
    EquivalenceSpotClose = "'"

    testli(["~otto'", "~otto'"], 
           ["~fritz'", "~fritz'"])
    testli(["~otto'", "~otto'"], 
           ["~fritz'", "~otto'"])
    testli(["~otto'~otto'"], 
           ["~fritz'~fritz'"])
    testli(["~otto'~otto'"], 
           ["~fritz'~otto'"])
    testli(["Einst wandelte ~Heidlinde' mit Ihrem Ehegatten ~Otto'\n",
            "durch die sonnigen Gaerten von ~Pforzheim'. Da kam ein\n",
            "Drache und frass ~Otto' und ~Heidlinde' und die ganze\n",
            "Stadt ~Pforzheim' schaute zu."], 
           ["Einst wandelte ~Frieda' mit Ihrem Ehegatten ~Kunibert'\n",
            "durch die sonnigen Gaerten von ~Muenster'. Da kam ein\n",
            "Drache und frass ~Kunibert' und ~Frieda' und die ganze\n",
            "Stadt ~Muenster' schaute zu."]) 

