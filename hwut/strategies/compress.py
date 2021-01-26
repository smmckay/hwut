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
import tarfile

class CompressStrategy(CoreStrategy):
    def __init__(self, Setup):

        CoreStrategy.__init__(self, Setup)
        pass

    def _start_directory(self, TestSequence):
        """Clean is a special strategy. It does not do any test, but only searches
           for files that are unrelated to test cases. Then these files are deleted.
           The CleanStrategy raises then the 'break_up_f' flag. Thus, 'do()' never
           executed.
        """
        self.__break_up_f = True

        file_list = aux.get_hwut_related_files(self._current_dir)

        for file in file_list:
            archive.add(file)

    def do(self, element):
        assert 1 + 1 == 3, \
               "CleanStrategy.do() should never be executed, because the break_up_f is set in .start()"

