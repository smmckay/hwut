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
from collections import defaultdict

from hwut.code_generation.generator.parameter import E_ValueType

class ArrayDb:
    """parameter name --> list of settings

       name, setting --> index in list of settings
    """
    def __init__(self):
        self.db = defaultdict(list)
        self.array_type_db    = {}
        self.element_type_db  = {}
        self.value_type_db    = {}
        self.element_n_max_db = defaultdict(int)

    def absorb(self, ParameterList):
        for p in ParameterList:
            if not p.is_array(): continue
            setting_list = self.db[p.name]
            self.array_type_db[p.name]   = p.concrete_type
            self.element_type_db[p.name] = p.element_type
            self.value_type_db[p.name]   = p.value_type
            for setting in p.array_settings():
                if setting in setting_list: continue
                setting_list.append(setting)
                if len(setting) > self.element_n_max_db[p.name]:
                    self.element_n_max_db[p.name] = len(setting)
            
    def array_name(self, name, setting):
        setting_list = self.db[name]
        index        = setting_list.index(setting)
        return "$$G$$_array_%s_%s" % (name, index)

    def implement(self):
        txt = ""
        for name, setting_list in self.db.iteritems():
            array_type_str = self.array_type_db[name]
            element_type   = self.element_type_db[name]
            value_type     = self.value_type_db[name]
            element_n_max  = self.element_n_max_db[name]
            for setting in setting_list:
                name_str  = self.array_name(name, setting)
                array_str = self.array_code(setting, value_type, element_n_max)
                txt += "static const %s %s = %s;\n" % (array_type_str, name_str, array_str)
        return txt
            
    def array_code(self, Array, ValueType, ElementNMax): 
        txt = "{ %i, { " % len(Array)
        if ValueType == E_ValueType.IARRAY: 
            txt += "".join(" %i, " % x for x in Array)
            for i in xrange(len(Array), ElementNMax):
                txt += "0, "
        else:                               
            txt += "".join(" %f, " % x for x in Array)
            for i in xrange(len(Array), ElementNMax):
                txt += "0.0, "
        txt += " } }"
        return txt
