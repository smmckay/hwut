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
from StringIO import StringIO

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.code_generation.sm_walker.parser.sm_walker as parser


if "--hwut-info" in sys.argv:
    print "Parser: Parse Complete Sm-Walker;"
    print "CHOICES: plain, refer-backward, refer-forward, wild;"
    sys.exit(0)

def test(Txt):
    Txt += "\n" + "-" * 80
    print "Input: {%s}" % Txt
    fh = StringIO(Txt)

    info_db = {
        "name":           "test_sm_walker", 
        "user_data_type": "uint128_t", 
        "max_path_length": 256,
        "max_loop_n":      1,
    }
    result = parser.do(fh, info_db)
    try:  
        pass
        #result = func(fh)
    except:
        print "<error>"
        return

    print "->", result
    print "__________________________________________________________________"

if "plain" in sys.argv:
    test("""
        first ----( ONE )----- second
        third ----( TWO )----- forth
    """)

elif "refer-forward" in sys.argv:
    test("""
          .-------( ONE )-------.
        third ----( TWO )----- forth
    """)
    test("""
          .-----| X |--( ONE )-------.
          .-----| Y |--( TWO )-------.
        third --| Z |--( THREE )----- forth
    """)

elif "refer-backward" in sys.argv:
    test("""
        third ----( TWO )----- forth
          '-------( ONE )-------'
    """)
    test("""
        third --| Z |--( THREE )----- forth
          '-----| X |--( ONE )-------'
          '-----| Y |--( TWO )----'
    """)

elif "wild" in sys.argv:
    test("""
          .-------( ONE )---- she
          .-------( TWO )------'
         he ------( THREE )----'
    """)
    test("""
          he------( ONE )------.
           '------( TWO )------.
           '------( THREE )----she
    """)
    test("""
          he -|X|-(TWO)- she
    """)
    test("""
          he-( ONE )-.
           '-( TWO )- she
    """)
    test("""
          he-( ONE )-| posto |-.
           '-( TWO )-| posta |- she
    """)
