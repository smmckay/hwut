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
from   hwut.sos.c.assembler       import Assembler
from   hwut.sos.c.filesystem_db   import FileSystemDb
import hwut.auxiliary.file_system as     fs
import hwut.auxiliary.path        as     path
from   copy import copy
import os

include_dirs_before = None

def prepare(Dir, IncludeDirList, RootDirListIncludes):
    global include_dirs_before

    RootDirListIncludes = [ os.path.abspath(x) for x in RootDirListIncludes ]
    IncludeDirList      = [ os.path.abspath(x) for x in IncludeDirList ]
    os.chdir(Dir)
    IncludeDirList      = [ path.relative(x) for x in IncludeDirList ]
    RootDirListIncludes = [ path.relative(x) for x in RootDirListIncludes ]

    filesystem_db = FileSystemDb()
    filesystem_db.preparation(
        RootDirListIncludes = RootDirListIncludes
    )
    assembler     = Assembler(filesystem_db)
    
    assembler.compiler.flag_list = ["-I%s " % x for x in IncludeDirList ]

    print "Here:                %s" % Dir
    print "IncludeDirs:         %s" % IncludeDirList
    print "RootDirListIncludes: %s" % RootDirListIncludes

    include_dirs_before = copy(IncludeDirList)
    return filesystem_db, assembler


def terminate(assembler, source_to_object_db, UncompiledSourceList):
    verdict = (len(UncompiledSourceList) == 0)

    new_include_dirs = set(assembler.compiler.include_dir_db.get_directories(None)).difference(include_dirs_before)


    print "Verdict:             %s" % verdict
    print "New IncludeDirs:     %s" % sorted([path.relative(x) for x in new_include_dirs]) 
    print "Not Compiled:        %s" % sorted([path.relative(x) for x in UncompiledSourceList])
    print "SourceToObjectDb: {"
    for source_file, object_file in sorted(source_to_object_db.iteritems(), key=lambda x: (len(x[0]), x[0])): 
        print "        %s -> ((%s))" % (path.relative(source_file), object_file)
    print "}"

    assembler.clean_up()

