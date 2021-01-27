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
from   hwut.test_db.result                import TestResult
from   hwut.test_db.attributes.core       import E_Attr, E_AType
import hwut.test_db.attributes.interview  as     hwut_interview

__attribute_db = {
    #                                     fly tag:                    default:                    type:
    E_Attr.APP_TITLE:                    ("title",                    "",                         E_AType.STRING),
    E_Attr.APP_TITLE_GROUP:              ("title_group",              "",                         E_AType.STRING),
    E_Attr.APP_VANISHED_F:               ("vanished_f",               False,                      E_AType.BOOL),
    E_Attr.APP_BUILD_TIME_SEC:           ("build_time",               None,                       E_AType.FLOAT), 
    E_Attr.APP_FILE_NAME:                ("file_name",                "#none#",                   E_AType.STRING),
    E_Attr.APP_HWUT_INFO_REQUEST_TIME:   ("hwut_info_time",           None,                       E_AType.INTEGER), 
    E_Attr.APP_MAKE_DEPENDENT_F:         ("make_dependent_f",         False,                      E_AType.BOOL),
                                                                                                  
    E_Attr.CALL_INTERPRETER_LIST:        ("interpreter_list",         [],                         E_AType.LIST),
    E_Attr.CALL_SIZE_LIMIT_KB:           ("size_limit_kb",            None,                       E_AType.INTEGER),    
    E_Attr.CALL_STDERR_POST_PROCESSOR:   ("stderr_post_proc",         None,                       E_AType.STRING),
    E_Attr.CALL_STDOUT_POST_PROCESSOR:   ("stdout_post_proc",         None,                       E_AType.STRING),
    E_Attr.CALL_TIMEOUT_F:               ("time_out_detection_f",     True,                       E_AType.BOOL),
    E_Attr.CALL_REMOTE_CONFIGURATION_ID: ("remote_config_id",         None,                       E_AType.STRING),
                                                                                                  
    E_Attr.OUT_SAME_F:                   ("same_f",                   False,                      E_AType.BOOL),
    E_Attr.OUT_SHRINK_EMPTY_LINES_F:     ("shrink_empty_lines_f",     True,                       E_AType.BOOL),
    E_Attr.OUT_SHRINK_SPACE_F:           ("shrink_space_f",           True,                       E_AType.BOOL),
    E_Attr.OUT_TEMPORAL_LOGIC_F:         ("temporal_logic_f",         False,                      E_AType.BOOL),
    E_Attr.OUT_TEMPORAL_LOGIC_RULE_LIST: ("temporal_logic_rule_list", [],                         E_AType.LIST),

    E_Attr.OUT_EXTRA_OUTPUT_FILE_LIST:   ("extra_output_file_list",   None,                       E_AType.DICT_LIST),
                                                                                                  
    E_Attr.OUT_CMP_ANALOGY_TUPLE:        ("analogy",                  ("((", "))"),               E_AType.LIST),  # 0 -> open; 1 -> close
    E_Attr.OUT_CMP_BACKSLASH_IS_SLASH_F: ("backslash_is_slash_f",     True,                       E_AType.BOOL),
    E_Attr.OUT_CMP_HAPPY_PATTERN_LIST:   ("happy_pattern_list",       [],                         E_AType.REGEX_LIST),
    E_Attr.OUT_CMP_POTPOURRI_F:          ("potpourri_f",              True,                       E_AType.BOOL),

    E_Attr.RESULT_LIST:                  ("result_list",              [TestResult("","",None,0)], E_AType.RESULT_LIST),
}

class AttributeDb(dict):
    def __init__(self, Table):
        dict.__init__(self, Table)

    def get_default(self, Attribute):
        return self[Attribute][1]

    def get_name(self, Attribute):
        return self[Attribute][0]

    def get_type(self, Attribute):
        return self[Attribute][2]

    def get_attribute(self, Name):
        for key, value in self.iteritems():
            if value[0] == Name: return key
        return None

    def is_list(self, Attribute):
        entry = self.get(Attribute)
        if entry is None:  return False
        else:              return entry[2] == E_AType.LIST

    def attribute_default_iterable(self):
        for key, info in self.iteritems():
            yield key, info[1]

attribute_db = AttributeDb(__attribute_db)




