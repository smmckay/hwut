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
# Observe the detection of missing include headers. That is, it considers the 
# output of the compilation and detects the missing reported headers.
#
# Author: Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os
import shutil
import glob

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.auxiliary.executer    as executer
import hwut.auxiliary.file_system as fs

from   hwut.sos.c.system import try_compile, \
                                try_link, \
                                try_nm, \
                                try_preprocess

if "--hwut-info" in sys.argv:
    print "C: Try compiling, linking, nm;"
    print "CHOICES: compile, link, nm, preprocess;"
    sys.exit()

choice = sys.argv[1]

def test_preprocess(SourceFile, IncludeDirList, AddFlagList):
    output  = try_preprocess(SourceFile, IncludeDirList, AddFlagList)
    print "Output:"
    print output

def test_compile(SourceFile, IncludeDirList, AddFlagList):
    object_file, \
    output       = try_compile(SourceFile, IncludeDirList, AddFlagList)

    verdict = (object_file is not None)

    print "_" * 80
    print "SourceFile:     %s;" % SourceFile
    print "IncludeDirList: %s;" % IncludeDirList
    print "AddFlagList:    %s;" % AddFlagList 
    print
    print "=> Verdict:     %s" % verdict
    msg = "<missing>"
    try:  
        if os.path.isfile(object_file): msg = "<exists>"
    except: 
        pass

    print "   OutputFile:  %s" % msg
    print_output(output)

    fs.try_remove(object_file)

def test_link(ObjectFileList, LibraryList, LibraryDirList, AddFlagList):
    
    application, output = try_link(ObjectFileList, LibraryList, LibraryDirList, 
                                            AddFlagList)
    
    print "ObjectFileList:  %s" % [ "((%s)), " % name for name in ObjectFileList ]
    print "LibraryList:     %s" % LibraryList
    print "LibraryDirList:  %s" % LibraryDirList
    print "AddFlagList:     %s" % AddFlagList

    print "=> Verdict:      %s" % (application is not None)
    print_output(output)

    return application

def test_nm(TestName, FileName):
    output = try_nm(FileName)
    print "Test Name:   %s" % TestName
    print "'T' content: {"
    for line in output.splitlines():
        fields = line.split()
        if len(fields) > 2 and fields[1] == "T":
            print "    T: %s" % fields[2].replace("_", "") # Windows <-> Unix
    print "}" 
    
def print_output(Output):
    print "   Output: {"
    print "   ## " + Output.replace("\n", "\n   ## ") 
    print "   }"

def compile_minis():
    main_o, dummy  = try_compile("data/main.c", [], [])
    assert dummy is not None
    mini0_o, dummy = try_compile("data/mini0.c", [], [])
    assert dummy is not None
    mini1_o, dummy = try_compile("data/mini1.c", [], [])
    assert dummy is not None
    mini2_o, dummy = try_compile("data/mini2.c", [], [])
    assert dummy is not None

    return [main_o, mini0_o, mini1_o, mini2_o]

if choice == "compile":
    test_compile("does-not-exist.c", [], [])
    test_compile("data/nonsense.c", [], [])
    test_compile("data/nonsense.c", ["./data"], [])
    test_compile("data/nonsense.c", ["./data"], ["-Wall"])
    test_compile("data/meaningful.c", ["./data"], ["-Wall"])

if choice == "preprocess":
    test_preprocess("does-not-exist.c", [], [])
    test_preprocess("data/nonsense.c", [], [])
    test_preprocess("data/do/1/12/123/1234/12345/number.c", ["./data/do/A/AB/ABC/ABCD"], [])

elif choice == "link":
    
    obj_list = compile_minis()
    
    # Check linking object files
    application = test_link(obj_list[:2], [], [], [])
    fs.try_remove(application)
    application = test_link(obj_list, [], [], [])
    fs.try_remove(application)
    
    print ".----------------------"
    executer.do(["ar", "-r", "libTmp.a"] +  obj_list)
    print "Built libTmp.a: %s" % os.path.isfile("libTmp.a")
    print "'----------------------"
    application = test_link(obj_list[0:1], ["-lTmp"], ["."], [])
    fs.try_remove(application)
    
    # Check LibraryList
    shutil.move("libTmp.a", "data/libTmp.a")
    print ".----------------------"
    print "Move 'libTmp.a' to 'data/': %s" % os.path.isfile("data/libTmp.a")
    print "'----------------------"    
    
    # Check LibraryDirList
    application = test_link(obj_list[0:1], ["-lTmp"], ["data/"], [])
    
    print "   'nm' -->",
    print_output(try_nm(application))
    fs.try_remove(application)
    
    # Check AddFlagList
    # Strip all symbol information. 'nm' must return nothing.
    application = test_link(obj_list[0:1], ["-lTmp"], ["data/"], ["-s"])
    print "   'nm' -->",
    print_output(try_nm(application))
    fs.try_remove(application)

elif choice == "nm":
    test_nm("Non-Existing Object File", "data/not-exist.o")
    obj_list = compile_minis()
    for i, file_name in enumerate(obj_list): 
        test_nm("%i" % i, file_name)

fs.try_remove_files(glob.glob("*.o") + ["data/libTmp.a"])
fs.try_remove_files(glob.glob("*.exe"))
    
print "<terminated>"
