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
"""
               Sender        Receiver                   Remote Target
                 |              |                             |
                 |              |   establish connection      |
                 O------------------------------------------->|
                 |              O---------------------------->|
                 |              |                             |
                 |      .----------------.                    |
                 |      | Wait for:      |                    |
                 |      | <<hwut-begin>> |                    |
                 |      | + magic        |                    |
                 |      '----------------'                    |
                 |              |                             |
                 O----( <<hwut-begin>> magic )--------------->|
                 |              |<--( <<hwut-begin>> magic )--O
                 |              |                             |
                 |      .----------------.                    |
                 |      | Receive Test   |                    |
                 |      | Output         |                    |
                 |      '----------------'                    |
                 |              |<----------( Content )-------O
                 |              |<----------( Content )-------O
                 |              |          ...                |
                 |              |<----------( Content )-------O
                 |              |                             |
           .-[ OPTIONAL ]-------------------------------------------.
           |     |              |                             |     |
           |     O----( <<hwut-end>> magic )----------------->|     |
           |     |              |                             |     |
           '--------------------------------------------------------'
                 |              |                             |
                 |              |<----( <<hwut-end>> magic )--O
                 |              |                             |
              (STOP)         (STOP)                        (STOP)
      
magic = 6 letter/digit string which is determined randomly at run-time.  It
serves as an identifier, to make sure that the response belongs to the request.

(C) Frank-Rene Schaefer
"""
import hwut.io.messages as io

import os
import sys
from   threading import Thread

class RemoteExecuter:
    """Base class for objects that act as 'ExecutionUnit'-s for remote 
    execution. The main function of this class is the function call operator
    '__call__'. It provided an interface similar to 'subprocess.Popen'. 

    Then the function call operator is called, it returns a RemoteThread
    object, or 'None' if the remote process execution cannot be started. 

    The RemoteThread object has two functions which are required by the caller:
    '.wait()' which waits for the execution to terminate and '.kill()' which
    initiates a forced termination of the remote execution.

    Particular protocols are implemented in derived classes as well as their
    receivers and senders.
    """
    BeginToken = "<<hwut-begin>>"
    EndToken   = "<<hwut-end>>"
    EndTokenL  = len("<<hwut-end>>")

    def __init__(self, Sender, Receiver, RemotePath):
        # setup connection to the agent on the remote target
        self.sender      = Sender
        self.receiver    = Receiver
        self.remote_path = RemotePath

    def __call__(self, CommandLine, stdout, stderr, env):
        """The call to the remote executor must comply the the signature and
        behavior of an 'ExecutionUnit' as described in the documentation of 
        function 

                        hwut.auxiliary.executer.do()

        That is, it must spawn a thread and provide a handle to something 
        that implements '.wait()' and '.kill()'.

        The 'env' is currently only there for conformity.
        """
        if not CmdLine: return None # Cannot start

        # Start the remote process
        command = "".join("%s " % cmd for cmd in CmdLine)[:-1] # len(CmdLine) > 0

        if not command: return None # Cannot start

        return RemoteThread(self.remote_path, command, stdout)
 
    def _extract(self, Info, Parameter, Default=None):
        Name           = Info["Name"]
        ConnectionType = Info["Type"]
        if not Info.has_key(Parameter):
            if Default is None: 
                io.remote_start_requires_parameter_definition(ConnectionType, 
                                                              Name, Parameter, 
                                                              Info.keys())
                sys.exit()
            return Default
        value = Info[Parameter]
        if type(Default) in (int, long): 
            if len(value) > 2 and value[:2] == "0x": return int(value[2:], 16)
            else:                                    return int(value)
        return value

class RemoteThread:
    def __init__(self, Sender, Receiver, RemotePath, Command, StdOut):
        args          = (RemotePath, Command)
        self.sender   = Sender
        self.receiver = Receiver

        start_identifier, end_identifier = self.receiver.init()
        self.thread = threading.Thread(target=self.receiver.do, 
                                       args=(StdOut,end_identifier))
        self.thread.start()
        self.sender.init(start_identifier, RemotePath + Command)
        return self

    def wait(self):
        self.thread.join()

    def kill(self):
        self.sender.force_termination()
        self.thread.join(0)

    def clean(self):
        self.sender.close()
        self.receiver.close()

class Sender:
    """Base class for all remote senders. Functions to be implemented by the
    derived class are implemented as 'assert False'.
    """
    def send(self, Command):       assert False
    def close(self):               assert False
    def init(self, StartIdentifier, Command):
        self.send(start_identifier)
        self.send(Command + "\n")
    def force_termination(self):
        self.send("%s\n" % RemoteExecuter.EndToken)

class Receiver:
    def init(self):
        magic_number     = random.randint(2**23, 2**24)
        start_identifier = "%s %06X\n" % (RemoteExecuter.BeginToken, magic_number)
        self.receive_init()
        return start_identifier

    def thread_function(self, stdout, StartIdentifier, EndIdentifier):
        # Wait until the receiver acknowledges begin of test.
        StartIdentifierL = len(StartIdentifier)
        EndIdentifierL   = len(EndIdentifier)
        data = ""
        while not data.match_end(StartIdentifier, StartIdentifierL):
            data = self.receive_chunk()
            
        while 1 + 1 == 2:
            data = self.receive_chunk()
            if Receiver.match_end(EndIdentifier, EndIdentifierL): break
            stdout.write(data)
        stdout.write(data[:-EndIdentifierL])

    @staticmethod
    def match_end(self, Data, DataL):
        """Check whether the current data chunk ends with 'EndToken'. If so, 
        the reception needs to stop.

        RETURNS: True  -- if Data ends with 'EndToken'
                 False -- if not.
        """
        if DataL < RemoteExecuter.EndTokenL: return False 
        
        return Data[:-RemoteExecuter.EndTokenL] == RemoteExecuter.EndToken

    def receive_init(self):  assert False
    def receive_chunk(self): assert False

if __name__ == "__main__":
    spy   = { "Type": "TCP", "Adr": "",             "Port": 37773, }
    agent = { "Type": "TCP", "Adr": "192.168.1.11", "Port": 37773, }

    class something_else:
        name = "'Hello World\nNice to meet you.\n<<end>>'"

    class something:
        def file_name(self):    return "/host/hwut_spy"
        def choice(self):       return something_else()
        def OUT_FileName(self): return "test-output-filename.txt"

    info = something()
    do(info, spy, agent)

