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
from hwut.temporal_logic.classes.statement_element import SyntaxNode
from   hwut.temporal_logic.classes.object          import Object

class TimeSpan(SyntaxNode):

    def is_sleeping_at_begin(self):
        return False

    def check_awake_condition(self, world):
        return self.x_check_awake_condition(world).content

    def check_sleep_condition(self, world):
        return self.x_check_sleep_condition(world).content

class TimeSpan_FromTo(TimeSpan):
    def __init__(self, ArgList):
        assert len(ArgList) == 2
        self.awake_condition = ArgList[0]
        self.sleep_condition = ArgList[1]

    def write(self, Depth):
        indent = "  " * Depth
        txt  = indent + "TimeSpan:\n"
        txt += indent + "  FROM\n"
        txt += self.awake_condition.write(Depth + 1)
        txt += indent + "  TO\n"
        txt += self.sleep_condition.write(Depth + 1)
        return txt

    def is_sleeping_at_begin(self):
        return True

    def x_check_awake_condition(self, world):
        return self.awake_condition.execute(world)
    
    def x_check_sleep_condition(self, world):
        return self.sleep_condition.execute(world)

    def prune(self):
        self.awake_condition = self.awake_condition.prune()
        self.sleep_condition = self.sleep_condition.prune()
        return self

class TimeSpan_From(TimeSpan):
    def __init__(self, ArgList):
        assert len(ArgList) == 1
        self.condition = ArgList[0]

    def write(self, Depth):
        indent = "  " * Depth
        txt  = indent + "TimeSpan:\n"
        txt += indent + "  FROM\n"
        txt += self.condition.write(Depth + 1)
        return txt

    def is_sleeping_at_begin(self):
        return True

    def x_check_awake_condition(self, world):
        """Sleeping from the very first beginning then, after the condition triggered 
           it never sleeps again. The related condition must initialy be set 'sleep'.
        """
        return self.condition.execute(world)

    def x_check_sleep_condition(self, world):
        return Object.bool(False)

    def prune(self):
        self.condition = self.condition.prune()
        return self

class TimeSpan_To(TimeSpan):
    def __init__(self, ArgList):
        assert len(ArgList) == 1
        self.condition = ArgList[0]

    def write(self, Depth):
        indent = "  " * Depth
        txt  = indent + "TimeSpan:\n"
        txt += indent + "  TO\n"
        txt += self.condition.write(Depth + 1)
        return txt
    
    def is_sleeping_at_begin(self):
        return False

    def x_check_awake_condition(self, world):
        """Awake from the very first beginning then, after the condition triggered 
           it never wakes up again. The related condition must initialy be set 'awake'.
        """
        return Object.bool(False)

    def x_check_sleep_condition(self, world):
        return self.condition.execute(world)

    def prune(self):
        self.condition = self.condition.prune()
        return self

