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

sys.path.insert(0, os.environ["HWUT_PATH"])

# Make sure that 'ctags' is not found
import hwut.common as common
def return_None(): return None
common.get_ctags_application = return_None

from   hwut.sos.c.filesystem_db   import FileSystemDb
import hwut.auxiliary.path        as     path
import hwut.auxiliary.file_system as     fs
import glob

if "--hwut-info" in sys.argv:
    print "C:  Collect files in hint directories;"
    sys.exit()

# Delete any possible trailing object files.
fs.try_remove_recursively("data/directory_tree", "*.o")

os.chdir("data/directory_tree")

# (*) Prepare: 
#     Make sure, that object files exist, at least by name
def touch(FileName):
    try:    open(FileName, "w").close()
    except: pass

file_list = [
    "./1/10/100/object_100.o",
    "./1/10/100/1001/object_1001.o",
    "./2/10/100/1000/object_1000.o"    # Not to be found!
]
for file in file_list:
    touch(file)


# (*) Build the Database
#
chint = FileSystemDb()

chint.preparation(
    RootDirListIncludes  = ["1/12/100", "1/10", "2"], 
    RootDirListSources   = ["1/10",             "2"],
    RootDirListLibraries = ["1/12/100",         "2"], 
    RootDirListObjects   = ["1/12/100", "1/10"]
)
    

# (*) Display the Database
def display(Name, Db):
    print "%s:" % Name
    for file_name, directory_set in sorted(Db.iteritems()):
        dir_list = [ path.relative(x) for x in directory_set ]
        print "    %s --> %s" % (file_name, repr(sorted(dir_list))[1:-1])

display("include_db", chint.include_file_db)
display("source_db",  chint.source_file_db)
display("library_db", chint.library_file_db)
display("object_db",  chint.object_file_db)


for file in file_list:
    os.remove(file)
