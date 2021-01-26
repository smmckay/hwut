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
#
# Testing the 'satisfy' algorithm. The task of the algorithm is to assign
# values to parameters, while there is a restricted set of possible values
# for each parameter. Also, each value can appear only once. The 'satisfy'
# algorithm provides a solution for problems such as:
#
#    parameter:   possible values:
#        A        [1, 3, 6]
#        B        [2, 3]
#       ...
#        C        [5, 6, 7]
#
# Where each of the number 1, 2, 3, 5, 6, 7 can at max. appear once.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import os
import sys

sys.path.insert(0, os.environ["HWUT_PATH"])

from hwut.verdict.potpourri import satisfy

from StringIO import StringIO

if "--hwut-info" in sys.argv:
    print "Satisfy Alternatives;"
    sys.exit()


def test(Db):
    print "_" * 80
    for x, alternative_list in Db.iteritems():
        print "%x: %s" % (x, alternative_list)
    result = satisfy(Db)
    if result is None:
        print "<No Solution>"
        return
    print 
    for x, assignee in sorted(result):
        assert assignee in Db[x]
        print "%s: %s" % (x, assignee)
    return


test({ 1: [10, 11], 2: [10, 11]})

test({ 1: [10, 11],     2: [10, 11],     3: [10, 11]})
test({ 1: [10, 11, 12], 2: [10, 11],     3: [10, 11]})
test({ 1: [10, 11],     2: [10, 11, 12], 3: [10, 11]})
test({ 1: [10, 11],     2: [10, 11],     3: [10, 11, 12]})
test({ 1: [10, 12],     2: [10, 11],     3: [11, 12]})

test({ 1: [10, 11, 12, 13],  2: [10, 11, 12, 13], 3: [10, 11, 12, 13]})
test({ 1: [10, 11, 12, 13, 14],  
       2: [11, 12, 13, 14, 15], 
       3: [12, 13, 14, 15, 16], 
       4: [13, 14, 15, 16, 17], 
       5: [14, 15, 16, 17, 18]})
test({ 1: [11, 12, 13, 14],  
       2: [11, 12, 13, 14], 
       3: [13, 14, 15, 16], 
       4: [13, 14, 15, 16, 17], 
       5: [14, 15, 16, 17]})
test({ 1: [11, 12, 15, 13, 14],  
       2: [11, 12, 13, 14], 
       3: [13, 14, 15], 
       4: [11, 12], 
       5: [11, 12]})
