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
#! /usr/bin/env python
import os
import sys
sys.path.insert(0, os.environ["HWUT_PATH"])

sys.stderr.write(">\n>HWUT_PATH = %s\n>\n" % os.environ["HWUT_PATH"])
sys.stderr.write(">\n>sys.path = %s\n>\n" % sys.path)

from   hwut.auxiliary.path import close_directory_iterable


if "--hwut-info" in sys.argv:
    print "path: close_directory_iterable;"
    sys.exit()

for directory in sorted(close_directory_iterable("./data/1/10/100/1000", 3)):
    if directory.find("TEST") != -1: continue
    # Let's be compatible, even on Windows
    print directory.replace("\\", "/")

