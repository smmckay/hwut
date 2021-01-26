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

from   hwut.code_generation.sm_walker.parser.sm_walker import parse_specifications
import hwut.code_generation.generator.parser.generator as     generator

from   operator import itemgetter


if "--hwut-info" in sys.argv:
    print "Parser:  Parse Sm-Walker Event/Condition Specification;"
    print "CHOICES: dash-line, content;"
    sys.exit(0)

def test_dl(Txt):
    print "{%s}" % Txt
    fh = StringIO(Txt)

    result = generator.parse_dash_line_special(fh)
    try:  
        pass
        #result = func(fh)
    except:
        print "<error>"
        return

    print "->", result
    print "__________________________________________________________________"

def test_content(Txt):
    print "{%s}" % Txt
    fh = StringIO(Txt)
    fh.name = "string"

    result = parse_specifications(fh, "EVENTS")
    try:  
        pass
        #result = func(fh)
    except:
        print "<error>"
        return

    print "->"
    for identifier, code in sorted(result.iteritems(), key=itemgetter(0)):
        print "%s: {" % identifier
        print "      file_name: %s;" % code.file_name
        print "      line_n:    %s;" % code.line_n
        print "      code: {"
        print "          " + code.text
        print "      }"
        print "}"
    print "__________________________________________________________________"


if "dash-line" in sys.argv:
    test_dl(" --// EVENTS //-- ")
    test_dl("--// EVENTS //-- ")
    test_dl("--// EVENTS //--")
    test_dl("--//EVENTS//--")

    test_dl(" --// CONDITIONS //-- ")
    test_dl("--// CONDITIONS //-- ")
    test_dl("--// CONDITIONS //--")
    test_dl("--//CONDITIONS//--")

    test_dl(" --// X //-- ")
    test_dl("--// X //-- ")
    test_dl("--// X //--")
    test_dl("--//X//--")

elif "content" in sys.argv:
    test_content(" name  { some0 { } }")
    test_content(" name1 { some1 { } }\n"
                 " name2 { some2 { { {  { { {} }}} }} }")
    test_content(" name1 {}\n"
                 " name2 { some2 {} }\n"
                 " name3 { some3 { } }")
    test_content(" @begin { 0 }\n"
                 " @end   { 1 }")
