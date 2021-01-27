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
from hwut.temporal_logic.classes.object            import Object

class Control_SwitchCase(SyntaxNode, SourceCodeOrigin):
    def __init__(self, ArgList):
        assert len(ArgList) == 3
        self.comparator     = ArgList[0].content
        self.compared_term  = ArgList[1]
        self.triggered_expr = ArgList[2]

    def prune(self):
        self.compared_term  = self.compared_term.prune()
        self.triggered_expr = self.triggered_expr.prune()
        return self

    def write(self, Depth):
        indent = "  " * Depth
        txt =  indent + "CASE: Comparator %s\n" % self.comparator
        txt += indent + "TERM:\n"
        txt += self.compared_term.write(Depth+1)
        txt += indent + "ACTION:\n"
        txt += self.triggered_expr.write(Depth+1)
        return txt


    def match_key(self, Key, world):
        term = self.compared_term.execute(world)
        return {"<":  lambda a, b: a < b,
                "<=": lambda a, b: a <= b,
                "==": lambda a, b: a == b,
                "!=": lambda a, b: a != b,
                ">=": lambda a, b: a >= b,
                ">":  lambda a, b: a > b,
               }[self.comparator](Key.content, term.content)

    def execute(self, world):
        return self.triggered_expr.execute(world)

class Control_Switch(SyntaxNode, SourceCodeOrigin):
    def __init__(self, ArgList):
        assert len(ArgList) == 3
        SourceCodeOrigin.__init__(self, ArgList[0])
        self.switch_key  = ArgList[1]
        self.case_list   = []
        self.else_case   = None
        for node in ArgList[2].sub_node_list:
            if node.__class__ == Control_SwitchCase: self.case_list.append(node)
            else:                                    self.else_case = node

    def write(self, Depth):
        indent = "  " * Depth
        txt =  indent + "Switch:\n"
        for case in self.case_list:
            txt += case.write(Depth+1)
        if self.else_case is not None:
            txt += self.else_case(Depth+1)
        txt += self.loop_body.write(Depth + 1)
        return txt

    def prune(self):
        self.switch_key = self.switch_key.prune()
        for i in range(len(self.case_list)):
            self.case_list[i] = self.case_list[i].prune()
        if self.else_case is not None:
            self.else_case = self.else_case.prune()
        return self

    def execute(self, world):
        # Execute the expression that 'brings' the collection
        key = self.switch_key.execute(world)

        # Go through the set of conditions and find the first that matches
        for case in self.case_list:
            if case.match_key(key, world): 
                return case.execute(world)
        else:
            # If no case triggered we perform the else case
            if self.else_case is not None: return self.else_case.execute(world)
            else:                      return Object.bool(True) # No conditions, no objections

class Control_ForLoop(SyntaxNode, SourceCodeOrigin):
    def __init__(self, ArgList):
        assert len(ArgList) == 4
        SourceCodeOrigin.__init__(self, ArgList[0])
        self.iterator_name   = ArgList[1].content
        self.collection_expr = ArgList[2]
        self.loop_body       = ArgList[3]

    def write(self, Depth):
        indent = "  " * Depth
        txt =  indent + "Control ForLoop:\n"
        txt += indent + "  FOR %s in:\n" % self.iterator_name
        txt += self.collection_expr.write(Depth + 1)
        txt += indent + "  DO:\n"
        txt += self.loop_body.write(Depth + 1)
        return txt

    def prune(self):
        self.collection_expr = self.collection_expr.prune()
        self.loop_body       = self.loop_body.prune()
        return self

    def execute(self, world):
        # Execute the expression that 'brings' the collection
        collection = self.collection_expr.execute(world)

        # Iterate over the collection
        if collection.type == Object.LIST: 
            iterable = collection.content
        elif collection.type == Object.MAP: 
            iterable = (Object.from_string_or_number(x) for x in collection.content.iterkeys())
        else:
            print "## Expression in 'for in' construct does not result in collection."
            print "## Iterations can only happen over collections."
            return Object.bool(False)

        verdict_f = True
        for element in iterable:
            # Assign the value to the loop variable (iterator)
            world.object_db[self.iterator_name] = element
            # Execute the loop body
            if self.loop_body.execute(world) == False: verdict_f = False

        return Object.bool(verdict_f)

class Control_IfElse(SyntaxNode):
    def __init__(self, ArgList):
        assert len(ArgList) in [3, 4]
        SyntaxNode.__init__(self, ArgList[0])
        self.condition = ArgList[1]
        self.then_part = ArgList[2]
        if len(ArgList) == 4: self.else_part = ArgList[3]
        else:                 self.else_part = None

    def write(self, Depth):
        indent = "  " * Depth
        txt  = indent + "Control IfElse:\n"
        txt += indent + "  IF:\n"
        txt += self.condition.write(Depth + 1)
        txt += indent + "  THEN:\n"
        txt += self.then_part.write(Depth + 1)
        if self.else_part is not None: 
            txt += indent + "  ELSE:\n"
            txt += self.else_part.write(Depth + 1)
        return txt

    def prune(self):
        self.condition = self.condition.prune()
        self.then_part = self.then_part.prune()
        if self.else_part is not None: self.else_part = self.else_part.prune()
        return self

    def execute(self, world):
        """If the condition is true one basic rule is to be applied, if it false, then 
           we apply another basic rules.
        """
        condition = self.condition.execute(world).content
        if condition:                    return self.then_part.execute(world)
        elif self.else_part is not None: return self.else_part.execute(world)
        else:                            return Object.bool(True)
    


