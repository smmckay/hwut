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
import sys
import os
from StringIO import StringIO

sys.path.append(os.environ["HWUT_PATH"])

import hwut.temporal_logic.parser.rules as parser
import hwut.temporal_logic.parser.lilli_peg as lilli_peg

"""
condition-primary: (... see "condition_primary-1.py")  # test without recursions
                   '(' condition ')'    
                   'not' condition     

"""

if "--hwut-info" in sys.argv:
    print "Syntax: Snap Condition Primary: Recursion"
    sys.exit()

def test(source_code):
    lilli_peg.node_cache.clear()
    sh = StringIO(source_code)
    print "code:   '%s'" % source_code
    print "result: \n" + parser.snap_condition_primary(sh).write(2)

test("  ( SHUTDOWN.time > 1000 )")
test("  not x < 1")
test("  ( not x < 4 * (1 + x) )")
