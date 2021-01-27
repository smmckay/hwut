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
import hwut.auxiliary.path as aux
import hwut.auxiliary.executer.core as executer

from hwut.strategies.core import CoreStrategy

class IndividualRunStrategy(CoreStrategy):
    def __init__(self, Setup, Program, ArgumentList, Script=""):
        assert type(ArgumentList) == list
        assert type(Program) == ""

        self.program       = Program
        self.argument_list = ArgumentList

        CoreStrategy.__init__(self, Setup)

    def do(self, element):
        argument_list = [ element.test_application_name, element.choice_name, element.protocol_file_name ]
        argument_list += self.argument_list

        executer.do([self.program] + self.argument_list)

    def is_only_database_query(self):
        return True
