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
from hwut.temporal_logic.classes.statement_element import SourceCodeOrigin, Fork, reject
from hwut.temporal_logic.classes.primary           import Primary_String, \
                                                          Primary_Event, \
                                                          Primary_ConstantNumber, \
                                                          Primary_Variable

__current_file_name     = ""
__current_line_n        = 0
__current_stream_handle = None

__keyword_list = [ "if", "else", "from", "to", "not", "and", "or", "match", "on", "freeze", "unfreeze", "shallow", "space", "active", "passive", "import" ]

def variable_name(sh):
    """identifier         = normal variable (starting with a LOWERCASE letter).
       $time, $time_alert = special variable ($time_alert = time when condition was awoken
                            $time  = current time)
       $n                 = where 'n' is an integer number. This is the matching lexeme
                            number 'n' in a regular expression triggered event definition.
    """
    pos = sh.tell()
    
    if word(sh, "$").ok(): 
        tmp = identifier(sh, AllowKeywordF=True)
        if tmp.ok() and tmp.content in ["time", "time_alert"]:
            tmp.content = "$" + tmp.content
            return Primary_Variable(tmp.content)
        tmp = integer(sh)
        if tmp.error(): return reject(sh, pos, "variable name")
        return Primary_Variable("$%i" % int(tmp.content))
    else:
        tmp = identifier(sh)
        if tmp.error() or not tmp.content[0].islower(): return reject(sh, pos, "variable name")
        return Primary_Variable(tmp.content)
        
    return reject(sh, pos, "variable name")

def event_name(sh):
    """Event names start with an UPPERCASE letter.
       $INIT = the initial event when the test starts.
    """
    pos = sh.tell()
    if word(sh, "$").ok(): 
        tmp = identifier(sh, AllowKeywordF=True)
        if tmp.ok() and tmp.content == "INIT":
            tmp.content = "$" + tmp.content
            return tmp

    tmp = identifier(sh)
    if tmp.error() or not tmp.content[0].isupper(): 
        return reject(sh, pos, "event name")
    return Primary_Event(tmp.content)

def integer(sh):
    pos = sh.tell()

    tmp = sh.read(1)
    if tmp == "-": sign = -1
    else:          sh.seek(-1, 1); sign = 1

    number = __read_integer(sh)

    if number is None: return reject(sh, pos, "integer")
    else:              return Primary_ConstantNumber(sign * number)

def number(sh):
    pos = sh.tell()

    # skip_whitespace(sh)
    
    tmp = sh.read(1)
    if tmp == "-": sign = -1
    else:          sh.seek(pos); sign = 1

    number_str      = ""
    dot_occurence_f = False
    while 1 + 1 == 2:
        tmp = sh.read(1)
        if   tmp == "": break
        elif tmp == ".": 
            if dot_occurence_f:  # there can be only one dot in a number
                sh.seek(-1, 1)
                break
            dot_occurence_f = True
        elif tmp.isdigit() == False:
            sh.seek(-1, 1)
            break

        number_str += tmp

    if number_str == "": return reject(sh, pos, "number")

    return Primary_ConstantNumber(float(number_str) * sign)

def identifier(sh, AllowKeywordF=False):
    pos = sh.tell()

    skip_whitespace(sh)
    id_start = map(chr,   range(ord('a'), ord('z')+1) 
                        + range(ord('A'), ord('Z')+1) 
                        + [ ord('_') ])
    id_continue = map(chr,   range(ord('a'), ord('z')+1) 
                           + range(ord('A'), ord('Z')+1) 
                           + range(ord('0'), ord('9')+1)
                           + [ ord('_') ])

    identifier_str = sh.read(1)
    if identifier_str not in id_start: return reject(sh, pos, "identifier")

    while 1 + 1 == 2:
        tmp = sh.read(1)
        if tmp == "": break
        if tmp not in id_continue: 
            sh.seek(-1, 1)
            break
        identifier_str += tmp

    if not AllowKeywordF:
        # keywords cannot be identifiers
        if identifier_str in __keyword_list: return reject(sh, pos, "identifier")

    return Primary_String(identifier_str)

def cmp(sh):
    pos = sh.tell()
    # NOTE: test first for the two character long comparators that could
    #       be outruled by the shorter ones
    tmp = word_options(sh, [">=", "<="])
    if tmp.ok(): return tmp

    tmp = word_options(sh, ["<", ">", "==", "!="])
    if tmp.ok(): return tmp

    return reject(sh, pos, "comparator")

def string(sh, LeaveBackslashBeforeQuoteF=False):
    pos = sh.tell()
    if word(sh, '"').error(): return reject(sh, pos, "string")
    txt = ""
    backslash_f = False
    while 1 + 1 == 2:
        tmp = sh.read(1)
        if tmp == "": 
            return reject(sh, pos, "string")
        elif tmp == '\\': 
            if backslash_f == False: backslash_f = True
            else:                    txt += '\\'; backslash_f = False
            continue
        elif backslash_f: 
            if tmp == '"': 
                if LeaveBackslashBeforeQuoteF: txt += '\\'
                txt += '"'
            else:
                txt += '\\' + tmp
            backslash_f = False
            continue
        elif tmp == '"':
            return Primary_String(txt)
        else:
            txt += tmp
            backslash_f = False

    return Primary_String(txt)

def word(sh, Word):
    skip_whitespace(sh)
    return plain_word(sh, Word)

def plain_word(sh, Word):
    pos = sh.tell()
    for letter in Word:
        character = sh.read(1)
        if character == "":     return reject(sh, pos, "'%s'" % Word)
        if letter != character: return reject(sh, pos, "'%s'" % Word)

    return Primary_String(Word)

def word_options(sh, WordList):
    pos  = sh.tell()
    MaxL = max(WordList)

    skip_whitespace(sh)
    txt = ""
    while len(txt) < MaxL:
        character = sh.read(1)
        if character == "": break

        txt += character
        if txt in WordList: return Primary_String(txt)

    return reject(sh, pos, WordList)

def skip_whitespace(sh):
    """Read all whitespace from current position until the first non-whitespace character.
       Skip comments that start with '#' and end with newline.
    """
    assert sh.tell() >= 0
    while 1 + 1 == 2:
        tmp = sh.read(1)
        if tmp == "#": 
            # read until end of comment
            while tmp != "\n": 
                tmp = sh.read(1)
                if tmp == "": return
            __record_line_n_increase(sh)

        elif tmp == "": return 
        elif tmp == "\n": 
            __record_line_n_increase(sh)
        elif not tmp.isspace(): break 

    sh.seek(-1, 1)
    return

def skip_line(sh):
    global __current_line_n
    sh.readline()
    __current_line_n += 1

def __record_line_n_increase(sh):
    global __current_line_n
    global __current_stream_handle
    __current_line_n        += 1  # recall stream handle to be able to detect 
    __current_stream_handle = sh  # multi-thread problems.

def _get_current_line_n(sh):
    global __current_line_n
    # return __current_line_n  ## Once, that thing is handled safely

    pos = sh.tell()
    sh.seek(0)
    line_n = sh.read(pos).count("\n")
    return line_n + 1 # zero newlines means we are in line '1'

def origin(sh, StartPosition):
    global __current_line_n
    global __current_file_name

    ## global __current_stream_handle
    ## assert sh == __current_stream_handle, \
    ##       "Multi-threading error while line counting. Different threads interfer."
    current_position = sh.tell()
    sh.seek(StartPosition)
    skip_whitespace(sh)
    line_n = _get_current_line_n(sh)
    sh.seek(current_position)
    return SourceCodeOrigin(__current_file_name, line_n)

def __read_integer(fh):
    """Read an integer in decimal, hex, octal, binary, or roman notation. 

    This code is based on 'read_integer' from the open-source project 'Quex'.
    (C) Frank-Rene Schaefer
    """
    base, digit_db = __get_base_an_digit_db(fh)
    if base is None:
        return None

    pos      = fh.tell()
    result   = 0
    virgin_f = True
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if   tmp == "":                                      # end of file
            if virgin_f: fh.seek(pos); return None
            else:        break
        elif tmp == ".": 
            if base in (2, 8, 16): continue                  # '.' as beautifier
            else:                  fh.seek(pos); return None # not an integer

        digit = digit_db.get(tmp)
        if digit is None: 
            if virgin_f: fh.seek(pos); return None           # not an integer
            else:        fh.seek(-1, 1); break               # end of integer
        virgin_f = False
        result *= base
        result += digit

    return result

db_binary  = dict((digit, ord(digit) - ord("0")) for digit in "01")
db_octal   = dict((digit, ord(digit) - ord("0")) for digit in "01234567")
db_decimal = dict((digit, ord(digit) - ord("0")) for digit in "0123456789")
db_hex     = dict((digit, ord(digit) - ord("0")) for digit in "0123456789")
db_hex.update((digit, ord(digit) - ord("a") + 10) for digit in "abcdef")
db_hex.update((digit, ord(digit) - ord("A") + 10) for digit in "ABCDEF")

def __get_base_an_digit_db(fh):
    global db_binary
    global db_octal
    global db_decimal
    global db_hex

    pos   = fh.tell()
    first = fh.read(1)
    if first == "0":
        second = fh.read(1)
        if   second == "x": return 16, db_hex
        elif second == "o": return 8,  db_octal
        elif second == "b": return 2,  db_binary

    fh.seek(pos)
    return 10, db_decimal


