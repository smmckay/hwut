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
# Check the functionality to find references in source files, object files
# and libraries. Files under concerns are located in 'data/find_references'.
# 
# Object files and libraries are buildt in place, so that the test may run 
# on different platforms.
#
#   CHOICE:            Tested member functions of class FileSystemDb:
#
#   "in_sources"   --> .find_references_in_source_files
#   "in_objects"   --> .find_references_in_object_files
#   "in_libraries" --> .find_references_in_libraries
#   "in_all"       --> .find_references
#
# Author: Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os

from   glob import glob
from   copy import copy
from   operator import itemgetter

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.auxiliary.file_system   as     fs
import hwut.auxiliary.path          as     path
from   hwut.sos.c.assembler         import Assembler
from   hwut.sos.c.filesystem_db     import FileSystemDb
from   hwut.sos.c.declaration_db    import DeclarationDb
import hwut.io.select               as     select

# Let the interactive selection always return '0'
select.input_integer = lambda a,b,Option=0,Offset=1: (0, True)

import hwut.common as common


if "--hwut-info" in sys.argv:
    print "C:       DeclarationDb;"
    print "CHOICES: with-ctags, without-ctags;"
    print "SAME;"
    sys.exit()

identifier_list = [
    "_some", "_a", "_b", "_c", "_missing", "_twice" 
    "extern_some", "extern_a", "extern_b", "extern_c", "extern_missing", "extern_twice" 
    "static_some", "static_a", "static_b", "static_c", "static_missing", "static_twice" 
]

include_path_list = [
    ".",
    "./1",
    "./1/10",
    "./1/10/100",
    "./1/10/100/1000",
    "./1/10/100/1001",
    "./1/10/102",
    "./1/10/102/1000",
    "./1/12",
    "./1/12/100",
    "./2",
    "./2/10",
    "./2/10/100",
    "./2/10/100/1000",
]

#______________________________________________________________________________
#
os.chdir("data/declaration_db")

if   "without-ctags" in sys.argv:
    # Make sure that 'ctags' is not found
    def return_None(): return None
    common.get_ctags_application = return_None

    declaration_db = DeclarationDb.without_ctags(identifier_list,
                                                 include_path_list)

elif "with-ctags" in sys.argv:
    # Business as usual
    declaration_db = DeclarationDb.with_ctags(identifier_list,
                                              include_path_list)
else:
    assert False

#______________________________________________________________________________
#
# Display:
#
print "Directory:" , path.relative(os.getcwd().lower(), os.environ["HWUT_PATH"].lower())
print
print
print "-" * 80
print DeclarationDb.get_string(declaration_db)


