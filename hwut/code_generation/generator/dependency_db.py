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
from   collections import defaultdict
from   copy import copy

class DependencyDb(dict):
    """Maintain information about parameters depending on each other.
    """
    def __init__(self, ParameterList):
        """Focus parameters may rely on other parameters. This function 
        checks whether no circular dependency exists. 

        RETURN: --> Everything Ok.
       
        Upon detection of a circular dependency, this function aborts
        with an error message.
        """
        
        def iterable(ParameterList):
            """Iterate of pairs (target, depedency). 'target' is name of the 
           
             parameter which depends on 'dependency'.
            """
            for i, p in enumerate(ParameterList):
                yield p.name, set(p.required_parameter_iterable())

        # dependency_db:    dependency --> target
        # Means that 'dependency' is required for 'target'.
        self.__direct = dict(
            (p.name, set(p.required_parameter_iterable()))
            for p in ParameterList
        )
        # Parameter 'target' depends on parameter 'dependency' being defined.
            
        # Investigate dependencies     
        for target, dependency_set in self.__direct.iteritems():
            dependency_set = copy(dependency_set)
            work_list      = list(dependency_set)
            while work_list:
                sub_target = work_list.pop()
                sub_dependency_set = self.__direct.get(sub_target)
                if not sub_dependency_set: continue
                for dependency in sub_dependency_set:
                    if dependency in dependency_set: continue
                    work_list.append(dependency)
                    dependency_set.add(dependency)

            self[target] = dependency_set
                
        return

    def get_circularity(self):
        """Determines whether DependencyDb contains a circular dependency. If so
        an error message is issued and the function is left. 

        RETURNS: -- list containing path of circular dependency.
                 -- None, else.
        """
        def dive(target, path):
            if   target in path:     del path[:path.index(target)]; return True
            elif target not in self: return False

            for dependency in self.__direct[target]:
                path.append(target)
                if dive(dependency, path): return True
                path.pop()
            return False

        for target in self.__direct.iterkeys():
            path = []
            if dive(target, path): return path
        return None

    def get_parameter_sequence(self, ParameterList):
        """Determine a sequence of parameters that respects dependencies. That is, 
        a parameter A which depends on another parameter B can never come before B.

        Note: As long as there is no circular dependency, then this function produces
        useful results. See 'check_circular_dependency()'.

        RETURNS: Parameter name sequence as a list.
        """
        sequence = []
        for p in ParameterList:
            name = p.name
            # Look from back to front. As soon as a parameter appears which depends on 
            # 'name' we cannot go further backwards.
            for i in range(len(sequence)):
                if sequence[i] in self and name in self[sequence[i]]:
                    sequence.insert(i, name)
                    break
            else:
                sequence.append(name)

        def by_name(Name, ParameterList):
            for p in ParameterList:
                if p.name == Name: return p
            assert False
        
        result = [ by_name(name, ParameterList) for name in sequence ]
        for p in ParameterList:
            if p.name not in sequence: result.append(p)
        return result
        
