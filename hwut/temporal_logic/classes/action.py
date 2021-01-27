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
from   hwut.temporal_logic.classes.statement_element import SyntaxNode
from   hwut.temporal_logic.classes.object            import Object    
from   hwut.temporal_logic.classes.primary           import Primary, Primary_Event
import hwut.temporal_logic.log                       as     log

class Action_ObjectAccess(SyntaxNode):
    """Based on a 'root' object a sequence of 'accesses' is applied. The 'root' 
    is the first 'self', then the 'self' is the result of an accesses, then the 
    next access is applied on the new self, resulting in again a new self, etc.

    EXAMPLE:   "x[12].record_list[2]"

        root = 'x'

        (0) self     = root

        (1) new_self = access('get element 12' of self)
            self     = new_self
        (2) new_self = access('get member 'record_list' of self)
            self     = new_self
        (3) new_self = access('get element 2' of self)
        
        Result: new_self 
    """
    def __init__(self, ArgList):
        assert len(ArgList) == 2
        self.root_object = ArgList[0]
        if len(ArgList[1]) != 0: self.access_list = ArgList[1]
        if len(ArgList[1]) == 0: self.access_list = None

    def write(self, Depth=0):
        indent = "  " * Depth
        if self.access_list is not None:
            access_str = "".join(
                access.write(0)
                for access in self.access_list
            )
            return "%sAccess %s: %s" % (indent, self.root_object.write(0), access_str)
        else:
            return "%sAccess %s" % (indent, self.root_object.write(0))

    def prune(self):
        if self.access_list is not None:
            self.access_list = [ access.prune() for access in self.access_list ]
        return self

    def execute(self, world):
        the_self = self.root_object.execute(world)

        if self.access_list is not None:
            for access in self.access_list:
                the_self = access.execute(world, the_self)

        return the_self

class Action_Print(SyntaxNode):
    def __init__(self, ArgList):
        SyntaxNode.__init__(self, ArgList[0]) # [0] = SourceCodeOrigin
        self.term_list     = ArgList[1].sub_node_list
        self.term_list_str = ""

    def is_log_command(self):
        return True

    def set_original_str(self, OriginalStr):
        self.term_list_str = OriginalStr

    def write(self, Depth):
        indent = "  " * Depth
        txt = indent + "print [%s]\n" % "".join(str(x) for x in self.term_list_str)
        # txt += indent + "  LOG <%s>\n" % self.numeric_term_str
        # txt += self.numeric_term.write(Depth + 1)
        return txt

    def prune(self):
        return self

    def execute(self, world):
        time_space = " " * len("%f" % world.time())
        print_str  = "".join((x.execute(world).plain_string() 
                             for x in self.term_list))
        log.log_this("%s: << %s >>\n" % (time_space, print_str))
        return Object.bool(True)

class Action_ConditionTest(SyntaxNode):
    def __init__(self, ArgList):
        assert len(ArgList) == 2
        SyntaxNode.__init__(self, ArgList[0])  # [0] = SourceCodeOrigin
        self.condition = ArgList[1]

    def write(self, Depth):
        indent = "  " * Depth
        txt =  indent + "Condition:\n"
        txt += self.condition.write(Depth + 1)
        return txt

    def prune(self):
        self.condition = self.condition.prune()
        return self.condition

    def execute(self, world):
        result = self.condition.execute(world)
        ## print "##callstack:" 
        ## for i in range(100):
        ##    try:
        ##       frame = sys._getframe(i).f_code
        ##       print "## <--", frame.co_filename, frame.co_firstlineno
        ##    except: break
        return result

class Action_DefineStateMachine(SyntaxNode):
    def __init__(self, ArgList):
        assert len(ArgList) == 2
        SyntaxNode.__init__(self, ArgList[0])  # [0] = SourceCodeOrigin
        self.event_name_list = ArgList[1]

    def is_state_machine_definition(self): 
        return True

    def write(self, Depth):
        indent = "  " * Depth
        return indent + "StateMachine: [%s]" % "".join("%s, " % name in self.event_name_list)

    def prune(self):
        return self

    def execute(self, world):
        world.register_state_machine(self.event_name_list, self.source_code_origin)
        ## print "##callstack:" 
        ## for i in range(100):
        ##    try:
        ##       frame = sys._getframe(i).f_code
        ##       print "## <--", frame.co_filename, frame.co_firstlineno
        ##    except: break
        return True

