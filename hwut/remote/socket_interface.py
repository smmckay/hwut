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
import socket
import time

import hwut.remote.core as core

class RemoteExecuter(core.RemoteExecuter):
    """Implements a remote execution on socket basis.
    """
    def __init__(self, Spy, Agent):
        TxHost           = self._extract(Agent, "Adr",         None)
        TxPort           = self._extract(Agent, "Port",        37773)
        remote_path      = self._extract(Agent, "Path",        "")
        RxHost           = self._extract(Spy,   "Adr",         "")
        RxPort           = self._extract(Spy,   "Port",        37773)
        RxTerminationStr = self._extract(Spy,   "Terminator",  "<<end>>")
        RxPackageSize    = self._extract(Spy,   "PackageSize", 4096)

        sender   = socket_interface.Sender(TxHost, TxPort)
        receiver = socket_interface.Receiver(RxHost, RxPort, 
                                             RxTerminationStr, RxPackageSize)

        RemoteExecuter.__init__(sender, receiver, remote_path)


class Sender(core.Sender):
    def __init__(self, Host, Port):
        assert Host is not None
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((Host, Port))
    def send(self, Content):
        self.__socket.send(Content)
    def close(self):
        self.__socket.close()

class Receiver(core.Receiver):
    def __init__(self, Host, Port, PackageSize=4096):
        """NOTE: You may use Host="" to signify 'any incoming host."""
        self.__package_size = PackageSize
        self.__socket       = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((Host, Port))
        self.__socket.listen(1)
        self.__connection = None

    def receive_init(self):
        self.__connection, addr = self.__socket.accept()

    def receive_chunk(self):
        """RETURNS: None -- if reception failed to receive anything.
                    Data -- if there was data of length > 0
        """
        try: 
            data = self.__connection.recv(self.__package_size)

        except Exception, x:
            return None

        if not data: return None

        return data

    def close(self):
        self.__connection.close()

if __name__ == "__main__":
    import sys
    if sys.argv[1] == "rx":
        print Receiver("", 37773).do()
    else:
        Sender("192.168.1.11", Port=37773).do(sys.argv[1])

