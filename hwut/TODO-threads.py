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
# (C) 2007-2014 Frank-Rene Schaefer
import hwut.common         as common
import hwut.io.messages    as io
import hwut.auxiliary.path as aux
import hwut.auxiliary.make as make
#
import threading
import os
import sys


TestThread_currently_running_n = -1


class TestThread(threading.Thread):
    def __init__(self, TestInfo, CreateOnlyOutputF):
        assert TestInfo.choice == "" or TestInfo.description.result_list

        self.test_info            = TestInfo
        self.create_only_output_f = CreateOnlyOutputF
        self.result_f             = False

        return threading.Thread.__init__(self)

    def run(self):
        is_group_element_f = self.test_info.group != ""
        io.on_test_start(self.test_info, is_group_element_f, "")

        if self.test_info.present_f: 
            self.result_f = test_executer.do(self.test_info, self.create_only_output_f) 
            result = convert_to_string_result(self.result_f) 
        else:
            result = "MAKE FAILED"

        self.test_info.description.results[self.test_info.choice_index()] = result

        io.on_test_end(self.test_info, result)


