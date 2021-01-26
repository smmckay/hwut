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
import sys
from   hwut.temporal_logic.classes.object            import Object
from   hwut.temporal_logic.classes.statement_element import SyntaxNode, \
                                                            Fork
import hwut.temporal_logic.log as log

class Primary(SyntaxNode):
    def execute(self, world):
        assert False

class Primary_Bool(Primary):
    def __init__(self, ArgList):
        assert type(ArgList) == bool
        self.content = { "true": True, "false": False }[ArgList[0]]

    def write(self, Depth=0):
        indent = "  " * Depth
        return indent + "Primary: bool '%s'\n" % { True: "true", False: "false" }[self.content]

    def execute(self, world):
        return Object.bool(self.content, "<constant>")

class Primary_ConstantNumber(Primary):
    def __init__(self, number):
        self.content = number

    def write(self, Depth=0):
        indent = "  " * Depth
        return indent + "Primary: constant number '%f'\n" % self.content

    def execute(self, world):
        return Object.number(self.content, "<constant>")


class Primary_String(Primary):
    def __init__(self, string):
        self.content = string

    def write(self, Depth=0):
        indent = "  " * Depth
        return indent + "Primary: constant string '%s'\n" % self.content

    def execute(self, world):
        return Object.string(self.content, "<constant>")

class Primary_Event(Primary):
    def __init__(self, string):
        self.content = string

    def write(self, Depth=0):
        indent = "  " * Depth
        return indent + "Primary: event '%s'\n" % (self.content)

    def execute(self, world):
        """RETURNS: EventDbEntry

        The '.count' = 0 and '.last_time' = World.BEGIN_OF_TIME if the event
        has not yet occurred.
        """
        return world.event_db_get(self.content)

class Primary_StateTransition(Primary):
    def __init__(self, ArgList):
        self.content = (ArgList[0], ArgList[1])

    def write(self, Depth=0):
        indent = "  " * Depth
        return indent + "Primary: transition '%s->%s'\n" % (self.content[0], self.content[1])

    def execute(self, world):
        from_state_event, to_state_event = self.content
        from_state = from_state_event.content
        to_state   = to_state_event.content
        sm = world.state_machine_db.get(from_state)

        if   sm is None:                return Object.bool(False)
        elif sm.state    != to_state:   return Object.bool(False)
        elif sm.previous != from_state: return Object.bool(False)
        
        trigger_time = world.event_db[to_state].last_time
        current_time = world.time()

        return Object.bool(current_time == trigger_time)

class Primary_Variable(Primary):
    def __init__(self, string):
        self.content = string

    def write(self, Depth=0):
        indent = "  " * Depth
        return indent + "Primary: variable '%s'\n" % self.content

    def execute(self, world):
        return world.variable_access(self.content)

class Primary_CollectionMap(Primary):
    def __init__(self, ArgList):
        assert len(ArgList) == 1
        key_value_list = ArgList[0].sub_node_list
        self.content = key_value_list

    def write(self, Depth=0):
        indent = "  " * Depth
        
        txt = indent + "Primary: map\n" % self.content
        for key, value in enumerate(self.content):
            txt += indent + repr(key) + " -to->\n"
            txt += indent + value.write(Depth+1)

        return txt

    def execute(self, world):
        result = Object.map(
            (node.sub_node_list[0].execute(world).content, node.sub_node_list[1].execute(world)) 
            for node in self.content
        )
        return result

class Primary_CollectionList(Primary):
    def __init__(self, ArgList):
        assert len(ArgList) == 1
        expr_list = ArgList[0].sub_node_list

        self.content = []
        for node in expr_list:
            self.content.append(node)

    def write(self, Depth=0):
        indent = "  " * Depth
        
        txt = indent + "Primary: list\n" % self.content
        for i, value in enumerate(self.content):
            txt += indent + "[%i] -to->\n" % i
            txt += indent + value.write(Depth + 1)

        return txt

    def execute(self, world):
        return Object.list(
            element.execute(world)
            for element in self.content
        )

class Primary_FunctionDefinition(Primary):
    """Creates a user function object upon '.execute()'
    """
    def __init__(self, ArgList):
        self.argument_list = ArgList[1].sub_node_list[0].sub_node_list
        self.function_body = ArgList[2].sub_node_list

    def is_function_definition(self): 
        return True

    def prune(self):
        for i in range(len(self.argument_list)):
            self.argument_list[i] = self.argument_list[i].prune()

        self.function_body = [
            element.prune()
            for element in self.function_body
        ]
        return self

    def write(self, Depth):
        txt  = "  " * Depth + "function:\n"
        txt += "  " * Depth + "ARGUMENTS:\n"
        i = 0
        for element in self.argument_list:
            i += 1
            txt += "  " * (Depth+1) + "(%i)\n" % i
            if element is None: txt += "  " * (Depth + 1) + "None\n"
            else:               txt += element.write(Depth + 1)

        txt += "  " * Depth + "BODY:\n"
        for element in self.function_body:
            txt += element.write(Depth+1)
        return txt

    def execute(self, world):
        return Object.user_function(self.argument_list, self.function_body)

    def __repr__(self):
        return "FunctionDefinition"

class Primary_Namespace(Primary):
    def __init__(self, ArgList):
        assert len(ArgList) == 3
        assert isinstance(ArgList[1], Fork)

        self.origin           = ArgList[0]
        self.relative_namespace        = map(lambda x: x.content, ArgList[1].sub_node_list)
        if isinstance(ArgList[2], Fork): self.rule_list = ArgList[2].sub_node_list
        else:                            self.rule_list = [ ArgList[2] ]

        self.set_namespace([])

    def set_namespace(self, ParentNamespace):
        # Every rule in the rule list must be labelled with the namespace
        for rule in self.rule_list:
            rule.set_namespace(ParentNamespace + self.relative_namespace)

    def write(self, Depth):
        indent = "  " * Depth
        txt  = indent + "Primary_Namespace: %s\n" % repr(self.relative_namespace)

        dummy = copy(self.parent_namespace)
        dummy.reverse()
        for name in dummy:
            txt += indent + "  in %s\n" % name 

        for rule in self.rule_list:
            txt += rule.write(Depth + 1)
        return txt

    def prune(self):
        for i in range(len(self.rule_list)):
            self.rule_list[i] = self.rule_list[i].prune()
        return self

    def execute(self, world):
        raise "Namespaces cannot be executed 'just like that'. See file 'engine.py'"

