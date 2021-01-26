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

if "--hwut-info" in sys.argv:
    print "C: do;"
    print "CHOICES: without-ctags, ctags;"
    print "NO-TIME-OUT;"
    sys.exit()

import hwut.common as common
if "without-ctags" in sys.argv:
    # Make sure that 'ctags' is not found
    def return_None(): return None
    common.get_ctags_application = return_None
else:
    assert common.get_ctags_application() is not None

import hwut.auxiliary.file_system as     fs
from   hwut.auxiliary.path        import good_path
from   hwut.sos.c.system          import try_compile, try_nm
from   hwut.sos.c.assembler       import Assembler
from   hwut.sos.c.filesystem_db   import FileSystemDb
import hwut.sos.c.core            as     sos
import hwut.io.select             as     select

# Let the interactive selection always return '0'
select.input_integer = lambda a,b,Option=0,Offset=1: (0, True)

# common.set_verbosity_f(True)

to_be_ignored_source = "to_be_ignored.c"
def to_be_ignored_build():
    global to_be_ignored_source

    try: 
        # In case, that the 'move-back' was aborted, try it here.
        os.rename("%s-MOVED" % to_be_ignored_source, to_be_ignored_source)
    except:
        pass

    object_file, output = try_compile(to_be_ignored_source, [], [])
    print "   compiled: %s -> ((%s))" % (to_be_ignored_source, object_file)
    assert object_file is not None

    os.rename(to_be_ignored_source, "%s-MOVED" % to_be_ignored_source)
    return object_file

def to_be_ignored_verify(object_file):
    nm_txt = try_nm(object_file)
    for reference in ("letter0", "letter1", "number0", "number1"):
        if nm_txt.find(reference) != -1: continue
        print "Missing reference in compiled object file to be ignored: '%s'" % reference
        sys.exit(-1)

    return object_file
    
def redundant_object_files_build():
    """Compile the sources into object files. Those object files, also
    need to be ignored, because there are sources that implement the references
    and the references have precedence.
    """
    print "To be ignored: {"
    trash = [ to_be_ignored_build() ]
    to_be_ignored_verify(trash[0])

    file_list = [
        "1/12/123/1234/12345/common_file_name.c",
        "1/12/123/1234/12345/number.c",
        "A/AB/ABC/ABCD/common_file_name.c",
        "A/AB/ABC/ABCD/letter.c",
        "main.c"
    ]
    include_dir_list = ["1/12/123/1234/12345", "A/AB/ABC/ABCD", "extra", "extra/more" ]

    for file_name in file_list:
        object_file, output = try_compile(file_name, include_dir_list, [])
        assert object_file is not None, output
        new_name = good_path(os.path.dirname(file_name), object_file)
        os.rename(object_file, new_name)
        print "   compiled: %s -> ((%s))" % (file_name, new_name)
        trash.append(new_name)

    print "}"
    print
    return trash

def setup(Dir):
    makefile    = "Makefile"
    application_list = ["main.exe", "main2.exe"]

    dir_here = os.getcwd()

    fs.try_remove_glob("hwut-crash-*.[co]")
    fs.try_remove_recursively(Dir, "*.o")
    fs.try_remove_recursively(Dir, "*.exe")
    os.chdir(Dir)


    filesystem_db = FileSystemDb() 
    filesystem_db.preparation(["./"])
    assembler     = Assembler(filesystem_db) 

    trash = redundant_object_files_build()

    fs.try_remove(makefile)
    fs.try_remove(application_list)

    return dir_here, makefile, application_list, filesystem_db, assembler, trash

def make(application):
    sys.stdout.flush()
    os.system("make %s 2>&1 > %s" % (application, os.devnull))
    try:    os.remove("tmp.txt")
    except: pass 

def execute(application):
    if not common.is_windows(): application = "./%s" % application
    os.system(application)

def terminate(dir_here, trash):
    os.system("make clean 2>&1 > tmp.txt")
    os.rename("%s-MOVED" % to_be_ignored_source, to_be_ignored_source)
    for file_name in trash: 
        os.remove(file_name)
    os.chdir(dir_here)

def test(Dir, SourceFileList):
    global chint
    global csetup

    dir_here, makefile, application_list, filesystem_db, assembler, trash = setup(Dir)

    print "Analyse ..."
    sys.stdout.flush()
    sos.do_core(SourceFileList, [], makefile, filesystem_db, assembler)
    sys.stdout.flush()
    print "        ... done."

    for app in sorted(application_list):
        print "Make '%s' ..." % app
        sys.stdout.flush()
        make(app)
        sys.stdout.flush()
        print "          ... done."

    sys.stdout.flush()
    for app in application_list:
        print "Execute '%s' ..." % app
        execute(app)
        sys.stdout.flush()
        print "             ... done."
    terminate(dir_here, trash)


test("data/do", ["main.c", "main2.c"])
print
print "<terminated>"


