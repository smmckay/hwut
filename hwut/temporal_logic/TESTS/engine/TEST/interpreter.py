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
#! /usr/bin/env python
import os
import sys
hwut_path = os.environ["HWUT_PATH"]
sys.path.append(hwut_path)
from StringIO import StringIO

import hwut.io.messages             as io
import hwut.temporal_logic.engine as engine
import hwut.temporal_logic.log    as log

case = os.path.basename(sys.argv[1]).replace(".evt", "")

if "--hwut-info" in sys.argv:
    print "%s;" % case
    # print "CHOICES: FromTo, IfElse, IfElse-2, IfElifElse, IfElifElse-2, IfElifElse-3, OnTrigger, OnTrigger-2, OnTrigger-Condition, Freeze, Freeze-2, Freeze-3, Freeze-4, FunctionActive, FunctionPassive, List, Map, Maps-2, Import, Import-2, ForIn, Switch, state_machine;" 
    print "HAPPY: \.tlr:[0-9]+:;"
    sys.exit()

rule_file_name  = "rules/%s.tlr"  % case
event_file_name = "%s.evt" % case
print event_file_name


result = engine.do(rule_file_name, open(event_file_name, "rb"), sys.stdout)
print "result =", result 

