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
class E_Attr:
    APP_TITLE                     = 1
    APP_TITLE_GROUP               = 2
    APP_VANISHED_F                = 3
    APP_BUILD_TIME_SEC            = 4
    APP_FILE_NAME                 = 5
    APP_HWUT_INFO_REQUEST_TIME    = 6
    APP_MAKE_DEPENDENT_F          = 7

    CALL_INTERPRETER_LIST         = 8
    CALL_SIZE_LIMIT_KB            = 9
    CALL_STDERR_POST_PROCESSOR    = 10
    CALL_STDOUT_POST_PROCESSOR    = 11
    CALL_TIMEOUT_F                = 12

    OUT_SAME_F                    = 13
    OUT_SHRINK_EMPTY_LINES_F      = 14
    OUT_SHRINK_SPACE_F            = 15
    OUT_TEMPORAL_LOGIC_F          = 16
    OUT_TEMPORAL_LOGIC_RULE_LIST  = 17

    OUT_CMP_ANALOGY_TUPLE         = 18
    OUT_CMP_BACKSLASH_IS_SLASH_F  = 19
    OUT_CMP_HAPPY_PATTERN_LIST    = 20
    OUT_CMP_POTPOURRI_F           = 21

    RESULT_LIST                   = 22

class E_AType:
    STRING      = 0
    FLOAT       = 1
    INTEGER     = 2
    STRING      = 3
    LIST        = 4
    BOOL        = 5
    RESULT_LIST = 6
    REGEX_LIST  = 7

