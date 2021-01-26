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
import fixpath
import colorama

# Demonstrate cursor relative movement: UP, DOWN, FORWARD, and BACK in colorama.CURSOR

up = colorama.Cursor.UP
down = colorama.Cursor.DOWN
forward = colorama.Cursor.FORWARD
back = colorama.Cursor.BACK

def main():
    """
    expected output:
    1a2
    aba
    3a4
    """
    colorama.init()
    print "aaa"
    print "aaa"
    print "aaa"
    print forward() + up(2) + "b" + up() + back(2) + "1" + forward() + "2" + back(3) + down(2) + "3" + forward() + "4"


if __name__ == '__main__':
    main()
