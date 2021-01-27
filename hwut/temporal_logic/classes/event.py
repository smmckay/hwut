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
from hwut.temporal_logic.classes.statement_element import SyntaxNode, SourceCodeOrigin
from hwut.temporal_logic.classes.world             import Event
from hwut.temporal_logic.classes.object            import Object

# NOTE: These here are 'event triggers', i.e. something like commands rather
#       than data carriers. When they are executed, they enter an event in the
#       current state database.

class EventTrigger_Adornment(SyntaxNode):
    def __init__(self, ArgList):
        assert len(ArgList) in [1, 2]

        if len(ArgList) == 2: 
            Arg1 = ArgList[0].content
            Arg2 = ArgList[1]
        else:
            Arg1 = ArgList[0]
            Arg2 = None

        if Arg2 is None:
            self.__name  = ""
            self.__term = Arg1
        else:
            self.__name = Arg1
            self.__term = Arg2

    def write(self, Depth, Index=0):
        if self.__name != "": txt = " " * Depth + "[%i] %s =" % (Index, self.__name) 
        else:                 txt = " " * Depth + "[%i] =" % Index 
        txt += "\n" + " " * Depth + self.__term.write(Depth+1)
        return txt

    def prune(self):
        self.__term = self.__term.prune()
        return self

    def name(self): 
        return self.__name

    def execute(self, world):
        result = self.__term.execute(world)
        return Object(result.type, result.content, self.__name)
        
class EventTrigger(SyntaxNode):
    def __init__(self, ArgList): # SourceOrigin, event_name, adornment_expr_list):
        SyntaxNode.__init__(self, ArgList[0])
        self.event_name = ArgList[1].content
        if len(ArgList) == 3:
            self.adornment_expr_list = ArgList[2].sub_node_list[0].sub_node_list
            for x in self.adornment_expr_list:
                assert x.__class__ == EventTrigger_Adornment
        else:
            self.adornment_expr_list = []

    def write(self, Depth=0, TypeNameF=True):
        indent = "  " * Depth
        if TypeNameF: txt = indent + "Event: %s\n" % self.event_name
        else:         txt = self.event_name + "\n"
        index = -1
        for adornment in self.adornment_expr_list:
            index += 1
            txt += indent + "   " + adornment.write(Depth + 1, index)
        return txt

    def pretty_string(self):
        #if self.adornment_instance_list == []: opening_bracket_str = ""; closing_bracket_str = ""
        #else:                                  opening_bracket_str = "("; closing_bracket_str = ")"
        txt = "Event: %s%s" % (self.event_name, opening_bracket_str)
        #for result in self.adornment_instance_list:
        #    txt += "%s=%s, " % (result.name, repr(result.value))
        #if len(self.adornment_instance_list) != 0: txt = txt[:-2]
        txt += closing_bracket_str
        return txt

    def prune(self):
        for i in range(len(self.adornment_expr_list)):
            self.adornment_expr_list[i] = self.adornment_expr_list[i].prune()
        return self

    def execute(self, world):
        adornment_instance_list = [
            expr.execute(world) for expr in self.adornment_expr_list
        ]
        return Event(self.event_name, adornment_instance_list)

class EventTrigger_List(SyntaxNode):
    def __init__(self, ArgList): # SourceOrigin, event_trigger_list):
        assert len(ArgList) >= 2
        SyntaxNode.__init__(self, ArgList[0])
        self.event_trigger_list = ArgList[1]

    def write(self, Depth):
        indent = "  " * Depth
        txt  = indent + "EventTrigger_List:\n"
        i = 0
        for event in self.event_trigger_list:
            i += 1
            txt += indent + "  (%i) " % i 
            txt += event.write(Depth + 1)[(Depth + 1)*2:]
        return txt

    def prune(self):
        # NOTE: Statements should not prune itself off, otherwise a new list would have to be built.
        for event_trigger in self.event_trigger_list:
            event_trigger.prune()
        return self

    def execute(self, world):
        return [ event.execute(world) for event in self.event_trigger_list ]




