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
from hwut.code_generation.generator.parameter       import ParameterConstant, E_ValueType, E_ValueType

class Generator:
    """Description which allows to implement a series of parameter settings. 
    The description consist of a list of 'Parameter' objects. Each parameter
    object describes the values which a parameter can take.

    The created generator uses the value which parameter can take and iterates
    over them with a cursor. The series of setting corresponds to iterating
    over all possible combinations of parameter settings. The series may be 
    restricted by constraints. Constraints may disallow certain parameter 
    value settings from being considered.
    """
    def __init__(self, ParameterList, ConstraintList, DependencyDb):
        self.parameter_list  = ParameterList
        self.constraint_list = ConstraintList
        self.dependency_db   = DependencyDb

        # Make sure, that all parameters are properly setup
        for p in self.parameter_list:
           p.finalize(ParameterList) 

        L = len(self.parameter_list)
        self.cursor_dimension_array              = [ ] 
        self.map_cursor_index_to_parameter_index = [ ] 
        self.parameter_name_to_cursor_index_db   = {}
        cursor_index = -1
        for p in self.parameter_list:
            cursor_index += 1
            self.cursor_dimension_array.append(p.get_step_number())
            self.map_cursor_index_to_parameter_index.append(p.index)
            self.parameter_name_to_cursor_index_db[p.name] = cursor_index

    def setting_number(self):
        product = 1
        for dim in self.cursor_dimension_array:
            product *= dim
        return product

    def parameter_list_by_precedence(self):
        """Parameters may depend on each other. This function returns a
        sequence in which parameters can be evaluated, so that every dependent
        factor is evaluated after the one he requires.
        """
        if self.dependency_db is None:
            return self.parameter_list
        else:
            return self.dependency_db.get_parameter_sequence(self.parameter_list)

    def parameter_list_is_constant(self):
        for parameter in self.parameter_list:
            if not isinstance(parameter, ParameterConstant): 
                return False
        return True

    def check_consistency(self, parameter_db):
        if len(self.parameter_list) == 0:
            print "Error: no parameters."

        name_list = [p.name for p in self.parameter_list]

        # No parameter can appear twice, because they are named according
        # their position in the line.
        assert len(set(name_list)) == len(name_list)

        # Any name list is in parameter_db. This results from the way
        # that the parameter names are associated with parameters.
        for name in name_list:
            assert name not in parameter_db

        for info in parameter_db:
            if info.name not in name_list: 
                print "Error: '%s' not mentioned in line." % name

    def __str__(self):
        txt = [ "".join("%s; " % p for p in self.parameter_list) ]
        for constraint in self.constraint_list:
            txt.append("<<%s>>\n" % constraint)
        return "".join(txt)

class GeneratorContantLines:
    """A list of parameter settings. Parameter settings sequences are determined
    by a plain constant list. No generation, such as permutation and filtering 
    aplies. 
    """
    def __init__(self, ParameterListList):
        self.setting_list   = ParameterListList
        self.parameter_list = ParameterListList[0]

        self.cursor_dimension_array              = [ self.setting_number() ]
        self.map_cursor_index_to_parameter_index = [ 0 ] # The pointer into table.
        self.parameter_name_to_cursor_index_db   = {}

    def setting_number(self):
        return len(self.setting_list)

    def __str__(self):
        txt = []
        for setting in self.setting_list:
            txt.append("".join("%s, " % x.constant for x in setting))
            txt.append("\n")
        return "".join(txt)

    def check_consistency(self, parameter_db):
        return

def get_max_array_length_db(SectionList):
    result = {}
    for g in SectionList:
        for p in g.parameter_list:
            if   not p.is_array():                    continue
            elif p.name not in result:                result[p.name] = p.max_array_length()
            elif p.max_array_length > result[p.name]: result[p.name] = p.max_array_length()
    return result
        
