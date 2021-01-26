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
#! /usr/bin/env python
import os
import sys
import stat

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.auxiliary.file_system as     fs
import hwut.preparation.hwut_info as     hwut_info
from   hwut.common                import HWUT_INFO_FILE_NAME

if "--hwut-info" in sys.argv:
    print "Parsing hwut-info.dat."
    print "CHOICES: access, parse, filter, auto-generate;"
    sys.exit()

def setup(TmpDirName, HwutInfoContent, FileNameList=[]):
    """(1) Generates a temporary directory 'TmpDirName'
       (2) In that directory a 'hwut_info.dat' file is generated.
           'HwutInfoContent' is what is written into it.
       (3) In that directory the list of files in 'FileNameList'
           is generated and made executable.
    """
    # Create a temp-directory
    try:    os.mkdir(TmpDirName)
    except: pass

    print "DIR:                  ", os.access(TmpDirName, os.R_OK)

    os.chdir(TmpDirName)

    # Generate 'hwut-info.dat'
    if HwutInfoContent is not None:
        fh = open(HWUT_INFO_FILE_NAME, "wb")
        fh.write(HwutInfoContent)
        fh.close()
        os.chmod(HWUT_INFO_FILE_NAME, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        print "HWUT_INFO_FILE_NAME:  ", os.access(HWUT_INFO_FILE_NAME, os.R_OK)

    # Generate list of executable files
    if FileNameList:
        print "FILES:"
        L = max(len(name) for name in FileNameList)
        for file_name in sorted(FileNameList):
            fh = open(file_name, "wb")
            fh.write("echo \"Me %s\"" % file_name)
            fh.close()
            os.chmod(file_name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
            print "    %s: %s%s" % (file_name, " " * (L-len(file_name)), os.access(HWUT_INFO_FILE_NAME, os.R_OK))

def clean(TmpDirName):
    fs.try_remove_files(os.listdir("."))
    os.chdir("..")
    try:    os.rmdir(TmpDirName)
    except: pass

            
def test_parse(Content):
    setup("tmp.parse", Content)
    fh = open(HWUT_INFO_FILE_NAME, "rb")
    true_db, false_set, remote_db, coverage_selector = hwut_info._parse(fh)
    print "FalseSet:", false_set
    print "TrueDb:"
    for key, value in true_db.iteritems():
        print "%s:\n%s" % (key, value) 
    clean("tmp.parse")

def test_filter(TrueDb, FalseSet, FileNameList):
    print 
    print "true_db:  ", sorted(TrueDb.keys())
    print "false_set:", sorted(list(FalseSet))
    print 
    setup("tmp.filter", "", FileNameList)
    result = hwut_info._filter(TrueDb, FalseSet)
    print "result:"
    for file_name, interpreter_sequence in sorted(result.iteritems()):
        print "   [%s] --> %s" % (file_name, interpreter_sequence)
    clean("tmp.filter")

def test_auto_gen(TrueDb, FalseSet):
    setup("tmp.auto", None)
    hwut_info.auto_generate(TrueDb, FalseSet)
    print 
    print "true_db:  ", sorted(TrueDb.keys())
    print "false_set:", sorted(list(FalseSet))
    print 
    print "---// %s //-------------------------" % HWUT_INFO_FILE_NAME
    print open(HWUT_INFO_FILE_NAME, "rb").read()
    print "-----------------------------------------"
    clean("tmp.auto")
    
   
if "access" in sys.argv: 
    try:    os.mkdir("tmp.access")
    except: pass
    os.chdir("tmp.access")
    print "Without hwut_info.dat: %s" % hwut_info.access("r")
    os.chdir("..")
    setup("tmp.access", "Hallo")
    print "With hwut_info.dat:    [%s]" % hwut_info.access("r").read()
    clean("tmp.access")

elif "parse" in sys.argv:
    print
    print "---// straight //----------------------------"
    print
    test_parse("?a*")
    test_parse("sh ?b*")
    test_parse("sh interpreter.sh ?c*")
    print
    print "---// not //---------------------------------"
    print
    test_parse("--not ?a*")
    test_parse("--not dest ?b*")
    test_parse("--not cest dest ?c*")
    print
    print "---// wild //--------------------------------"
    print
    test_parse(
            "?a* \n" \
            "sh ?b* \n" \
            "sh interpreter.sh ?c*\n" \
            "--not C \n" \
            "--not A C\n" \
            "--not A B C")

elif "filter" in sys.argv:
    print
    print "---// empty //-------------------------------"
    print
    true_db   = {}
    false_set = set()
    test_filter(true_db, false_set, [])
    test_filter(true_db, false_set, ["a", "b", HWUT_INFO_FILE_NAME])

    print
    print "---// one //---------------------------------"
    print
    true_db   = { "*.a": [], }
    false_set = set(["b*"])
    test_filter(true_db, false_set, [])
    test_filter(true_db, false_set, ["x.a", "x.b", "b.a", HWUT_INFO_FILE_NAME])

    print
    print "---// two //---------------------------------"
    print
    true_db   = { "*.a": [], "b*": []}
    false_set = set(["b*.a", "a*.b"])
    test_filter(true_db, false_set, [])
    test_filter(true_db, false_set, [
        "b00.a", "a00.b", "b00.b", "a00.a", "b00.b", HWUT_INFO_FILE_NAME
    ])

elif "auto-generate" in sys.argv:
    true_db   = {}
    false_set = set()
    test_auto_gen(true_db, false_set)
    true_db   = {"Aaa": [], 
                 "Bbb": ["valgrind"], 
                 "Ccc": ["cccc.x", "dddddddd.y"],
                 "Ddd": ["cccc.x", "dddddddd.y", "X"] }
    false_set = set(["f%02i" % i for i in range(32)])
    test_auto_gen(true_db, false_set)
