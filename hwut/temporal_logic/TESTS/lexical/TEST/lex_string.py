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

import hwut.temporal_logic.parser.lexical_analysis as lex


if "--hwut-info" in sys.argv:
    print "Lexical Analysis: string"
    sys.exit()


def test(source_code):
    sh = StringIO(source_code)
    print "code:   |%s|" % source_code
    result = lex.string(sh)
    if result is not None: print "result: " + repr(result.content).replace("'", "|")
    else:              print "result: None"


test(' "hello world"')
test('"_aber\\" hallo"')
test('  "_aber" hallo')
test('  "aber\\"\\\\" hallo')

