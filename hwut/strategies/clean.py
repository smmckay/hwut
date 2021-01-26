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
import hwut.auxiliary.file_system as fs
import hwut.auxiliary.path        as aux
import hwut.io.messages           as io
import hwut.io.select             as select

import os

from hwut.strategies.core import CoreStrategy

class CleanStrategy(CoreStrategy):
    def __init__(self, Setup):
        assert Setup.grant in ["ALL", "NONE", "INTERACTIVE"]

        self.grant = Setup.grant

        self.__to_be_deleted_file_list = []

        CoreStrategy.__init__(self, Setup)

    def _start_directory(self, TestSequence):
        """Clean is a special strategy. It does not do any test, but only searches
           for files that are unrelated to test cases. Then these files are deleted.
           The CleanStrategy raises then the 'break_up_f' flag. Thus, 'do()' never
           executed.
        """
        # ensure that .do() is not called for single test elements
        self.set_break_up_request()

        file_list = aux.get_hwut_unrelated_files()
        self.__to_be_deleted_file_list.extend(
            os.path.normpath("%s/%s" % (self._current_dir, f)) 
            for f in file_list
        )

    def do(self, element):
        assert 1 + 1 == 3, \
               "CleanStrategy.do() should never be executed, because the break_up_f is set in .start()"

    def _end_directory_tree(self):

        if self.grant == "INTERACTIVE":
            index_list = select.request_file_list_deletion(os.getcwd(), self.__to_be_deleted_file_list)
        elif self.grant == "ALL":
            index_list = range(len(self.__to_be_deleted_file_list))
        else:
            io.on_clean_no_files_to_delete(self.__to_be_deleted_file_list)
            index_list = []

        for index in index_list:
            file_name = self.__to_be_deleted_file_list[index]
            # os.remove(file_name)
            io.on_file_deleted(file_name)

        return

    def is_only_database_query(self):
        return True

