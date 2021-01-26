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
from hwut.temporal_logic.classes.statement_element import SyntaxNode, Fork
from hwut.temporal_logic.classes.object            import Object, FunctionObject

class Action_OpBase(SyntaxNode):
    """A Action_OpBase stores information about a function call to be performed. 
       For this, it contains:

        -- a string with the function's name
        -- a list of expressions which will later on evaluate to real objects
           that are passed as arguments to the function.

       A Action_OpBase lives in a syntax/parse tree as a syntax element.
    """
    def __init__(self, FunctionName, ArgumentList=None):
        assert type(FunctionName) == str
        self.__operation_name = FunctionName
        self._argument_list  = ArgumentList

    def set_argument_list(self, ArgumentList):
        # Argument list shall not be set twice
        assert self._argument_list is None
        self._argument_list = ArgumentList
        if self._argument_list is None:
            return

        for arg in self._argument_list:
            if isinstance(arg, Fork): arg.disallow_reduction_to_single()

    def prune(self):
        for i in range(len(self._argument_list)):
            if self._argument_list[i] is not None:
                self._argument_list[i] = self._argument_list[i].prune()
            
        return self

    def write(self, Depth=0):
        indent = "  " * Depth
        txt =  indent + "Operation %s(\n" % self.__operation_name
        for expr in self._argument_list:
            txt += expr.write(Depth + 1)
        txt += indent + ")\n"
        return txt

    def execute(self, world, the_self=None):
        """In case of member functions the reference to the object under concern
        is given by 'the_self'. It is passed to the functions as the first 
        argument. Normal global functions do not use 'the_self'.
        """

        argument_instance_list = self.intantiate_arguments(world, the_self)

        op                     = self.get_operation(world, argument_instance_list)
        if op is None:
            return Object.bool(False, "missing function or overload")
        
        result = op.do(world, argument_instance_list)
        if False:
            print "#operation_name:", self.__operation_name
            print "#RESULT:", result
        assert isinstance(result, Object)
        return result

    def intantiate_arguments(self, world, the_self):
        """Execute whatever is to be executed to instantiate the list of 
        arguments. 
        """
        if False:
            print "#ARGUMENT_LIST", self.__operation_name
            for i, arg in enumerate(self._argument_list):
               print "# [%i]:" % i, arg.write(1)

        result = [
            argument.execute(world) for argument in self._argument_list
        ]

        if the_self is not None:
            result.insert(0, the_self)
        
        if False:
            print "#ARGUMENT_INSTANCE_LIST", self.__operation_name
            for i, arg in enumerate(result):
               print "# [%i]:" % i, str(arg)
        return result
        
    def get_operation(self, world, ArgumentInstanceList):
        """RETURNS: function pointer that fits the types of the 
                    'ArgumentInstanceList'.
        """
        # -- Access the function
        operation = world.object_db.get(self.__operation_name)
        if operation is None:
            print "Error: operator '%s' not defined. " % self.__operation_name
            return None

        # -- Call
        if type(operation.content) != list:
            # One distinct function
            return operation.content

        # Overloaded function: select function by argument list type
        for overload in operation.content:
            if overload.check_argument_types(ArgumentInstanceList): 
                return overload

        # No fitting overload found
        print "Error: no matching overload."
        print "Error: ", [ x.type for x in ArgumentInstanceList ] 
        return None


class Action_OpCall(Action_OpBase):
    def __init__(self, ArgList):
        argument_list = ArgList[0].sub_node_list[0].sub_node_list
        Action_OpBase.__init__(self, "call", argument_list)
        
    def execute(self, world, the_self):
        """In case of member functions the reference to the object under concern
        is given by 'the_self'. It is passed to the functions as the first 
        argument. Normal global functions do not use 'the_self'.
        """
        if isinstance(the_self, FunctionObject):
            pass
        elif isinstance(the_self, Object) and the_self.type == Object.FUNCTION:
            the_self = the_self.content
        else:
            print "Error: Call to something which is not a function. Found: %s" % the_self.type
            return None

        argument_instance_list = [
            argument.execute(world) for argument in self._argument_list
        ]

        return the_self.do(world, argument_instance_list)


class Action_Op(Action_OpBase):
    def __init__(self, ArgList):
        if type(ArgList) == list: 
            assert len(ArgList) == 2
            name          = ArgList[0].content
            argument_list = ArgList[1].sub_node_list[0].sub_node_list
        else:
            name          = ArgList
            argument_list = None

        Action_OpBase.__init__(self, name, argument_list)

class Action_BinaryOp(Action_OpBase):
    def __init__(self, ArgList):
        assert len(ArgList) == 3
        operation_name = ArgList[1].content
        Action_OpBase.__init__(self, operation_name, [ArgList[0], ArgList[2]])

