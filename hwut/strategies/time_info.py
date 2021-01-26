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
import hwut.common as common
from   hwut.strategies.core import CoreStrategy

class TimeInfo:
    def __init__(self):
        self.make    = 0.0  # Time to make test applications
        self.execute = 0.0  # Time to run test applications

    def add(self, ExeTime, MakeTime):
        if ExeTime is not None:  self.execute += ExeTime
        if MakeTime is not None: self.make    += MakeTime

    def add_other(self, Other):
        self.execute += Other.execute
        self.make    += Other.make

class TimeInfoStrategy(CoreStrategy):
    def __init__(self, Setup):
        CoreStrategy.__init__(self, Setup)
        self.__time_result_db = []
        self.__total          = TimeInfo()

    def _start_directory(self, TestSequence):
        self.__current = TimeInfo()

    def do(self, Element):
        """NOTE: The printout already happens by the hwut.core framework,
                 so there is not much to be done here.
        """
        suppress_application_name_f = False 
        make_time    = 0.0
        execute_time = 0.0
        if Element.choice_index() == 0 and Element.description.make_dependent_f(): 
            io.print_make_time(Element)
            make_time                   = Element.description.make_time_sec()
            suppress_application_name_f = True

        io.print_test_time(Element, suppress_application_name_f)

        self.__current.add(Element.result().time_to_execute_sec, 
                           make_time)

        return Element.result()

    def _end_directory(self):
        self.__time_result_db.append([self._current_dir, self.__current])
        self.__total.add_other(self.__current) 

        io.print_total_time(self._current_dir, self.__current.execute, self.__current.make)

        self.directory = os.devnull

    def _end_directory_tree(self):
        io.print_time_summary(self.__time_result_db)

    def xml_database_write_permission(self):
        return False

    def is_only_database_query(self):
        return True

    def get_referred_date(self):
        """In the info strategy the date is printed, when the test results were safed.
        """
        return "<no date>"
