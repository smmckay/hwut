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

from   hwut.code_generation.function_stubs.c.core       import ObjectSpec
import hwut.code_generation.generator.language.c.header as header
import hwut.code_generation.generator.language.c.source as source
from   hwut.code_generation.generator.generator         import Generator
from   hwut.code_generation.generator.parameter         import *

from   collections import defaultdict

if "--hwut-info" in sys.argv:
    print "Generator: C source code basic tests;"
    print "CHOICES: header, source;" 
    print "HAPPY: Lines: +[0-9]+;" 
    print "HAPPY: [0-9]+;" 
    sys.exit()

def check_open_dollars(result):
    print "    Open $-s: %i (must be ZERO!)" % result.count("$")
    if result.count("$") == 0:
        return
    for line_n, line in enumerate(result.splitlines(), start=1):
        if line.find("$") != -1:
            print "    [%3i] %s" % (line_n, line)
    sys.exit()

class something:
    def __init__(self):
        self.element_n_max_db = defaultdict(int)
    def implement(self): return ""

array_db = something()

if "header" in sys.argv:
    print "(1a) Impossible: len(GeneratorName) == 0"
    print "     header_do() -->", header.do("", [1,2,3], array_db)
    print 
    print "(1b) Impossible: len(ParameterList) == 0"
    print "     header_do() -->", header.do("X", [], array_db)
    print 
    print "(2)  Normal Case 1:"
    print 
    print "___________________________________________________________________"
    generator_name = "x"
    p0  = ParameterConstant(E_ValueType.INTEGER, 7777) 
    p0.specify(0, "x", "int")
    p1  = ParameterConstant(E_ValueType.FLOAT, 7778) 
    p1.specify(0, "y", "float")
    parameter_list = [ p0, p1 ]
    generator = Generator(parameter_list, [], None)
    result    = header.do(generator_name, [generator], array_db)
    print "    Lines:    %i" % result.count("\n")
    check_open_dollars(result)
    print result
    print "___________________________________________________________________"
    print result
    print "___________________________________________________________________"
    print "(3)  Normal Case 2:"
    print 
    print "___________________________________________________________________"
    generator_name = "fritz_the_fisher"

    p  = ParameterConstant(E_ValueType.INTEGER, 7777) 
    p.specify(0, "str", "const char*")

    generator = Generator([p], [], None)

    result = header.do(generator_name, [generator], array_db)
    print "    Lines:    %i" % result.count("\n")
    check_open_dollars(result)
    print result
    print "___________________________________________________________________"
    
else:    
    print "(1a) Impossible: len(GeneratorName) == 0"
    print "     source_do() -->", source.do("", [], array_db, "fs")
    print 
    print "(1b) Impossible: len(ParameterList) == 0"
    class something:
        pass
    g = something()
    g.parameter_list = []
    print "     source_do() -->", source.do("X", [g], array_db, "fs")
    print 
    print "(2)  Normal Case 1: (no constraints)"
    print 
    first  = ParameterConstant(E_ValueType.INTEGER, 7777) 
    first.specify(0, "x", "int")
    second = ParameterSelection(E_ValueType.INTEGER, [0.815, 3.14, 47.11]) 
    second.specify(1, "y", "float")
    third  = ParameterRange(E_ValueType.FLOAT, Range(1000, 2000), Step=200) 
    third.specify(2, "rizzo", "double")
    forth  = ParameterRange(E_ValueType.FLOAT, 
                            Range(TrivialExpression("rizzo", "-", 2),
                                  TrivialExpression("rizzo", "+", 2)), 
                            Step=0.5) 
    forth.specify(3, "gorgo", "double")

    parameter_list = [ first, second, third, forth ]
    generator_name = "ZZZ"
    generator = Generator(parameter_list, [], None)
    result    = source.do(generator_name, [generator], array_db, "fs")
    print "    Lines:    %i" % result.count("\n")
    check_open_dollars(result)
    print "    Generator references at line begin:"
    for line_n, line in enumerate(result.splitlines(), start=1):
        line = line.strip()
        if line.find("ZZZ") != 0: continue
        print "        hwut_generator-%s.c:%03i: %s" % (generator_name, line_n, line)

