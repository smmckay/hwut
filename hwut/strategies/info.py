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
import os
import hwut.io.messages as io
import hwut.common      as common
from   hwut.strategies.test import TestExecutionStrategy

class InfoStrategy(TestExecutionStrategy):
    def __init__(self, Setup):
        TestExecutionStrategy.__init__(self, Setup)

    def verdict_get(self, TestInfo):
        """Here is the big difference to 'TestExecutionStrategy': The test is
        not executed, but only the result is read out.
        """
        return TestInfo.result().verdict

    def coverage_analysis_on_test_done(self, TestInfo):
        pass

    def coverage_analysis_on_directory_tree_done(self):
        pass

    def xml_database_write_permission(self):
        return False

    def is_only_database_query(self):
        return True

    def get_referred_date(self):
        """In the info strategy the date is printed, when the test results were safed.
        """
        return "<no date>"
