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
import shutil
import StringIO 

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.io.mini_fly as fly

if "--hwut-info" in sys.argv:
    print "Mini Fly Code Writer;"
    print "CHOICES: write_list, write_list_list, write_string_trivial, write_struct_list;"
    sys.exit(0)

choice = sys.argv[1]

function = {
    "write_string_trivial":  fly.write_string_trivial,
    "write_list":            fly.write_list,
    "write_list_list":       fly.write_list_list,
    "write_struct_list":     fly.write_struct_list,
}[choice]

def pretty(Txt):
    if isinstance(Txt, str):
        return Txt.replace("\t", "\\t").replace("\n", "\\n")
    else:
        return repr(Txt)

def print_result(X, Indent=""):
    if type(X) == list:
        print "["
        for element in X:
            print_result(element, Indent + "    ")
        print "]"
    else:
        print "%s%s" % (Indent, X)

def test(Txt, Arg=None):
    global function 
    global choice 

    if choice == "write_list_list":
        result = function(Txt, len(Txt[0]))
    else:
        result = function(Txt)

    print "IN:     \"%s\"" % pretty(Txt)
    print "RESULT:"
    print_result(result)
    print "----------------------------"

if choice == "write_string_trivial":
    test("")
    test(" ")
    test("\t")
    test("\n")
    test("  ")
    test("\t ")
    test("\n ")
    test("  ")
    test(" \t")
    test(" \n")
    test("+")
    test(" -")
    test("\ta")
    test("\nb")
    test("  c")
    test("\t d")
    test("\n e")
    test("  f")
    test(" \tg")
    test(" \nh")
    test(";")
    test(" ;")
    test("\t;")
    test("\n;")
    test("  ;")
    test("\\;")
    test(" \\;")
    test("\t\\;")
    test("\n\\;")
    test("  \\;")
    test("[")
    test("\\[")
    
elif choice == "write_list":
    test([])
    test([":"])
    test([":", "::"])

elif choice == "write_list_list":
    test([[]                    ])
    test([[],         [],       ])
    test([[":"],      [":"],    ])
    test([[":", ":"], [":", ":"]])

elif choice == "write_struct_list":
    test({                                 })
    test({ "a": []                         })
    test({ "a": [],         "b": [],       })
    test({ "a": ["x"],      "b": ["1"],    })
    test({ "a": ["y", "z"], "b": ["2", "3"]})
