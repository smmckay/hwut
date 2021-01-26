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
import sys
import os
import shutil

sys.path.insert(0, os.environ["HWUT_PATH"])

import hwut.coverage.lcov         as lcov
import hwut.auxiliary.executer.core    as executer
import hwut.auxiliary.path        as path
import hwut.auxiliary.file_system as fs

if "--hwut-info" in sys.argv:
    print "LCOV Coverage Analyzer - Related Functionality;"
    print "CHOICES: parse, save, collect;"
    sys.exit()


def test_save(Dir):
    here_dir = os.getcwd()
    os.chdir("data/lcov/%s" % Dir)
    try:    shutil.copy("nonsense.gcda.SAVE_AWAY", "nonsense.gcda")
    except: pass

    fs.try_remove("%s.info" % Dir)

    file_name_list = lcov.save("T%s" % Dir, NamingF=True) 
    assert file_name_list is not None
    assert len(file_name_list) == 1

    line_list = [
        "    %s" % line
        for line in sorted(open(file_name_list[0], "rb").readlines())
        if line.find("SF:") != 0
    ]
    os.chdir(here_dir)
    print "file name: %s" % path.relative(file_name_list[0])
    print "".join(line_list)

if "parse" in sys.argv:
    print "-" * 80
    coverage_db = lcov.parse("data/test.info")
    for file_name, content in coverage_db.iteritems():
        print content
    print "-" * 80
    coverage_db = lcov.parse("data/test2.info")
    for file_name, content in coverage_db.iteritems():
        print content
    print "-" * 80

elif "save" in sys.argv:
    test_save("1")
    test_save("2")

elif "collect" in sys.argv:
    fs.try_remove("collected.info")

    lcov.collect([
        os.path.normpath(file) 
	for file in ("data/lcov/collect/a/b/c/y.info", 
                     "data/lcov/collect/q/r/s/x.info")
	],
        "collected.info") 
   
    print "".join(
        "    %s" % line
        for line in sorted(open("collected.info", "rb").readlines())
        if line.find("SF:") != 0
    )





    
