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
import time
import os

import hwut.auxiliary.path as aux
from   hwut.strategies.core import CoreStrategy

class CollectDataForTreeDisplay(CoreStrategy):

    def __init__(self, Setup, test_db):
        self.__test_db = test_db
        CoreStrategy.__init__(self, Setup)

    def do(self, Element):
        assert Element.__class__ == Test

        total_path  = self._current_dir  + "/"
        total_path += Element.file_name() + "/"
        if Element.choice() == "": total_path += "/-no-choice-"
        else:                      total_path += Element.choice()
        total_path  = os.path.normpath(total_path)

        self.__test_db[total_path] = Element
        return Element.last_result()

    def is_only_database_query(self):
        return True

