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
import sys
import os
from StringIO import StringIO

sys.path.append(os.environ["HWUT_PATH"])

import hwut.temporal_logic.parser.statements as     parser
from   hwut.temporal_logic.classes.world     import World
from   hwut.temporal_logic.engine            import Court

if "--hwut-info" in sys.argv:
    print "Syntax: Snap StatementList"
    sys.exit()

def test(source_code):
    sh = StringIO(source_code)
    print "code:   '%s'" % source_code
    print "result: \n"
    for event in parser.event_iterable(sh, World(Court(), {})):
        print event

test(
"""  
"hello-world.c":23:21.001:  { START; BLOB; SPLISH("3x", correct_n=3); }
21.002:                     END(0.0, 10);
SOMETHING("const", "expression"); 
""")

