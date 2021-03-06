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
# Check the functionality to find include headers based on a list 
# of given root directories.
#
# Author: Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os
from   copy import copy

sys.path.insert(0, os.environ["HWUT_PATH"])
# Make sure that 'ctags' is not found
import hwut.common as common
def return_None(): return None
common.get_ctags_application = return_None

import hwut.sos.c.TEST.helper     as     helper

if "--hwut-info" in sys.argv:
    print "C: compile_source_list;"
    print "CHOICES: good, fail;"
    sys.exit()


def test(Dir, IncludeDirList, RootDirListIncludes=["."]):
    dir_here = os.getcwd()

    filesystem_db, \
    assembler      = helper.prepare(Dir, IncludeDirList, RootDirListIncludes)

    bad_source_list, \
    goo_object_list  = assembler.compiler.do_list(filesystem_db.source_file_list())

    helper.terminate(assembler, assembler.compiler.source_to_object_db, bad_source_list)

    os.chdir(dir_here)

if "good" in sys.argv:
    test("data/directory_tree/1/10/100/1000", 
         ["data/directory_tree"], 
         RootDirListIncludes=["data/directory_tree/"])
else:
    test("data/directory_tree/1/10/100/1000", 
         IncludeDirList      = ["data/directory_tree/1/10/100/1000"], 
         RootDirListIncludes = ["data/directory_tree/1/10/100/1000"])
    print
    test("data/directory_tree/1/10/100/1000", 
         IncludeDirList      =[
             "data/directory_tree/1/10/100/1000"
         ], 
         RootDirListIncludes = [ 
            'data/directory_tree/2/10/100/1000', 
            'data/directory_tree/1/10/100/1001', 
            'data/directory_tree/1/12/100'
         ])


