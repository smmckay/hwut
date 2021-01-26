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
from   StringIO import StringIO
from   operator import itemgetter

sys.path.insert(0, os.environ["HWUT_PATH"])

from   hwut.code_generation.function_stubs.c.core      import ObjectSpec
from   hwut.code_generation.generator.parser.generator import parse_line
from   hwut.code_generation.generator.dependency_db    import DependencyDb
from   hwut.code_generation.generator.parameter        import *


if "--hwut-info" in sys.argv:
    print "DependencyDb;"
    print "CHOICES: init, circularity, sequence;"
    sys.exit(0)


def focus(Index, Name, Id0, Id1=None):
    if Id1 is None: Id1 = Id0
    result  = ParameterRange(E_ValueType.FLOAT, 
                             Range(TrivialExpression(Id0, "-", 2),
                                   TrivialExpression(Id1, "+", 2)), 
                             Step=1)
    result.specify(Index, Name, "int")
    return result

def normal(Index, Name):
    result  = ParameterConstant(E_ValueType.FLOAT, 0.815) 
    result.specify(Index, Name, "float")
    return result

def print_db(dependency_db):
    print "____________________________________________________________________"
    for key, dependency_set in sorted(dependency_db.iteritems(), key=itemgetter(0)):
        if not dependency_set: continue
        print "[%s] -> %s" % (key, dependency_set)

def circulator(dependency_db):
    print_db(dependency_db)
    path = dependency_db.get_circularity()
    print 
    if path is None:
        print "    <no circularity>"
    else:
        for i, element in enumerate(path):
            print "    %s%s depends on:" % (" " * i, element)
        print "    %s%s" % (" " * len(path), path[0])
            
def sequencator(dependency_db, parameter_list):
    print_db(dependency_db)
    sequence = dependency_db.get_parameter_sequence(parameter_list)
    print 
    print "->"
    print "".join("    %s;\n" % str(p) for p in sequence)


if "init" in sys.argv:
    dependency_db = DependencyDb([
        focus(0, "u", "v"),
        focus(1, "v", "w"),
        focus(2, "w", "x"),
        focus(3, "x", "y"),
        focus(4, "y", "z"),
        normal(5, "z"),
    ])
    print_db(dependency_db)

    dependency_db = DependencyDb([
        focus(0, "u", "v", "y"),
        focus(1, "v", "w", "x"),
        normal(2, "w"),
        normal(3, "x"),
        normal(4, "y"),
        normal(5, "z"),
    ])
    print_db(dependency_db)

elif "circularity" in sys.argv:
    # No circularity
    dependency_db = DependencyDb([
        focus(0, "u", "v"),
        focus(1, "v", "w"),
        normal(2, "w")
    ])
    circulator(dependency_db)

    # Linear direct loop
    dependency_db = DependencyDb([
        focus(0, "u", "v"),
        focus(1, "v", "u"),
        normal(2, "w")
    ])
    circulator(dependency_db)

    # Linear big loop
    dependency_db = DependencyDb([
        focus(0, "u", "v"),
        focus(1, "v", "w"),
        focus(2, "w", "x"),
        focus(3, "x", "y"),
        focus(4, "y", "z"),
        focus(5, "z", "u"),
    ])
    circulator(dependency_db)

    # Small tree without loop
    dependency_db = DependencyDb([
        focus(0, "a",  "b1", "b2"),
        focus(1, "b1", "c1", "c2"),
        focus(2, "b2", "d1", "d2"),
        focus(3, "b3", "e1", "e2"),
        normal(4, "c1"),
        normal(5, "c2"),
        normal(6, "d1"),
        normal(7, "e2"),
        normal(8, "e1"),
        normal(9, "d2"),
    ])
    circulator(dependency_db)

    # Small tree with loop
    dependency_db = DependencyDb([
        focus(0, "a",  "b1", "b2"),
        focus(1, "b1", "c1", "c2"),
        focus(2, "b2", "d1", "d2"),
        focus(3, "b3", "e2"),
        normal(4, "c1"),
        normal(5, "c2"),
        normal(6, "d1"),
        normal(7, "e2"),
        focus(8,  "d1", "b2"),
        normal(9, "d2"),
    ])
    circulator(dependency_db)

    # Crossing, but not circular
    dependency_db = DependencyDb([
        focus(0, "u", "v"),
        focus(1, "v", "w"),
        normal(2, "w"),
        focus(3, "x", "y"),
        focus(4, "y", "z"),
        focus(5, "z", "w"),
    ])
    circulator(dependency_db)

    # Crossing, and not circular
    dependency_db = DependencyDb([
        focus(0, "u", "v"),
        focus(1, "v", "w"),
        focus(2, "w", "a"),
        focus(3, "x", "y"),
        focus(4, "y", "z"),
        focus(5, "z", "w"),
        focus(5, "a", "u"),
    ])
    circulator(dependency_db)

elif "sequence" in sys.argv:
    parameter_list = [
        focus(0, "u", "v"),
        focus(1, "v", "w"),
        focus(2, "w", "a"),
        focus(3, "x", "y"),
        focus(4, "y", "z"),
        focus(5, "z", "w"),
    ]
    dependency_db = DependencyDb(parameter_list)
    sequencator(dependency_db, parameter_list)

    parameter_list = [
        focus(0, "u", "v", "w"),
        normal(1, "v"),
        normal(2, "w"),
        focus(3, "x", "y", "z"),
        normal(4, "y"),
        normal(5, "z"),
    ]
    dependency_db = DependencyDb(parameter_list)
    sequencator(dependency_db, parameter_list)

    parameter_list = [
        focus(0, "u", "v", "w"),
        normal(1, "v"),
        focus(2, "w", "X"),
        focus(3, "x", "y", "z"),
        normal(4, "y"),
        focus(5, "z", "X"),
        normal(6, "X"),
    ]
    dependency_db = DependencyDb(parameter_list)
    sequencator(dependency_db, parameter_list)
