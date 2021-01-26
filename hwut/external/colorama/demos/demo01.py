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
#!/usr/bin/python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

# print grid of all colors and brightnesses
# uses stdout.write to write chars with no newline nor spaces between them
# This should run more-or-less identically on Windows and Unix.
from __future__ import print_function
import sys

# Add parent dir to sys path, so the following 'import colorama' always finds
# the local source in preference to any installed version of colorama.
import fixpath
sys.path.insert(0, "..\\")
from colorama import init, Fore, Back, Style

init()

# Fore, Back and Style are convenience classes for the constant ANSI strings that set
#     the foreground, background and style. The don't have any magic of their own.
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

NAMES = {
    Fore.BLACK: 'black', Fore.RED: 'red', Fore.GREEN: 'green', Fore.YELLOW: 'yellow', Fore.BLUE: 'blue', Fore.MAGENTA: 'magenta', Fore.CYAN: 'cyan', Fore.WHITE: 'white'
    , Fore.RESET: 'reset',
    Back.BLACK: 'black', Back.RED: 'red', Back.GREEN: 'green', Back.YELLOW: 'yellow', Back.BLUE: 'blue', Back.MAGENTA: 'magenta', Back.CYAN: 'cyan', Back.WHITE: 'white',
    Back.RESET: 'reset'
}

# show the color names
sys.stdout.write('        ')
for foreground in FORES:
    sys.stdout.write('%s%-7s' % (foreground, NAMES[foreground]))
print()

# make a row for each background color
for background in BACKS:
    sys.stdout.write('%s%-7s%s %s' % (background, NAMES[background], Back.RESET, background))
    # make a column for each foreground color
    for foreground in FORES:
        sys.stdout.write(foreground)
        # show dim, normal bright
        for brightness in STYLES:
            sys.stdout.write('%sX ' % brightness)
        sys.stdout.write(Style.RESET_ALL + ' ' + background)
    print(Style.RESET_ALL)

print()
