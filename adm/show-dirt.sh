# PURPOSE: Cleaning the directory tree from useless things.
#
# (This file has been originally developped in the frame of HWUT--The Hello
#  Worldler's Unit Test. Copyright and Licensing is as mentioned.)
#
# (C) 2007-2015 Frank-Rene Schaefer  fschaef@users.sourceforge.net
# 
# ABSOLUTELY NO WARRANTY
#
#------------------------------------------------------------------------------
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


# -- filter out all files that are not directly required for 
#    a working application.
extension_list="svn o obj exe pyc pyo bak orig swo swp stackdump 7z backup orig tgz tbz zip pdf ps"
path_list="TEST\/OUT TEST\/f?[0-9]+\/OUT doc\/manual\/build TEST\/htmlcov dumpster " 
# path_list="TEST TEST-old TEST\/OUT TEST\/f?[0-9]+\/OUT doc\/manual\/build TEST\/htmlcov dumpster " 
file_list="tmp\.[a-z]+\$ stats.log\$ core\$ °$ *~$"

txt0=$(for x in $(echo "$extension_list"); do printf "/\.%s$/ || " $x; done; echo) 
txt1=$(for x in $(echo "$path_list"); do      printf "/\/%s\// || " $x; done; echo) 
txt2=$(for x in $(echo "$file_list"); do      printf "/\/%s/ || " $x; done; echo)
txt_end="/\/nOnSeNse.txt/ { print; }"

find -type f | awk "$txt0 $txt1 $txt2 $txt_end" 
