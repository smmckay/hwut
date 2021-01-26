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

import hwut.test_db.hwut_info_interview as interview
import hwut.auxiliary.path              as aux      

if "--hwut-info" in sys.argv:
    print "Parse --hwut-info response;"
    print "CHOICES: title, choices;"
    print "HAPPY:   [0-9L]+;"
    sys.exit()

def test(Text):
    if Text.find("\n") == -1:
        print "TEST: {%s}" % Text
    else:
        print "TEST: {\n    %s\n}" % Text.strip().replace("\n", "\n    ")

    result = interview.parse_response(aux.strip_dot_slash(sys.argv[0]), Text)
    if result is None: 
        print "    FAILED"
    else:
        result = str(result).strip()
        print "|||| potpourri"
        print "    %s" % result.replace("\n", "\n    ")
        print "|||| potpourri"

if "title" in sys.argv:
    test(";")
    test("A;")
    test(":;")
    test("A:;")
    test("A:B;")
elif "choices" in sys.argv:
    test("A; CHOICES:;")
    test("A; CHOICES: 1;")
    test("A; CHOICES: 1, 2;")
    test("A; CHOICES: 1,2,3;")
    


