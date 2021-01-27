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
import hwut.common as common
import signal
import os

class Executer:
    def __init__(self, CmdLine, stdout, stderr, env):
        assert False

    def kill(self):
        if   self.process is None:            return
        elif self.process.poll() is not None: return

        try:
            if common.is_posix():
                os.killpg(self.process.pid, signal.SIGKILL)
            else:
                # Assume it's windows. 
                # Somehow, windows does not seem to like 'SIGTERM'
                os.kill(self.process.pid, signal.SIGTERM)
        except:
            print "Error while killing process %s." % self.process.pid

    def is_alive(self):
        if self.process is None: return False
        return self.process.poll() is None

    def wait_for_termination(self):
        self.process.communicate()
        

