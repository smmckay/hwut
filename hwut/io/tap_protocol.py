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
"""PURPOSE: 

Write test output in the 'TAP' protocol format. 

(C) Frank-Rene Schaefer
"""
import hwut.auxiliary.file_system as fs

def do(ResultDb, FileName, SubTestsF):
    if SubTestsF:
        print "Error: tap protocol: subtests are currently not supported."
        
    try:    fh = fs.open_or_die(FileName, "wb")
    except: return False

    fh.write("TAP version 12\n")
    fh.write("1..%i\n" % len(ResultDb))
    done_set = set()
    for i, info in enumerate(ResultDb):
        directory, description, result = info
        if   result.verdict == "OK":   verdict_str = "ok"
        elif result.verdict != "SKIP": verdict_str = "not ok"
        else:                          continue
        if result.choice: choice = "(%s)" % result.choice
        else:             choice = result.choice
        if description.title(): title = description.title()
        else:                   title = description.file_name()

        key = (title, choice)
        if key not in done_set:
            fh.write("%s %i - %s %s\n" % (verdict_str, i, title, choice))
        else:
            done_set.add(key)
    
    fh.close()
    return True
