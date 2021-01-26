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
from   hwut.sos.c.implementation_db import ImplementationDb

import hwut.common as common

# Make sure that 'ctags' is not found
def return_None(): return None
common.get_ctags_application = return_None

if "--hwut-info" in sys.argv:
    print "C:       ImplementationDb;"
    print "CHOICES: Sources, NoSources;"
    sys.exit()

def make_libraries(ObjectFileList):
    # Make a library out of every object file and leave it in its directory
    library_list = []
    for i, object_file in enumerate(ObjectFileList):
        file_path = path.good_path(os.path.dirname(object_file), "libMine%i.a" % i)
        try:    os.remove(file_path)
        except: pass
        os.system("ar -cq %s %s" % (file_path, object_file))
        library_list.append(file_path)
        print "## Made Library: %s ((%s))" % (path.relative(file_path), object_file)

def make_object_files(assembler, filesystem_db):
    filesystem_db.preparation(
        RootDirList = ["."],
    )

    source_list = [
        "1/example.c",
        "2/example.c",
        "3/example.c",
        "example.c",
    ]
    assembler.compile_and_link(source_list, [], [])
    return assembler, filesystem_db

def clean_directories():
    def iterable():
        directory_list = [
            "",
            "data/find_references/1/",
            "data/find_references/2/",
            "data/find_references/3/",
            "data/find_references/",
        ]
        for directory in directory_list:
            for file_name in glob(os.path.normpath("%s*.o" % directory)):
                yield file_name
            for file_name in glob(os.path.normpath("%slib*.a" % directory)):
                yield file_name

    fs.try_remove_files(iterable())

def prepare_nice_name_db(SourceToObjectDb):
    # Make sure that the object files appears sorted according to their source files.
    item_list        = sorted(SourceToObjectDb.iteritems(), 
                              key=itemgetter(0))
    object_file_list = [object_file for source, object_file in item_list]
    nice_name_db     = dict((path.relative(x), "object%i.o" % i) 
                            for i, x in enumerate(object_file_list))

    for file_name in object_file_list:
        print "## OBJECT: ((%s))" % file_name
    return nice_name_db

def print_this(implementation_db, nice_name_db):
    # Get relative path to HWUT_PATH. There is some issue under Windows
    # and CygWin with the driver letter. If the upper/lower-case does not
    # match the given directory, a bad relative path is found. 
    # Simple lower-case the whole path.
    print "Directory:" , path.relative(os.getcwd().lower(), os.environ["HWUT_PATH"].lower())
    print
    print
    print "-" * 80
    txt = implementation_db.get_string(nice_name_db)
    for name, nice_name in nice_name_db.iteritems():
        txt = txt.replace(name, nice_name)
    print txt

#______________________________________________________________________________
#
os.chdir("data/find_references")

filesystem_db = FileSystemDb()
assembler     = Assembler(filesystem_db)

make_object_files(assembler, filesystem_db)
make_libraries(assembler.compiler.source_to_object_db.values())

nice_name_db  = prepare_nice_name_db(assembler.compiler.source_to_object_db)

#______________________________________________________________________________
#
# Re-prepare to capture the newly compiled object files and libraries
filesystem_db.preparation(
    RootDirList = ["."],
)

if "NoSources" in sys.argv:
    assembler.compiler.source_to_object_db = {}
if "Sources" in sys.argv:
    filesystem_db.object_file_db.clear()

#______________________________________________________________________________
#
# TEST:
#
implementation_db = ImplementationDb.without_ctags(assembler, filesystem_db) 

print_this(implementation_db, nice_name_db)

clean_directories()

