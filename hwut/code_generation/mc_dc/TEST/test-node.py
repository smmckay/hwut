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

from   hwut.code_generation.mc_dc.core import *

if "--hwut-info" in sys.argv:
    print "Plain node tests;"
    print "CHOICES: NodeLeaf, NodeNot, NodeAnd, NodeOr;"
    sys.exit()

elif "NodeLeaf" in sys.argv:
    node = NodeLeaf(4711)
elif "NodeNot" in sys.argv:
    node = NodeNot(NodeLeaf(100))
elif "NodeAnd" in sys.argv:
    node = NodeAnd([NodeLeaf(100), NodeLeaf(200)])
elif "NodeOr" in sys.argv:
    node = NodeOr([NodeLeaf(100), NodeLeaf(200)])

print "Require True:"
for sequence in node.require(True):
    print "".join("%5 " % flag for flag in sequence)

print "Require False:"
for sequence in node.require(False):
    print "".join("%5 " % flag for flag in sequence)
