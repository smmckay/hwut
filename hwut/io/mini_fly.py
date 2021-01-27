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
# Implementation of a small subset of the 'fly' language.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
def skip_whitespace(fh):
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if   not tmp:           break
        elif not tmp.isspace(): fh.seek(-1, 1); break
        
def is_struct_begin(fh):
    return check(fh, "{")

def is_struct_end(fh):
    return check(fh, "}")

def check(fh, Delimiter):
    """RETURNS: True  -- if the first non-whitespace character that follows
                         is equal to 'Delimiter'.
                False -- else.
    """ 
    skip_whitespace(fh)
    tmp = fh.read(1)
    if not tmp: 
        return False
    elif tmp == Delimiter:
        return True
    else:
        fh.seek(-1, 1)
        return False

letter_set = set("_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

def read_label(fh):
    """RETURNS: string -- the label that has been found.
                None   -- No label has been found.
    """
    global letter_set

    skip_whitespace(fh)
    txt = ""
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if not tmp:                 return None
        elif tmp not in letter_set: break
        txt += tmp

    if tmp != ":": return None
    elif not txt:  return None # Label of length 0 it not a label
    else:          return txt

def read_string_trivial(fh):
    """Parse a string terminated by ';'. Semi-colons inside the string
    are backslashed, i.e. preceeded by '\\'. Double backslashes are 
    backslashes.

             \;   -->   ;
             \[   -->   [

    NOTE: The '\\' element is not part of 'fly'. It is implemented here
          to avoid '{^ ... '^}' comments.

    RETURNS: string -- the trivial string.
             None   -- no string terminated with ';' has been found. 
    """
    skip_whitespace(fh)
    pos = fh.tell()
    txt = ""
    backslash_f = False
    while 1 + 1 == 2:
        tmp = fh.read(1)
        if tmp == "\\": 
            if backslash_f: txt += "\\"
            backslash_f = not backslash_f
        elif tmp == "[" and backslash_f: 
            txt += "["
        elif tmp == ";" and not backslash_f: 
            return txt
        elif not tmp:           
            fh.seek(pos)
            return None
        else:               
            backslash_f = False
            txt += tmp
    
    assert False

def read_list(fh):
    """RETURNS: List -- containing the objects listed in the list
                None -- no list has been found.
    """
    pos = fh.tell()
    if not check(fh, "["):
        return None
    result = []
    while 1 + 1 == 2:
        if check(fh, "]"):
            break
        value = read_string_trivial(fh)
        if value is None: 
            print "Error: in '.fly' file--missing string."
            fh.seek(pos)
            return None

        result.append(value)
    return result

def read_list_list(fh, N):
    """RETURNS: A list of lists where each sub list has 'N' elements.
                None -- if there was nothing that matches that.
    """
    pos = fh.tell()
    if not check(fh, "["):
        return None
    result = []
    while 1 + 1 == 2:
        if check(fh, "]"):
            break
        x = read_list(fh)
        if x is None:     
            print "Error: missing sub list"
            return None
        elif len(x) != N: 
            print "Error: fly file--sub list was not of size '%i'" % N
            return None
        result.append(x)
    return result

def read_struct_list(fh):
    """RETURNS: Dictionary where each value is a list of strings.
       
    EXAMPLE: '{ name1: [ x; y; z; ] name2: [ a; b; c ] }'
    """
    pos = fh.tell()
    if not is_struct_begin(fh): return None

    result = {}
    while not is_struct_end(fh):
        label = read_label(fh)
        if label is None: fh.seek(pos); return None

        value_list = read_list(fh)
        if value_list is None: fh.seek(pos); return None

        result[label] = value_list

    return result

def write_list(ValueList):
    return "".join([
        "[ ", 
        "".join("%s " % write_string_trivial(x) for x in ValueList),
        "]"
    ])
        
def write_list_list(ListList, N):
    return "".join([
        "[\n", 
        "".join("  %s\n" % write_list(x) for x in ListList),
        "]"
    ])

def write_struct_list(DictList):
    txt = [ "{\n" ]
    txt.extend(
        "%s: %s\n" % (key, write_list(value_list))
        for key, value_list in DictList.iteritems()
    )
    txt.append("\n}\n")
    return "".join(txt)
        
def write_string_trivial(Value):
    if   Value is None:                         Value = "None"
    elif not isinstance(Value, str): Value = "%s" % repr(Value)

    return "%s;" % str(Value.lstrip().replace("\\", "\\\\").replace(";", "\\;").replace("[", "\\["))
