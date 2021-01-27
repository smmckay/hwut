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
# PURPOSE:
# 
# Provide a list of external and static functions and write tests files 
# for them.
#
# Author: Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os
from   copy import copy
sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.sos.c.lazy.core as lazy
import hwut.auxiliary.path  as path
import hwut.auxiliary.file_system  as fs
import hwut.io.select       as select

# Let the interactive selection always return '0'
select.input_integer = lambda a,b,Option=0,Offset=1: (0, True)

if "--hwut-info" in sys.argv:
    print "Write Tests;"
    print "CHOICES: Empty, Non-Empty;"
    print "HAPPY:   [0-9]+ +[0-9]+ +[0-9]+;"
    sys.exit()

elif "Empty" in sys.argv:
    extern_function_list = []
    static_function_list = []
elif "Non-Empty" in sys.argv:
    extern_function_list = ["otto", "karl", "emil"]
    static_function_list = ["kunibert", "vladimir"]

source_file         = "data/empty.c"
include_header_list = ["stdio.h", "data/empty.h"]

extern_test_list, \
static_test_list  = lazy.write_tests(extern_function_list, 
                                     static_function_list, 
                                     include_header_list,
                                     source_file)

def check(FileName):
    os.system("wc %s" % FileName)

print "External Function Test Files:"
for file_name in extern_test_list:
    check(file_name)

print
print "Static Function Test Files:"
for file_name in static_test_list:
    check(file_name)

fs.try_remove_files(extern_test_list + static_test_list)
