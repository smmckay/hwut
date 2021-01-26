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
from hwut.code_generation.function_stubs.c.core          import ObjectSpec
from hwut.code_generation.generator.language.c.auxiliary import get_integer_code

from collections import namedtuple

import sys

class E_ValueType:
    INTEGER = "INTEGER"
    FLOAT   = "FLOAT"
    STRING  = "STRING"
    IARRAY  = "IARRAY"
    FARRAY  = "FARRAY"

    @staticmethod
    def name(X):
        return {
            E_ValueType.INTEGER: "INTEGER",
            E_ValueType.FLOAT:   "FLOAT",
            E_ValueType.STRING:  "STRING",
            E_ValueType.IARRAY:  "IARRAY",
            E_ValueType.FARRAY:  "FARRAY",
        }[X]

    @staticmethod
    def is_array(X):
        return X in (E_ValueType.IARRAY, E_ValueType.FARRAY)

    @staticmethod
    def is_number(X):
        return X in (E_ValueType.FLOAT, E_ValueType.INTEGER)

class Parameter(ObjectSpec):
    def __init__(self, ValueType):
        ObjectSpec.__init__(self, "", "")
        self.index      = None
        self.value_type = ValueType

    def specify(self, Index, Name, Type):
        self.index = Index
        self.name  = Name
        self.type = Type       #-> ObjectSpec

    @property
    def concrete_type(self):
        if self.is_array():
            return "$$G$$_array_%s_t" % self.name
        else:
            return self.type

    @property
    def member_type(self):
        if   self.is_array(): 
            return "const %s*" % self.concrete_type
        elif self.value_type == E_ValueType.STRING:
            if self.concrete_type.find("const") != -1: 
                return self.concrete_type
            else:                                      
                return "const %s" % self.concrete_type
        else:
            return self.concrete_type

    @property
    def element_type(self):
        return self.type

    def get_minimum(self, ParameterList):
        assert False

    def get_maximum(self, ParameterList):
        assert False

    def finalize(self, ParameterList):
        assert False

    def get_step_number(self):
        assert False

    def required_parameter_iterable(self):
        """Generator that produces iterable over all parameter on which this
        parameter depends.
        """
        if False: yield None

    def array_settings(self):
        return []
        
    def format_string(self):
        return {
            E_ValueType.INTEGER: "%i",
            E_ValueType.FLOAT:   "%f",
            E_ValueType.STRING:  "%s",
            E_ValueType.IARRAY:  "%i",
            E_ValueType.FARRAY:  "%f",
        }[self.value_type]

    def format_string_cast(self):
        return {
            E_ValueType.INTEGER: "int",
            E_ValueType.FLOAT:   "float",
            E_ValueType.STRING:  "const char*",
            E_ValueType.IARRAY:  "int",
            E_ValueType.FARRAY:  "float",
        }[self.value_type]

    def is_array(self):
        return E_ValueType.is_array(self.value_type)

    def max_array_length(self):
        assert False

    def __str__(self):
        assert False

class ParameterConstant(Parameter):
    def __init__(self, ValueType, Value):
        Parameter.__init__(self, ValueType)
        self.constant  = Value

    def get_minimum(self, ParameterList):
        return self.constant

    def get_maximum(self, ParameterList):
        return self.constant

    def finalize(self, ParameterList):
        pass

    def get_step_number(self):
        return 1
        
    def get_setting_by_iterator(self, ArrayDb, CursorIndex):
        if   self.value_type == E_ValueType.FLOAT:
            return "    it->%s = %s;\n"     % (self.name, self.constant)
        elif self.value_type in E_ValueType.INTEGER:
            return "    it->%s = %s;\n"     % (self.name, get_integer_code(self.constant, self.concrete_type))
        elif self.value_type == E_ValueType.STRING:
            return "    it->%s = \"%s\";\n" % (self.name, self.constant)
        elif self.is_array():
            return "    it->%s = &%s;\n"    % (self.name, ArrayDb.array_name(self.name, self.constant))
        else:
            assert False
        
    def array_settings(self):
        if not self.is_array(): return []
        else:                   return [ self.constant ]
        
    def max_array_length(self):
        if not self.is_array(): return -1
        else:                   return len(self.constant)

    def __str__(self):
        return "[%s] %s: (%s)%s" % (self.index, self.name, 
                                    E_ValueType.name(self.value_type), 
                                    self.constant)

class ParameterSelection(Parameter):
    def __init__(self, ValueType, Selection):
        assert type(Selection) == list
        Parameter.__init__(self, ValueType)
        self.selection = Selection

    def get_minimum(self, ParameterList):
        if self.value_type not in (E_ValueType.INTEGER, E_ValueType.FLOAT):
            print "Error: Parameter '%s' may not be used in numeric expression."
            sys.exit()
        return min(self.selection)

    def get_maximum(self, ParameterList):
        if self.value_type not in (E_ValueType.INTEGER, E_ValueType.FLOAT):
            print "Error: Parameter '%s' may not be used in numeric expression."
            sys.exit()
        return max(self.selection)

    def finalize(self, ParameterList):
        pass

    def get_step_number(self):
        return len(self.selection)
        
    def array_settings(self):
        if not self.is_array(): return []
        else:                   return self.selection
        
    def get_setting_by_iterator(self, ArrayDb, CursorIndex):
        assert CursorIndex is not None

        txt = [ "    switch( it->hwut.cursor.index[%i] ) {\n" % CursorIndex ]

        for i, element in enumerate(self.selection):
            if self.value_type in E_ValueType.INTEGER:
                rvalue = "%s" % get_integer_code(element, self.concrete_type)
            elif self.value_type in E_ValueType.FLOAT:
                rvalue = "%s" % element
            elif self.value_type == E_ValueType.STRING:
                rvalue = "\"%s\"" % element
            elif self.is_array():
                rvalue = "&%s" % ArrayDb.array_name(self.name, self.selection[i])
            else:
                assert False
            txt.append("        case %s: it->%s = %s; break;\n" % (i, self.name, rvalue))
        txt.append("    }\n")
        return "".join(txt)

    def max_array_length(self):
        if not self.is_array(): return -1
        return max([len(array) for array in self.selection])

    def __str__(self):
        return "[%s] %s: (%s)%s" % (self.index, self.name, 
                                    E_ValueType.name(self.value_type), 
                                    self.selection)

# .front = first element in range
# .back  = last element in range
Range = namedtuple("Range", ("front", "back"))

class ParameterRange(Parameter):
    def __init__(self, ValueType, RangePrimary, RangeCut=None, Step=None):
        """'RangePrimary' and 'Step' determine the iteration over the range. 
        The 'RangeCut' determines inside what interval the values need to lie.
        """
        Parameter.__init__(self, ValueType)
        assert RangePrimary.front is not None
        assert RangePrimary.back is not None
        
        self.primary = RangePrimary
        self.cut     = RangeCut   
        if Step is not None:  self.step = Step
        else:                 self.step = 1

    def get_minimum(self, ParameterList):
        if hasattr(self.primary.front, "get_minimum"): 
            return self.primary.front.get_minimum(ParameterList)
        else:
            return self.primary.front

    def get_maximum(self, ParameterList):
        if hasattr(self.primary.back, "get_maximum"): 
            return self.primary.back.get_maximum(ParameterList)
        else:
            return self.primary.back

    def primary_range_size_is_zero(self):
        front = self.primary.front
        back  = self.primary.back
        if front.__class__ == TrivialExpression:
            return front.is_equal(back)
        else:
            return front == back

    def finalize(self, ParameterList):
        if self.primary.front.__class__ == TrivialExpression:
            self.primary.front.determine_parameter_reference(ParameterList)

        if self.primary.back.__class__ == TrivialExpression:
            self.primary.back.determine_parameter_reference(ParameterList)

        if     self.primary.front.__class__ == TrivialExpression  \
           and self.primary.back.__class__  == TrivialExpression  \
           and self.primary.front.identifier == self.primary.back.identifier:
           delta = TrivialExpression.get_max_delta(self.primary.front,
                                                   self.primary.back, 
                                                   ParameterList) 
        else:
            front = self.get_minimum(ParameterList)
            back  = self.get_maximum(ParameterList)
            delta = back - front

        if delta < 0: 
            print "Error: minimum > maximum in range expression"
            sys.exit()
        
        self.__step_number = int(float(delta) / float(self.step) + 0.5) + 1

    def get_step_number(self):
        assert self.__step_number
        return self.__step_number
        
        
    def required_parameter_iterable(self):
        if isinstance(self.primary.front, TrivialExpression):
            yield self.primary.front.identifier
        if isinstance(self.primary.back, TrivialExpression):
            yield self.primary.back.identifier
        if self.cut is not None:
            if isinstance(self.cut.front, TrivialExpression):
                yield self.cut.front.identifier
            if isinstance(self.cut.back, TrivialExpression):
                yield self.cut.back.identifier

    def get_setting_by_iterator(self, ArrayDb, CursorIndex):
        assert CursorIndex is not None

        #   value = primary_front + index * step
        #   if   value > primary_back:  value = primary_back
        #   elif value < primary_front: value = primary_front
        #   if   value > cut_back:      value = cut_back
        #   elif value < cut_front:     value = cut_front

        def get_string(X):
            if hasattr(X, "identifier"): 
                if X.op is None: return "it->%s"                 % X.identifier
                else:            return "(((%s)(it->%s)) %s %s)" % (self.concrete_type, X.identifier, X.op, X.number)
            else:                        
                if self.value_type == E_ValueType.INTEGER:
                    return get_integer_code(X, self.concrete_type)
                else:
                    return X

        ct = self.concrete_type

        primary_front_type = ct
        if self.primary.front.__class__ == TrivialExpression:
            primary_front_type = self.primary.front.parameter_ref.concrete_type
        primary_back_type = ct
        if self.primary.back.__class__ == TrivialExpression:
            primary_back_type = self.primary.back.parameter_ref.concrete_type

        txt = [ "{\n" ]
        if self.cut is not None:
            txt.extend([
                "    %s cut_front     = (%s)%s;\n" % (ct, ct, get_string(self.cut.front)),
                "    %s cut_back      = (%s)%s;\n" % (ct, ct, get_string(self.cut.back)),
            ])

        if not self.primary_range_size_is_zero():
            txt.extend([
                "    %s primary_front = %s;\n" % (ct, get_string(self.primary.front)),
                "    %s primary_back  = %s;\n" % (ct, get_string(self.primary.back)),
                "    %s step_size     = (%s)%s;\n" % (ct, ct, self.step),
                "    %s index         = (%s)(it->hwut.cursor.index[%i]);\n" % (ct, ct, CursorIndex),
                # Protect against overflow
                "    %s delta         = index * step_size;\n"     % ct,
                "    %s value         = primary_front + delta;\n" % ct,
                "    if     ( delta < 0 )             return 0; /* impossible */\n",
                "    else if( value < primary_front ) return 0; /* impossible */\n",
                "    else if( value > primary_back )  return 0; /* impossible */\n"
            ])
        else:
            txt.extend([
                "    %s value         = (%s)%s;\n" % (ct, ct, get_string(self.primary.front)),
            ])

        if self.cut is not None:
            txt.extend([
                "    if     ( value < cut_front )     return 0; /* impossible */\n",
                "    else if( value > cut_back )      return 0; /* impossible */\n"
            ])
        txt.extend([
            "    it->%s = (%s)value;\n" % (self.name, ct),
            "}\n"
        ])
       
        return "".join("    %s" % line for line in txt)

    def __str__(self):
        txt = [
            "[%s] %s: (%s) " % (self.index, self.name, self.value_type)
        ]
        txt.append("|%s:%s|" % (self.primary.front, self.primary.back))
        if self.cut is not None:
            txt.append("in |%s:%s|" % (self.cut.front, self.cut.back))
        if self.step != 1:
            txt.append("step %s" % (self.step))
        return "".join(txt)

class TrivialExpression:
    __slots__ = ("identifier", "op", "number", "parameter_ref")
    def __init__(self, Identifier, Op, Number, ParameterRef=None):
        self.identifier    = Identifier
        self.op            = Op
        self.number        = Number
        self.parameter_ref = ParameterRef

    def get_minimum(self, ParameterList):
        min_offset = self.parameter_ref.get_minimum(ParameterList)
        return self.operate(min_offset)

    def get_maximum(self, ParameterList):
        assert self.parameter_ref is not None
        max_offset = self.parameter_ref.get_maximum(ParameterList)
        return self.operate(max_offset)

    def is_equal(self, Other):
        if Other.__class__ != TrivialExpression:
            return False
        return     self.identifier == Other.identifier \
               and self.op         == Other.op         \
               and self.number     == Other.number

    def determine_parameter_reference(self, ParameterList):
        """RETURNS:      Parameter with name == identifier
           THROWS ERROR: If no such parameter exists.
        """
        for p in ParameterList:
            if p.name == self.identifier: 
                self.parameter_ref = p
                return
        print "Error: Parameter '%s' does not exist in expression." % self.identifier
        sys.exit()

    def is_add(self):
        return self.op in ("-", "+", None) # No operation/ no constant = "+ zero"

    def norm_number(self):
        """RETURNS: The .number member's value in a 'normalized' manner.

        That is, it returns a numeric value, so that the operator '+' can be
        used even in case of .op == '-' and the operation '*' may be used in 
        case that .op == '/'. This means, that the .number may be potentionally
        inverted with respect to the given operation.
        """
        if   self.op is None:    return 0  # No operation/ no constant = "+ zero"
        elif self.op == "-":     return - self.number
        elif self.op == "/": 
            if self.number != 0: return 1.0 / self.number
            else:
                print "Error: division by zero."
                sys.exit()
        return self.number

    @staticmethod
    def get_max_delta(X, Y, ParameterList):
        """RETURNS: The maximum distance of two parameters 'X' and 'Y' if both
                    rely on the same identifier.
        """
        assert X.identifier == Y.identifier

        n0 = X.norm_number()
        n1 = Y.norm_number()

        # (x + n1) - (x + n0)
        if X.is_add() and Y.is_add():         return n1 - n0

        p       = X.__get_parameter_reference(ParameterList)
        maximum = p.get_maximum(ParameterList)
        # (x * n1) - (x * n0) = x * (n1 - n0)
        if not X.is_add() and not Y.is_add(): return maximum * (n1 - n0)
        # (x * n1) - (x + n0) = x * (n1 - 1) - n0
        if not X.is_add() and     Y.is_add(): return maximum * (n1 - 1) - n0
        # (x + n1) - (x * n0) = x * (1 - n0) + n0
        if not X.is_add() and not Y.is_add(): return maximum * (1 - n0) + n1

        # All cases should have been handled
        assert False 

    def operate(self, Value):
        if   self.op is None: return Value
        elif self.op == "+":  return Value + self.number
        elif self.op == "-":  return Value - self.number
        elif self.op == "*":  return Value * self.number
        elif self.op == "/":  return Value / self.number
        else:                 assert False

    def __str__(self):
        if self.op is None: return "%s" % self.identifier
        else:               return "%s%s%s" % (self.identifier, self.op, self.number)
        
def assign(P, Source):
    return "it->%s = %s" % (P.name, Source)

