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
import subprocess
sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.sos.c.lazy.core        as lazy
import hwut.auxiliary.path         as path
import hwut.auxiliary.file_system  as fs
import hwut.io.select              as select

# Let the interactive selection always return '0'
select.input_integer = lambda a,b,Option=0,Offset=1: (0, True)

if "--hwut-info" in sys.argv:
    print "Generate Test Suite;"
    sys.exit()

class Setup:
    pass

fs.try_remove_recursively("data", "*.o")
fs.try_remove_recursively("data", "*.exe")

os.chdir("data")

# Make sure that the 'dangerous .c' file is there.
path.verify_existence(["source_directory/1/.c"])

fh_devnull = open(os.devnull, "wb")

Setup.first_argument = "source_directory/count.c"
Setup.hint_root_dir_list = ["."]
Setup.hint_root_dir_list_include = [".", "%s/support/C" % os.environ["HWUT_PATH"]]
Setup.hint_root_dir_list_source = []
Setup.hint_root_dir_list_objects = []
Setup.hint_root_dir_list_libraries = []
Setup.hint_exclude_pattern_list = []
Setup.hint_exclude_dir_pattern_list = []
Setup.user_args = []
Setup.user_compile_args = []
Setup.user_link_args = []
Setup.output_makefile = "Makefile"

lazy.do(Setup)

subprocess.call(["make", "clean"], stdout=fh_devnull)
sys.stdout.write("||||\n") # Potpourri lines
sys.stdout.flush()
os.system("make")
sys.stdout.flush()
sys.stdout.write("||||\n") # Potpourri lines
subprocess.call(["make", "clean"], stdout=fh_devnull)

os.chdir("..")
