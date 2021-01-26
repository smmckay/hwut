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

sys.path.insert(0, os.environ["HWUT_PATH"])

from hwut.sos.c.output_interpreter import detect_missing_include_headers

if "--hwut-info" in sys.argv:
    print "C: detect_missing_include_headers"
    print "CHOICES: Empty, NoInfo, SomeInfo;"
    sys.exit()

choice = sys.argv[1]

if choice == "Empty": content = ""
else:                 content = open("data/cc-%s.txt" % choice).read()

header_db = detect_missing_include_headers(content)

print "Database:"
for header, including_file in header_db.iteritems():
    print "    %s <-- %s" % (header, including_file) 
    
print "<terminated>"
