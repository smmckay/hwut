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
from   copy import deepcopy, copy
from   itertools import izip

class Object(object):
    VOID     = "void"
    FUNCTION = "function"
    BOOL     = "bool"
    NUMBER   = "number"
    STRING   = "string"
    LIST     = "list"
    MAP      = "map"

    NAME_ANONYMOUS = "<anonymous>"

    __slots__ = ("type", "content", "name", "default_value")

    def __init__(self, Type, Content=None, Name="<anonymous>"):
        assert not isinstance(Content, Object)
        self.type          = Type
        self.content       = Content
        self.name          = Name
        self.default_value = None
    
    @staticmethod
    def void(Name="<anonymous>"):        
        return Object(Object.VOID, None, Name)
    @staticmethod
    def bool(X, Name="<anonymous>"):     
        assert type(X) == bool
        return Object(Object.BOOL, X, Name)
    @staticmethod
    def number(X, Name="<anonymous>"):   
        return Object(Object.NUMBER, X, Name)
    @staticmethod
    def string(X, Name="<anonymous>"):   
        assert isinstance(X, (str, unicode))
        return Object(Object.STRING, X, Name)
    @staticmethod
    def function(X, Name="<anonymous>"): 
        return Object(Object.FUNCTION, X, Name)
    @staticmethod
    def user_function(ArgumentList, Body, Name="<anonymous>"): 
        return Object(Object.FUNCTION, FunctionObjectUser(ArgumentList, Body), Name)
    @staticmethod
    def from_string_or_number(X, Name="<anonymous>"): 
        if   isinstance(X, (int, float, long)): return Object.number(X, Name)
        elif isinstance(X, (str, unicode)):     return Object.string(X, Name)
        else:                                   assert False
    @staticmethod
    def convert_to_bool(X):
        if not X.content or X.type == Object.VOID: return Object.bool(False)
        else:                                      return Object.bool(True)
    @staticmethod
    def map(Iterable, Name="<anonymous>", DefaultValue=None):
        content = dict((key, value) for key, value in Iterable)
        result = Object(Object.MAP, content, Name) 
        result.default_value = DefaultValue
        return result
    @staticmethod
    def list(Iterable, Name="<anonymous>", DefaultValue=None):
        content = list(element for element in Iterable)
        result = Object(Object.LIST, content, Name) 
        result.default_value = DefaultValue
        return result

    def size(self):
        if self.type not in (Object.LIST, Object.MAP):
            print "Error: Object of type %s does not have a member '.size'" % self.type
        return Object.number(len(self.content))

    def delete(self, Key):
        if self.type == Object.LIST:
            if Key.type == Object.NUMBER: deletion_key = int(Key.content)
            else:
                print "Error: Deletion keys must be numbers. found: %s" % str(Key)
            if deletion_key >= 0 or deletion_key < len(Key.content): 
                del self.content[deletion_key]

        elif self.type == Object.MAP:
            if   Key.type == Object.NUMBER: deletion_key = int(Key.content)
            elif Key.type == Object.STRING: deletion_key = Key.content
            else:
                print "Error: Deletion keys must be numbers or strings found: %s" % str(Key)

            if deletion_key in self.content:
                del self.content[deletion_key]
        else:
            print "Error: Object of type %s does not have a member '.delete'" % self.type
        return Object.bool(True)
            
    def has(self, Key):
        if self.type == Object.LIST:
            for x in self.content:
                if x.content == Key.content: return Object.bool(True)
            return Object.bool(False)
        elif self.type == Object.MAP:
            return Object.bool(Key.content in self.content)
        else:
            print "Error: Object of type %s does not have a member '.size'" % self.type

    def find_key(self, Value):
        if self.type == Object.LIST:
            for i, x in enumerate(self.content):
                if x.content == Value.content: return Object.number(i)
            return Object.void()

        elif self.type == Object.MAP:
            for key, value in self.content.iteritems():
                if value.content == Value.content: return Object.from_string_or_number(key)
            return Object.void()
        else:
            print "Error: Object of type %s does not have a member '.size'" % self.type

    def plain_string(self):
        if self.type == Object.LIST:
            content_str = "".join("%s, " % x.plain_string() for x in self.content)
            if content_str: content_str = content_str[:-2]
            content_str = "[%s]" % content_str

        elif self.type == Object.MAP:
            content_str = "".join("%s: %s, " % (key, value.plain_string()) 
                                  for key, value in self.content.iteritems())
            if content_str: content_str = content_str[:-2]
            content_str = "{%s}" % content_str

        else:
            content_str = str(self.content)
        return content_str

    def __str__(self):
        if self.type == Object.LIST:
            content_str = "".join("%s, " % str(x) for x in self.content)
            if content_str: content_str = content_str[:-2]
            content_str = "[%s]" % content_str

        elif self.type == Object.MAP:
            content_str = "".join("%s: %s, " % (key, str(value)) for key, value in self.content.iteritems())
            if content_str: content_str = content_str[:-2]
            content_str = "{%s}" % content_str
        elif self.type == Object.FUNCTION:
            content_str = ""
        else:
            content_str = str(self.content)
        return "(%s: %s)" % (self.type.upper(), content_str)

class FunctionObject:
    """Applies an OPERATION on the WORLD using a list of ARGUMENTS and returns
       a RESULT. This happens in function '.do()':

                                   .-------------.
                    WORLD -------->|             |
                                   |  OPERATION  +-------> RESULT
                    ARGUMENTS ---->|             |
                                   '-------------'

       A FunctionObject contains:

       -- a function that can deal with a set of arguments
       -- a list of 'strings' that tells about the required argument type.

       A FunctionObject can: 

       -- check if the given argument list is conform to the function call requirements
       -- execute the internal function with the given set of arguments.

       A FunctionObject lives in some type of 'database of possible functions.'
    """
    def __init__(self, OperationFunction, ArgumentListTypes, WorldRequiredF=False):
        self.__function            = OperationFunction
        self.__argument_list_types = ArgumentListTypes
        self.__world_required_f    = WorldRequiredF

    def do(self, world, ArgumentList):

        if self.check_argument_types(ArgumentList) == False:
            print "Error: function '%s'" % self.__function
            print "Error: arguments do not fit: ", ArgumentList
            print "Error: required: " + repr(self.argument_list_types())[1:-1]
            return None

        argument_instance_list = copy(ArgumentList)
        if self.__world_required_f: argument_instance_list.insert(0, world)

        AL = argument_instance_list
        L  = len(AL)

        if   L == 0:  return self.__function()
        elif L == 1:  return self.__function(AL[0])
        elif L == 2:  return self.__function(AL[0], AL[1])
        elif L == 3:  return self.__function(AL[0], AL[1], AL[2])
        elif L == 4:  return self.__function(AL[0], AL[1], AL[2], AL[3])
        elif L == 5:  return self.__function(AL[0], AL[1], AL[2], AL[3], AL[4])
        elif L == 6:  return self.__function(AL[0], AL[1], AL[2], AL[3], AL[4], AL[5])
        elif L == 7:  return self.__function(AL[0], AL[1], AL[2], AL[3], AL[4], AL[5], AL[6])
        elif L == 8:  return self.__function(AL[0], AL[1], AL[2], AL[3], AL[4], AL[5], AL[6], AL[7])
        elif L == 9:  return self.__function(AL[0], AL[1], AL[2], AL[3], AL[4], AL[5], AL[6], AL[7], AL[8])
        elif L == 10: return self.__function(AL[0], AL[1], AL[2], AL[3], AL[4], AL[5], AL[6], AL[7], AL[8], AL[9])
        else:         return None

    def argument_list_types(self):
        return self.__argument_list_types

    def check_argument_types(self, ArgumentList):
        if len(ArgumentList) != len(self.__argument_list_types): 
            return False

        for atype, arg in izip(self.__argument_list_types, ArgumentList):
            if   atype == "Object" or atype == Object.VOID: 
                continue
            elif arg is None:
                if atype == "PyNone":   continue
                else:                   return False
            elif type(arg) == str:
                if atype == "PyString": continue
                else:                   return False
            elif type(arg) == bool:
                if atype == "PyBool":   continue
                else:                   return False
            elif type(arg) == list:     
                if atype == "PyList":   continue
                else:                   return False
            elif type(arg) == dict:     
                if atype == "PyMap":    continue
                else:                   return False
            elif atype == arg.type:     continue
            return False

        return True

class FunctionObjectUser(FunctionObject):
    def __init__(self, FunctionBody, ArgumentNameDb, Ego):
        """FunctionArgumentNameDb:  argment index --> argument name
           FunctionBody:            function to be executed.
        """
    def __init__(self, FunctionArgumentList, FunctionBody):
        self.argument_name_db = dict(
            (i, variable.content) for i, variable in enumerate(FunctionArgumentList)
        )
        self.body = FunctionBody
        self.__ego = Object.void()

    def do(self, world, ArgumentInstanceList):
        self.set_arguments(world, ArgumentInstanceList)
        total_result = True
        for element in self.body:
            result = element.execute(world).content
            if result == False: total_result = False
        self.unset_arguments(world)
        return Object.bool(total_result)

    def set_new_ego(self, NewEgo):
        self.__ego = NewEgo
 
    def set_arguments(self, world, ArgumentInstanceList):
        """Assigns a list of arguments to variables which can then be referenced
        from inside the function. If there is an interference with 'world' 
        variables, the world variables are back-uped.
        """
        self.backup_db = []
        def set_this(Name, TheObject):
            if Name in world.object_db: 
                self.backup_db.append((Name, world.object_db[Name])) # reset upon exit
            else:                          
                self.backup_db.append((Name, None))                     # delete upon exit
            world.object_db[Name] = TheObject
            
        for i, argument in enumerate(ArgumentInstanceList):
            set_this(self.argument_name_db[i], argument)
        set_this("ego", self.__ego)

    def unset_arguments(self, world):
        """Reset the state of the world before the arguments have been set.
        """
        def unset_this(Name, TheObject):
            if TheObject is None and Name in world.object_db: 
                del world.object_db[Name]
            else:  
                world.object_db[Name] = TheObject

        for name, argument in self.backup_db:
            unset_this(name, argument)

        

