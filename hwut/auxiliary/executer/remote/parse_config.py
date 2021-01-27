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
import hwut.io.mini_fly                                as     fly
from   hwut.auxiliary.executer.remote.socket_interface import ConfigurationSocket

from   StringIO import StringIO

connection_type_db = {
    "socket": ConfigurationSocket,
}

def do(Text):
    fh = StringIO(Text)

    config = parse_type_and_id(fh)
    if config is None: return None

    while 1 + 1 == 2:
        label = fly.read_label(fh)
        if label is None: break
        value = fly.read_string_trivial(fh)
        if value is None: break

        config.set_parameter(label, value)

    return config

def parse_type_and_id(fh):
    connection_type = fly.read_label(fh)
    if connection_type is None: 
        print "Error: missing remote connection type identifier." 
        print "Error: syntax is"
        print "Error:   --remote 'type: id;' list-of('name: value' pairs)"
        print "Error: Example:"
        print "Error:   --remote socket: my-socket; ip: localhost; port: 37773; start: init-remote.sh; "
        return None

    if connection_type not in connection_type_db: 
        print "Error: connection type '%s' unknown to hwut." % connection_type
        return None

    connection_id = fly.read_string_trivial(fh)

    return connection_type_db[connection_type](ConnectionId=connection_id)
    



