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

import hwut.temporal_logic.parser.rules as parser
import hwut.temporal_logic.parser.statements as debug
import hwut.temporal_logic.parser.lilli_peg as lilli_peg

if "--hwut-info" in sys.argv:
    print "Syntax: Snap Function Definition"
    sys.exit()

def test(source_code):
    lilli_peg.node_cache.clear()
    debug._debug = {}
    sh = StringIO(source_code)
    print "____________________________________________________________________"
    print "code:   '%s'" % source_code
    print "result: \n" + parser.snap_rule(sh).prune().write(2)

test("""
        my_function = function(a, b, c): { 
            x = 12;
        };
""")
test("""
        my_function = function(a): { 
            if x == 12: send SOMETHING;
            else: {
               if y == 13:   send ELSE;
               elif y == 14: send THIS;
               else:         send NOTHING;
            }
        };
""")
test("""
        my_function = function(a, b, c): { 
            x = 12;
        };
""")
test("""
        my_function = function(a): { 
            if x == 12:  SOMETHING.count < 24;
            else: {
               if y == 13:   ELSE.time > $time - 20;
               elif y == 14: THIS.time - other_time == 5000;
               else:         NOTHING.count == 0;
            }
        };
""")
