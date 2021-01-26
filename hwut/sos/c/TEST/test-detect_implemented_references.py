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
# Observe the detection of implemented references. That is, it considers the 
# output of the 'nm' program and derives the list of implemented and referenced
# functions.
#
# Author: Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os

sys.path.insert(0, os.environ["HWUT_PATH"])

from hwut.sos.c.output_interpreter import detect_implemented_references

if "--hwut-info" in sys.argv:
    print "C: detect_implemented_references"
    print "CHOICES: Empty, NoInfo, SomeInfo;"
    sys.exit()

choice = sys.argv[1]

if choice == "Empty": content = ""
else:                 content = open("data/nm-%s.txt" % choice).read()

implemented_list, \
unresolved_list,  \
static_list       = detect_implemented_references(content)

print "Implemented:"
for function in sorted(implemented_list):
    print "    %s" % function
    
print "Unresolved:"
for function in sorted(unresolved_list):
    # Windows/Unix linking conventions ...
    if   function.find("gcov_init") != -1:      function = "__gcov_init"
    elif function.find("gcov_merge_add") != -1: function = "__gcov_merge_add"
    print "    %s" % function
    
print "Static:"
for function in sorted(static_list):
    print "    %s" % function
    
print "<terminated>"
