#! /usr/bin/env python
#
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
#
# PURPOSE: Entry point for HWUT.
#
# The command line is separated into two parts:
# 
#    1. The arguments until the first 'minused' argument.
#    2. The remaining arguments.
#
# The LEADING NO-MINUS arguments, they hold the following meaning:
#
#    $1 -- command (test, accept, info, time-info, ...)
#    $2 -- application pattern (e.g. "test*.py")
#    $3 -- choice pattern (e.g. "choice?")
#
# The following arguments follow the usual command line option flag schemes.
#
# (C) Frank-Rene Schaefer
#
# ABSOLUTELY NO WARRANTY
################################################################################
import sys
import os

if not os.environ.has_key("HWUT_PATH"):
    print "Warning: Environment variable 'HWUT_PATH' is not defined'"
    print "Warning: Let it point to the directory where hwut is installed."

sys.path.insert(0, os.path.dirname(sys.argv[0]))

try: 
    # If a calling application pipes and breaks the pipe, then an exception
    # is triggerred. This exception needs to be caught--but only on platforms
    # which actually support it.
    from signal import signal, SIGPIPE, SIG_DFL
    signal(SIGPIPE, SIG_DFL)
except:
    pass

import hwut.common       as common
import hwut.command_line as cl
import hwut.io.messages  as io
    
if __name__ == "__main__":    
    try:
        bye_str        = "<terminated>"
        cl.prepare()
        command, setup = cl.get_setup(sys.argv)
        common.setup   = setup
        command(setup)
    except KeyboardInterrupt:
        print
        io.print_bye_bye()
        bye_str        = "<aborted>"

print " " * (common.terminal_width() - len(bye_str) - 1) + bye_str

