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
import hwut.auxiliary.path as aux
import hwut.auxiliary.executer as executer

from   hwut.strategies.core import CoreStrategy

import os

class RunStrategy(CoreStrategy):
    def __init__(self, Setup, Program, ArgumentList, Script=""):
        assert type(ArgumentList) == list
        assert type(Program) == str

        # If the program is accessible based on its path-name and the current
        # directory, then make it available with an absolute path. This way, it 
        # is call-able from any directory.
        if os.access(Program, os.F_OK):
            self.program = os.path.abspath(os.path.normpath(Program))
        else:
            self.program = Program
        
        self.argument_list = ArgumentList

        CoreStrategy.__init__(self, Setup)
        self.set_warn_if_no_test_application_found(False)

    def execution_name(self):
        result = "".join("%s " % x for x in [self.program] + self.argument_list)
        result = result.strip()
        if len(result) > 32: 
            result = "%s..." % result[:29] 
        return result

    def _start_directory(self, TestSequence):
        """Clean is a special strategy. It does not do any test, but only searches
           for files that are unrelated to test cases. Then these files are deleted.
           The CleanStrategy raises then the 'break_up_f' flag. Thus, 'do()' never
           executed.
        """
        command_line = [self.program] + self.argument_list
        executer.do(command_line)

        # ensure that .do() is not called for single test elements
        self.set_break_up_request()

    def do(self, element):
        assert 1 + 1 == 3, \
               "RunStrategy.do() should never be executed, because the break_up_f is set in .start()"

    def is_only_database_query(self):
        return True
