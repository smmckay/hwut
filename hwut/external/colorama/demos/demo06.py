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
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
from __future__ import print_function
import fixpath
import colorama
from colorama import Fore, Back, Style
from random import randint, choice
from string import printable

# Demonstrate printing colored, random characters at random positions on the screen

# Fore, Back and Style are convenience classes for the constant ANSI strings that set
#     the foreground, background and style. The don't have any magic of their own.
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

# This assumes your terminal is 80x24. Ansi minimum coordinate is (1,1).
MINY, MAXY = 1, 24
MINX, MAXX = 1, 80

# set of printable ASCII characters, including a space.
CHARS = ' ' + printable.strip()

PASSES = 1000

def main():
    colorama.init()
    # gratuitous use of lambda.
    pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
    # draw a white border.
    print(Back.WHITE, end='')
    print('%s%s' % (pos(MINY, MINX), ' '*MAXX), end='')
    for y in range(MINY, 1+MAXY):
        print('%s %s ' % (pos(y, MINX), pos(y, MAXX)), end='')
    print('%s%s' % (pos(MAXY, MINX), ' '*MAXX), end='')
    # draw some blinky lights for a while.
    for i in range(PASSES):
        print('%s%s%s%s%s' % (pos(randint(1+MINY,MAXY-1), randint(1+MINX,MAXX-1)), choice(FORES), choice(BACKS), choice(STYLES), choice(CHARS)), end='')
    # put cursor to top, left, and set color to white-on-black with normal brightness.
    print('%s%s%s%s' % (pos(MINY, MINX), Fore.WHITE, Back.BLACK, Style.NORMAL), end='')

if __name__ == '__main__':
    main()
