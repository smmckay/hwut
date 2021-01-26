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

from   hwut.code_generation.function_stubs.c.core      import ObjectSpec
from   hwut.code_generation.generator.parameter        import *
import hwut.code_generation.generator.parser.generator as     generator
  

if "--hwut-info" in sys.argv:
    print "Parser: The parser function."
    sys.exit(0)


def test(Text):
    fh = StringIO(Text)

    generator_list = generator.do(fh)
    print_generator_list(generator_list)

def print_generator_list(generator_list):
    print "GeneratorN: %i" % len(generator_list)
    for i, generator in enumerate(generator_list):
        print "(%i) %s" % (i, str(generator).replace("\n", "\n    "))


test("""
    int x; float y; 
    1;     0.815;
    2;     47.11;
""")

test("""
    int x; const char* str; 
    1;     ["hello", "guten tag"];
    2;     ["bonjour", "hola"];
""")

test("""
    float x; const char* str; 
    1;            ["hello", "guten tag"];
    0x2           ["bonjour", "hola"];
    0x7;          [0x0A, 0x0D];
    0b0101.1010;  "Hm?";
    0b1111.1111;  "Captain?";
""")

