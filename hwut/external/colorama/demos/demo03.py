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

# Demonstrate the different behavior when autoreset is True and False.

from __future__ import print_function
import fixpath
from colorama import init, Fore, Back, Style

init(autoreset=True)
print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + 'Line 1: colored, with autoreset=True')
print('Line 2: When auto reset is True, the color settings need to be set with every print.')

init(autoreset=False)
print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + 'Line 3: colored, with autoreset=False')
print('Line 4: When autoreset=False, the prior color settings linger (this is the default behavior).')
