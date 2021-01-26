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

import hwut.sos.c.TEST.helper     as     helper
import hwut.auxiliary.file_system as     fs

if "--hwut-info" in sys.argv:
    print "C: Compile User Sources;"
    print "CHOICES: good, fail;"
    print "NO-TIME-OUT;"
    print "HAPPY: ^Error:[' a-zA-Z/\\\\]+;"
    sys.exit()


def test(Dir, IncludeDirList, RootDirListIncludes=["."]):
    source_file_list = [
        # "data/directory_tree/1/10/100/1000/main.c",
        "data/directory_tree/1/10/100/1000/some.c",
        "data/directory_tree/2/10/100/1000/almost-good.c",
        "data/directory_tree/2/10/100/1000/main.c",
        "data/directory_tree/2/10/100/1000/some.c"
    ]
    source_file_list = [ os.path.abspath(x) for x in source_file_list ]

    dir_here = os.getcwd()

    filesystem_db, \
    assembler      = helper.prepare(Dir, IncludeDirList, RootDirListIncludes)

    uncompiled_source_list, \
    unresolved_reference_set,      \
    implemented_reference_set      \
                    = assembler.compile_and_link(source_file_list, [], [])

    helper.terminate(assembler, assembler.compiler.source_to_object_db, uncompiled_source_list)
    print "Implemented:         %s" % "".join("%s, " % x for x in sorted(list(implemented_reference_set)))
    print "Required:            %s" % "".join("%s, " % x for x in sorted(list(unresolved_reference_set)))

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


