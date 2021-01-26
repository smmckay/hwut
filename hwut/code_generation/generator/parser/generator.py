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
import hwut.temporal_logic.parser.lexical_analysis     as     T
from   hwut.code_generation.function_stubs.c.core      import extract_argument_list
from   hwut.code_generation.generator.dependency_db    import DependencyDb
from   hwut.code_generation.generator.types            import E_Generator
from   hwut.code_generation.generator.parser.parameter import skip_whitespace_in_line, \
                                              check, \
					      check_newline, \
                                              value_type_fit, \
                                              parse_constant, \
                                              parse_selection, \
                                              parse_range, \
                                              parse_user_code
from   hwut.code_generation.generator.generator import Generator, \
                                                       GeneratorContantLines
import sys

def do(fh):
    parameter_db = parse_header(fh)

    section_list = []
    while not is_dash_line(fh):
        if is_empty_line(fh): continue
        if is_end_of_file(fh): break
        parameter_list, constraint_list = parse_line(fh, parameter_db)
        if len(parameter_list) == 0: continue

        dependency_db = DependencyDb(parameter_list)
        circularity   = dependency_db.get_circularity()
        if circularity is not None:
            print "Error: circularity:", circularity
            sys.exit()

        section_list.append(Generator(parameter_list, constraint_list, 
                                      dependency_db))
    fh.readline()

    # All parameters with the same name/index must have the same value type.
    # For example, one cannot mix 'integer' and 'string' parameters.
    for g in section_list:
        for p in g.parameter_list:
            p.value_type = parameter_db[p.index].global_value_type

    # Combine 'plain constant value' lines into a more efficient generator.
    extract_plain_constant_generators(section_list)

    # Check whether the parameter have consisting types. For example if 'z'
    # appears as a string somewhere it cannot appear as an integer somewhere 
    # else.
    check_consistency(parameter_db, section_list)

    return section_list

def parse_header(fh):
    """EXAMPLE:

       int x; float y; const char* name; ptrdiff_t length; bool return;

       Record seperator:  ';' 
       Line separator:    '\n' 

       Newline suppressor '\' lets continue in next line.
    """
    argument_list_str = ""
    while 1 + 1 == 2:
        line = fh.readline()
        if len(line) == 0: 
            break
        line = line.strip()
        if   len(line) == 0: 
            continue
        elif line[-1] != "\\":
            argument_list_str += line
            break
        else:
            line = line[:-1] 
            argument_list_str += line

    if len(argument_list_str) == 0:
        print "Missing header definition;"

    # map: parameter index --> (name, type)
    parameter_db = extract_argument_list(argument_list_str, Delimiter=";")
    for p in parameter_db:
        p.global_value_type = None

    return parameter_db

def parse_line(fh, parameter_db):
    """Parse a line consisting of parameters and possibly constraint.
       EXAMPLE:

            3.14213;  |1:2|; ["otto", "friedhelm"]; { 0x5A, 0xFF, 0xFE };
       
       Newline suppressor '\' lets continue in next line.
    """
    parameter_list  = []
    constraint_list = []
    
    while parse_line_element(fh, parameter_db, parameter_list, constraint_list):
        # 'check' calls 'skip_whitespace_in_line' which skips the newline
        # if it is preceeded by '\'.
        if is_end_of_file(fh): break
        if check_newline(fh):  break

    if len(parameter_list) == 0:
        print "Error: no definition found in line."
        print "Error: '%s'" % fh.readline().replace("\n", "")
        sys.exit()

    return parameter_list, constraint_list
        
def parse_line_element(fh, parameter_db, parameter_list, constraint_list):
    """Parse the next line element. This must be either a parameter or 
    a constraint. 
    """
    for i, func in enumerate([parse_constant, 
                              parse_selection, 
                              parse_range, 
                              parse_user_code]): 
        
        found = func(fh)
        if found is None: 
            continue

        elif func != parse_user_code:
            if len(parameter_list) > len(parameter_db):
                print "Error: too many parameters described."
            index = len(parameter_list)
            info  = parameter_db[index]
            info.global_value_type = value_type_fit(info.global_value_type, 
                                                    found.value_type)
            found.specify(index, info.name, info.type)
            parameter_list.append(found)
        else:     
            constraint_list.append(found)

        if not check(fh, ";"):
            print "Error: missing ';' after parameter. Found '%s'. " % fh.read(5)

        return True

    return False
          
def extract_plain_constant_generators(GeneratorList):
    """Extracts those generators which consists of plain constant parameter 
    settings and combines them into a single generator which iterates over
    lines of settings.
    """
    setting_list = []
    i            = len(GeneratorList) - 1
    while i >= 0: 
        generator = GeneratorList[i]
        if generator.constraint_list: 
            pass # not 'continue'
        elif generator.parameter_list_is_constant():
            setting_list.append(generator.parameter_list)
            del GeneratorList[i]
        i -= 1

    setting_list.reverse()

    if len(setting_list) != 0:
        GeneratorList.append(GeneratorContantLines(setting_list))
        

def check_consistency(parameter_db, GeneratorList):
    value_type_list = None
    for generator in GeneratorList:
        generator.check_consistency(parameter_db)
    
def snap_line(fh):
    """Snaps at least two '-' signs, but as many as there are.
    """
    pos = fh.tell()
    if not check(fh, "-"):
        return None

    tmp = fh.read(1)
    while tmp == "-":
        tmp = fh.read(1)
        if tmp == "-": continue
        elif not tmp:  return None

    return tmp

def is_dash_line(fh):
    """A line that starts with three or more '-'.
    """
    pos = fh.tell()
    line = fh.readline()
    fh.seek(pos)
    return line.strip().find("---") == 0 

def parse_dash_line_special(fh):
    """Snap:
                ---// IDENTIFIER //------------

       RETURNS: The found IDENTIFIER, if the pattern of the line fits.
       
       Otherwise, the stream is set back to where it started to parse.
    """
    pos = fh.tell()
    skip_whitespace_in_line(fh)
   
    end_marker = snap_line(fh)
    if end_marker is None:                        fh.seek(pos); return None
    elif end_marker != "/" or not check(fh, "/"): fh.seek(pos); return None

    skip_whitespace_in_line(fh)
    identifier = T.identifier(fh)
    if identifier.error():                        fh.seek(pos); return None                   
    identifier = identifier.content
    skip_whitespace_in_line(fh)

    if   not check(fh, "//"):                     fh.seek(pos); return None
    elif snap_line(fh) is None:                   fh.seek(pos); return None

    return identifier

def is_empty_line(fh):
    """A line that starts or ends with '##', or is full of whitespace.
    """
    pos  = fh.tell()
    line = fh.readline()
    if not line: 
        return False
    line = line.strip()
    if len(line) == 0:
        return True
    elif line.find("##") == 0 or line.rfind("##") == len(line) - 2:
        return True
    fh.seek(pos)
    return False 
    
def snap_until_dash_line(fh):
    txt = []
    while not is_dash_line(fh):
        line = fh.readline()
        if len(line) == 0: print "Error: missing dashline"
        txt.append(line)    
    fh.readline()
        
    return "".join(txt)

def find_dash_line(fh):
    while not is_dash_line(fh):
        tmp = fh.read(1)
        if len(tmp) == 0: print "Error: missing dashline"
        fh.seek(-1, 1)
    fh.readline()

    return

def get_marker_content(line, marker, N):
    idx   = line.find(marker)
    begin = idx + len(marker)
    end   = line.find(">>", begin)
    if end == -1: 
        print "Error: missing closing '>>'"
        return None

    plain_content = line[begin:end].strip()
    content       = plain_content.split()
    if len(content) != N:
        print "Error: '%s' requires %i arguments. Received %i." % (marker, N, len(content))
    return content
    
def is_end_of_file(fh):
    pos = fh.tell()
    if not fh.read(1): return True
    fh.seek(pos)
    return False
