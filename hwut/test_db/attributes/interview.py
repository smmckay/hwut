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
from   hwut.temporal_logic.parser.lexical_analysis import __read_integer
from   hwut.test_db.attributes.core                import E_Attr
from   hwut.test_db.result                         import TestResult
import hwut.common                                 as     common

def __comma_separated_list(Line, MinN=None):
    item_list = Line.split(",")
    if MinN is not None and len(item_list) < MinN:
        print "Error: %s requires exactly %s arguments separated by comma." % (Keyword, MinN)
        sys.exit()
    result = filter(lambda s: len(s), [ str(p).strip() for p in item_list])
    return result

def on_CHOICES(descr, line):
    choice_list               = __comma_separated_list(line)
    descr[E_Attr.RESULT_LIST] = [ 
        TestResult(choice, "", None, 0) for choice in choice_list 
    ]

def on_SAME(descr, line):
    descr[E_Attr.OUT_SAME_F] = True

def on_LOGIC(descr, line):
    # -- temporal logic
    rule_file_list = __comma_separated_list(line)
    descr[E_Attr.OUT_TEMPORAL_LOGIC_RULE_LIST] = rule_file_list
    descr[E_Attr.OUT_TEMPORAL_LOGIC_F]         = True

def on_NO_POTPOURRI(descr, line):
    descr[E_Attr.OUT_CMP_POTPOURRI_F] = False 
    
def on_NO_BACKSLASH_IS_SLASH(descr, line):
    descr[E_Attr.OUT_CMP_BACKSLASH_IS_SLASH_F] = False

def on_NO_SHRINK(descr, line):
    on_NO_SHRINK_SPACES(descr, line)
    on_NO_SHRINK_EL(descr, line)
    
def on_NO_SHRINK_SPACES(descr, line):
    descr[E_Attr.OUT_SHRINK_SPACE_F] = False
    
def on_NO_SHRINK_EL(descr, line):
    descr[E_Attr.OUT_SHRINK_EMPTY_LINES_F] = False
    
def on_NO_ANALOGY(descr, line):
    descr[E_Attr.OUT_CMP_ANALOGY_TUPLE] = (None, None)
    
def on_NO_TIME_OUT(descr, line):
    descr[E_Attr.CALL_TIMEOUT_F] = False
    
def on_SIZE_LIMIT(descr, line):
    number_str                       = __comma_separated_list(line, 1)[0]
    descr[E_Attr.CALL_SIZE_LIMIT_KB] = get_size_limit_kb(number_str)

def on_ANALOGY(descr, line):
    open_str, close_str                 = __comma_separated_list(line, 2)
    descr[E_Attr.OUT_CMP_ANALOGY_TUPLE] = (open_str.strip(), close_str.strip())

def on_HAPPY(descr, line):
    pattern_str = line.strip()
    regex       = common.re_compile(pattern_str)
    if regex is None: return
    descr[E_Attr.OUT_CMP_HAPPY_PATTERN_LIST].append((regex, pattern_str))

handler_db = {
    "CHOICES:":              on_CHOICES,
    "SAME":                  on_SAME,
    "LOGIC:":                on_LOGIC,
    "NO-POTPOURRI":          on_NO_POTPOURRI,
    "NO-BACKSLASH-IS-SLASH": on_NO_BACKSLASH_IS_SLASH,
    "NO-SHRINK":             on_NO_SHRINK,
    "NO-SHRINK-SPACES":      on_NO_SHRINK_SPACES,
    "NO-SHRINK-EL":          on_NO_SHRINK_EL,
    "NO-ANALOGY":            on_NO_ANALOGY,
    "NO-TIME-OUT":           on_NO_TIME_OUT,
    "SIZE-LIMIT:":           on_SIZE_LIMIT,
    "ANALOGY:":              on_ANALOGY,
    "HAPPY:":                on_HAPPY,
}

unit_db = { 
    "KB":  1024**1,  # kilo byte
    "MB":  1024**2,  # mega byte
    "GB":  1024**3,  # giga byte
    "TB":  1024**4,  # terra byte
    "PB":  1024**5,  # peta byte
    "EB":  1024**6,  # exa byte 
    "ZB":  1024**7,  # zetta byte
    "YB":  1024**8,  # yotta byte
    "BB":  1024**9,  # bronto byte
    "GeB": 1024**10  # gego byte
}
def get_size_limit_kb(NumberStr):
    """Parses the given number string of the pattern

            number ["KB" "MB" "GB" "TP" "PB" "EB" "ZB" "YB", "BB", "GeB"]

    RETURNS: Size limit in kilobytes. 
    
    If "KB" is specified no scaling happens. If "MB" is specified the 
    number is multiplied by 1024. "GB" causes a mulitplication by 1024**2.
    """
    global unit_db
    NumberStr = NumberStr.strip()
    L         = len(NumberStr)
    for unit, scale in unit_db.iteritems():
        index = NumberStr.rfind(unit) 
        if index != L-2: continue
        value_str = NumberStr[:index].strip()
        fh        = StringIO(value_str)
        integer   = __read_integer(fh)
        if integer is None:
            print "Error: integer required for 'SIZE-LIMIT: <int> UNIT;'"
            return None
        return integer * scale
    else:
        print "Error: SIZE-LIMIT: <int> UNIT;"
        print "Error: missing UNIT, i.e 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'BB', 'GeB'."
        return None
