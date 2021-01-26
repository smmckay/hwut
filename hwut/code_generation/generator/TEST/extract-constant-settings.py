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
from   hwut.code_generation.generator.generator        import Generator
from   hwut.code_generation.generator.parameter        import *
from   hwut.code_generation.generator.parser.generator import extract_plain_constant_generators
  

if "--hwut-info" in sys.argv:
    print "Generator: Extract constant settings"
    sys.exit(0)

i = 0
def test(generator_list):
    global i
    i = 0

    print "________________________________________________________________________"
    print "Before:"
    print_generator_list(generator_list)

    extract_plain_constant_generators(generator_list)

    print "After:"
    print_generator_list(generator_list)

def print_generator_list(generator_list):
    for i, generator in enumerate(generator_list):
        print "(%i) %s" % (i, str(generator).replace("\n", "\n    "))

def get(Description):
    """ C -- ParameterConstant
        S -- ParameterSelection
        R -- ParameterRange
        F -- ParameterFocusRange
    """
    global i 
    rizzo_required_f = False
    result = []
    for t in Description: 
        if t == "C": 
            parameter  = ParameterConstant(E_ValueType.INTEGER, i) 
            parameter.specify(0, "x%i" % i, "int")
        elif t == "S":
            parameter = ParameterSelection(E_ValueType.INTEGER, [-i, 0, i]) 
            parameter.specify(1, "y%i" % i, "float")
        elif t == "R": 
            parameter  = ParameterRange(E_ValueType.FLOAT, 
                                        Range(10*i, 10*i + 10), 
                                        Step=2) 
            parameter.specify(2, "z%i" % i, "double")
        elif t == "F":
            parameter = ParameterRange(E_ValueType.FLOAT, 
                                   Range(TrivialExpression("rizzo", "-", 2 + i),
                                         TrivialExpression("rizzo", "+", 2 + i)), 
                                   Step=0.5) 
            parameter.specify(3, "fr%i" % i, "double")
            rizzo_required_f = True
        else:
            assert False
        result.append(parameter)
        i += 1
    
    if rizzo_required_f:
        dummy_parameter = ParameterConstant(E_ValueType.INTEGER, 0x4711) 
        dummy_parameter.specify(66, "rizzo", "int")
        result.append(dummy_parameter)
    return Generator(result, [], {})

# The 'get' function generates a parameter setting. With the letters 'C', 'S', 
# 'R', and 'F' parameters are created. The 'C' stands for a 'ParameterConstant'
# object. Use this function to create test scenarios.

print "0 Generators ___________________________________________________________"
test([ ])
test([ get([]) ])

print "1 Generator which is constant __________________________________________"
test([ get("C") ])
test([ get("CC") ])
test([ get("CCC") ])

print "1 Generator which is not constant ______________________________________"
print "  (Check that all non-constant parameter types can appear at any position)"
test([ get("S") ])
test([ get("R") ])
test([ get("F") ])
test([ get("SC") ])
test([ get("CS") ])
test([ get("RC") ])
test([ get("CR") ])
test([ get("FC") ])
test([ get("CF") ])
test([ get("CCS") ])
test([ get("CSC") ])
test([ get("SCC") ])
test([ get("CCR") ])
test([ get("CRC") ])
test([ get("RCC") ])
test([ get("CCF") ])
test([ get("CFC") ])
test([ get("FCC") ])

print "2 Generators"
test([ get("CCC"), get("CCC") ])  # constant,     constant
test([ get("CCC"), get("CCR") ])  # constant,     not constant
test([ get("RCC"), get("CCC") ])  # not constant, constant
test([ get("CFC"), get("FCC") ])  # not constant, not constant

print "3 Generators"
test([ get("CCC"), get("CCC"), get("CCC") ])  #     c,     c,     c
test([ get("CCC"), get("CCC"), get("CCR") ])  #     c,     c,     not c
test([ get("CCC"), get("RCC"), get("CCC") ])  #     c, not c,     c
test([ get("CCC"), get("RCC"), get("CFC") ])  #     c, not c,     not c
test([ get("FCC"), get("CCC"), get("CCC") ])  # not c,     c,     c
test([ get("CRC"), get("CCC"), get("CCR") ])  # not c,     c,     not c
test([ get("CCS"), get("RCC"), get("CCC") ])  # not c, not c,     c
test([ get("CFC"), get("RCC"), get("CFC") ])  # not c, not c,     not c

