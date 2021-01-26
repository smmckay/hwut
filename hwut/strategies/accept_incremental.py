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
import os
import hwut.common                as common
import hwut.auxiliary.path        as aux
import hwut.auxiliary.file_system as fs
import hwut.io.messages           as io
#
from   hwut.strategies.difference import DifferenceDisplayStrategy
from   hwut.strategies.test       import TestExecutionStrategy

class AcceptIcrementalStrategy(DifferenceDisplayStrategy):

    def __init__(self, Setup):
        DifferenceDisplayStrategy.__init__(self, Setup)

    def do(self, TestInfo):
        fs.ensure_GOOD_file_exists(TestInfo)
        DifferenceDisplayStrategy.do(self, TestInfo) 
