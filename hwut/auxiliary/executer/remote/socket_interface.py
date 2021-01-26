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
import hwut.auxiliary.executer.remote.base         as     base
from   hwut.temporal_logic.parser.lexical_analysis import read_integer

from   collections import namedtuple
from   StringIO    import StringIO
import subprocess
import socket
import time

class Connection:
    def __init__(self):
        self.server = None
        self.socket = None
        self.info   = None

class ExecuterRemoteSocket(base.ExecuterRemote):
    """Implements a remote execution on socket basis.
    """
    def __init__(self, Configuration, CommandLine, stdout, stderr): 
        self.configuration = Configuration
        base.ExecuterRemote.__init__(self, CommandLine, stdout, stderr)
        #    |
        #    '--> Thread()
        #         |
        #         '---> base.ExecuterRemote.receive()
        #               |
        #               '---> self.configuration.open()
        #               '---> self.configuration.send()
        #               '---> self.configuration.receive()
        #______________________________________________________________________

    @classmethod
    def for_QueryApplicationList(cls, Configuration):
        # CmdLine = None  => Query for test application list.
        return cls(Configuration, None, None, None)


class ConfigurationSocket(base.RemoteConfiguration): 
    def __init__(self, ConnectionId):
        base.RemoteConfiguration.__init__(self, ConnectionId, ExecuterRemoteSocket)
        self.ip_adr_to_listen = ""    # Accept on all interfaces
        self.port_to_listen   = 37773 # Default hwut port to listen
        self.script_to_start  = None

        self._connection      = None

    def set_parameter(self, Name, Value):
        if   Name == "ip":    self.ip_adr_to_listen = Value
        elif Name == "port":  self.port_to_listen   = read_integer(StringIO(Value))
        elif Name == "start": self.script_to_start  = Value
        else:                 return False
        return True

    def open(self):
        if self._connection is None: 
            self._connection = self.__open()

        if self._connection is None:
            return False

        # Now, defined: self._connection.server 
        #               self._connection.socket 
        #               self._connection.info
        return True

    def is_ok(self):
        return     self._connection is not None \
               and self._connection.socket is not None

    def send(self, Content):
        if self._connection is None or self._connection.socket is None: return False
        self._connection.socket.send(Content)
        return True

    def receive(self):
        if self._connection is None or self._connection.socket is None: return False
        return self._connection.socket.recv(64)

    def close(self):
        if self._connection is None: return
        self._connection.socket.send(base.HWUT_REMOTE_SETTING_EXECUTION_STOP)
        self._connection.socket.close()

    def __open(self):
        """Open a socket with the given self's configuration.
        """
        connection = Connection()

        # Create an INET, STREAMing socket
        connection.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if connection.server is None: return None

        # Bind the socket to a public host,
        # and a well-known port
        if self.ip_adr_to_listen: ip_str = self.ip_adr_to_listen
        else:                     ip_str = "<all-on-localhost>"

        try: 
            connection.server.bind((self.ip_adr_to_listen, self.port_to_listen))
        except:
            print "Error: Cannot bind a listener to %s:%s." % (ip_str, self.port_to_listen)
            print "Error: Maybe already in use."
            return None

        # Initiate the remote process that manages the tests
        if self.script_to_start: 
            assert isinstance(self.script_to_start, (str, unicode))
            try: 
                # Tell the remote process where HWUT is listening: 
                # Command line arg: (1) ip-address, "<all-on-localhost>" for all interfaces on this PC.
                #                   (2) port number 
                subprocess.Popen([self.script_to_start, ip_str, "%s" % self.port_to_list])
            except: 
                print "Error: Hwut cannot initiate remote test agent through '%s'." % self.id
                print "Error: Failed to execute '%s'" % "".join(self.script_to_start)
                return None

        # Become a server socket
        connection.server.listen(1)
        connection.socket, \
        connection.info    = connection.server.accept()

        return connection

    def __repr__(self):
        return "".join([
            "id:               '%s';\n"      % self.id,
            "ip_adr_to_listen: '%s';\n"      % self.ip_adr_to_listen,
            "port_to_listen:   %i=0x%04X;\n" % (self.port_to_listen, self.port_to_listen),
            "script_to_start:  '%s';\n"      % self.script_to_start,
            "open:             %s;\n"        % (self._connection is not None)
        ])

