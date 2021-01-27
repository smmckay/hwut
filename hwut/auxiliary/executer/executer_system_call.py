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
import hwut.io.messages           as io
from   hwut.auxiliary.executer.executer import Executer
import hwut.auxiliary.file_system as fs
import hwut.common                as common
import subprocess
import threading
from   numbers    import Number
import os
import signal
import tempfile
import stat
import time
from   copy       import copy
from   StringIO   import StringIO
from   exceptions import OSError, Exception

class ExecuterSystemCall(Executer):
    def __init__(self, CmdLine, stdout, stderr, env):
        if common.is_posix():
            # preexec_fn: AFTER  forking new process.
            #             BEFORE executing new process.
            # os.setsid:  Start a new process group and make the process
            #             the group leader. So, we can kill the whole group
            #             of processes related to the test.
            process = subprocess.Popen(CmdLine, stdout=stdout, stderr=stderr, 
                                       env=env, shell=False, 
                                       preexec_fn=os.setsid)
        elif common.is_windows():
            process = subprocess.Popen(CmdLine, stdout=stdout, stderr=stderr, 
                                       env=env, shell=False, 
                                       creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            # When we use Python > 3.2 ...
            process = subprocess.Popen(CmdLine, stdout=stdout, stderr=stderr, 
                                       env=env, shell=False, 
                                       start_new_session=True)
        self.process = process


        
