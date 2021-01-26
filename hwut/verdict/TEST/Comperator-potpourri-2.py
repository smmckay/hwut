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

from hwut.verdict.comparison import Comperator, StreamResult

from StringIO import StringIO

if "--hwut-info" in sys.argv:
    print "Comperator: Potpourri 2 (line blocks);"
    sys.exit()

def show(Name, X):
    first_f = True
    for line in X:
        if first_f: print "    %s:       [%s]" % (Name, line.replace("\n", "\\n"))
        else:       print "             [%s]" % line.replace("\n", "\\n")
        first_f = False

i = -1
def test(A, B):
    sa = StreamResult(StringIO(A), True, True, None)
    sb = StreamResult(StringIO(B), True, True, None)
    global i
    i += 1
    Comperator.init()
    print "Test: %i" % i
    chunk_a = sa.get_next()
    chunk_b = sb.get_next()
    show("A", chunk_a)
    show("B", chunk_b)
    print "    verdict: %s" % Comperator.potpourri(chunk_a, chunk_b)
    print "<end>"
    return 

test("""
||||
Walter von der Vogelweide.
---- 
Samson von der Sesamstrasse.
Oscar aus der Muelltonne.
----
||||
""", 
"""
||||
---- 
Samson von der Sesamstrasse.
Oscar aus der Muelltonne.
----
Walter von der Vogelweide.
||||
""")

test("""
||||
Walter von der Vogelweide.
---- 
Oscar aus der Muelltonne.
Samson von der Sesamstrasse.
----
||||
""", 
"""
||||
---- 
Samson von der Sesamstrasse.
Oscar aus der Muelltonne.
----
Walter von der Vogelweide.
||||
""")
test("""
||||
---- 
Oscar
Samson
---- 
---- 
Oscar
Samson
----
||||
""", 
"""
||||
---- 
Samson
Oscar
----
----
Samson
Oscar
----
||||
""")
test("""
||||
---- 
Oscar
Samson
---- 
---- 
Oscar
Samson
----
||||
""", 
"""
||||
---- 
Oscar
Samson
----
----
Oscar
Samson
----
||||
""")
