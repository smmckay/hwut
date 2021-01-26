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
import sys
import os
import binascii

from   hwut.strategies.core  import CoreStrategy

import hwut.auxiliary.path          as aux
import hwut.common             as common
import hwut.io.messages        as io
import hwut.auxiliary.make               as make

import hwut.verdict.comparison    as comparison
import hwut.temporal_logic.engine as temporal_logic
import hwut.temporal_logic.log    as log

from   StringIO import StringIO

class LogicDisplayStrategy(CoreStrategy):

    def __init__(self, Setup, CreateOnlyOutputF=False):
        self.create_only_output_f = CreateOnlyOutputF
        self.directory            = os.devnull
        CoreStrategy.__init__(self, Setup)

    def do(self, TestInfo):
        if TestInfo.description.temporal_logic_f() == False: 
            return "NO LOGIC"

        fh_output, execution_time = TestInfo.execute()
    
        for i, logic_file in enumerate(TestInfo.description.temporal_logic_rule_file_list()):
            sub_result = temporal_logic.do(logic_file, fh_output, LogSH=sys.stdout)
            if sub_result != "OK": return sub_result

        return "OK" # Nothing went wrong => Oll Korrekt
                
