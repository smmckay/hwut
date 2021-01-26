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
import sys
import os
import shutil
import StringIO 

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.io.mini_fly as fly

if "--hwut-info" in sys.argv:
    print "Mini Fly Parser;"
    print "CHOICES: skip_whitespace, read_label, read_string_trivial, " \
                   "read_list, read_list_list;"   
    sys.exit(0)

choice = sys.argv[1]

function = {
    "skip_whitespace":     fly.read_list,
    "read_label":          fly.read_label,
    "read_string_trivial": fly.read_string_trivial,
    "read_list":           fly.read_list,
    "read_list_list":      fly.read_list_list,
}[choice]

def pretty(Txt):
    return Txt.replace("\t", "\\t").replace("\n", "\\n")

def test(Txt, Arg=None):
    global function 

    fh = StringIO.StringIO(Txt)
    if Arg is None: result = function(fh)
    else:           result = function(fh, Arg)

    n = fh.tell()
    fh.seek(0)
    lexeme = fh.read(n)
    next_c = fh.read(1)

    print "IN:     \"%s\"" % pretty(Txt)
    print "RESULT: [%s]"   % result
    print "LEXEME: \"%s\"" % pretty(lexeme)
    print "NEXT:   \"%s\"" % pretty(next_c)
    print "----------------------------"

if choice == "skip_whitespace":
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
    
elif choice == "read_label":
    test(":")
    test("a:")
    test("_:")
    test("aber:")
    test("file_name:")
    test("analogy:")
    test("result_list:")
    test("build_time:")
    test("happy_pattern_list:")
    test("interpreter_list:")
    test("make_dependent_f:")
    test("potpourri_f:")
    test("same_f:")
    test("shrink_empty_lines_f:")
    test("shrink_space_f:")
    test("temporal_logic_f:")
    test("temporal_logic_rule_list:")
    test("title:")
    test("title_group:")
    test("vanished_f:")
    test("hwut_info_time:")
    test("stdout_post_proc:")
    test("stderr_post_proc:")

elif choice == "read_string_trivial":
    test(":")
    test(";")
    test("\;;")
    test("a;")
    test("a b;")
    test("a b c;")

elif choice == "read_list":
    test(":")
    test("[]")
    test("[ ]")
    test("[;]")
    test("[;;]")
    test("[;;;]")
    test("[a;]")
    test("[ a; b; ]")
    test("[a;b;c;]")

elif choice == "read_list_list":
    test("[[]]", 0)
    test("[[]", 0)
    test("[[", 0)
    test("[[a;]]", 1)
    test("[[;][;]]", 1)
    test("[[a;][a;]]", 1)
    test("[[a;b;][a;b;]]", 2)
