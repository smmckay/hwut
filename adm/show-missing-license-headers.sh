#! /usr/bin/env bash
#
# PURPOSE: Find all relevant files in the file system that do not contain
#          the license header. 
#
# Several files are excluded from consideration (see below). As 'hint' for a 
# missing license header string "SPDX license identifier" is used. It appears 
# on top of every license header.
#
# The output is formatted so that a 'gcc compiler parser' may use it as input
# for direct jumping to the issue. For example in 'vim':
#
#   :set makeprg=bash
#   :make adm/show-missing-license-headers.sh
#
# will step through all files with missing license headers. The lines are 
# sorted by file extension. This helps the user to copy the exact same content
# as many times as possible.
#
# (C) Frank-Rene Schaefer, Visteon, Kerpen, Germany.
#______________________________________________________________________________
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

grep -FL SPDX . -r \
     --exclude     "*~"      \
     --exclude     "*.htm"   \
     --exclude     "*.orig"  \
     --exclude     "*.html"  \
     --exclude     "*.jpg"   \
     --exclude     "*.mm"    \
     --exclude     "*.png"   \
     --exclude     "*.rst"   \
     --exclude     "*.svg"   \
     --exclude     "*.txt"   \
     --exclude     "*.uxf"   \
     --exclude     "*.xcf"   \
     --exclude     cache.fly \
     --exclude-dir "TEST*"   \
     --exclude-dir dev       \
     --exclude-dir external  \
     --exclude-dir smile     \
| while IFS='' read -r line || [[ -n "$line" ]]; do
    # Write 'extension' ' ' 'file-name'.
    # So that the list can be sorted by extension.
    extension="${line##*.}"
    echo "$extension $line" 
done \
| sort \
| awk '{ print $2 ":1:    watch here."; }'

