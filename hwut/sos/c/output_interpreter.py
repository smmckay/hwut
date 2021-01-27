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
import hwut.common as common

import re
import os
from   collections import namedtuple, \
                          defaultdict

re_quoted           = re.compile("`([^']+)'")
re_line_number      = re.compile('([0-9]+):')
re_missing_included = re.compile('error *: *([^: ]+) *:')
re_missing_lib      = re.compile('ld: *cannot +find + -l([^\\n ]+)')
re_implemented      = re.compile('[0-9a-fA-F]+ +T +([^ ]+)')   # 'T' - symbol in text
re_static           = re.compile('[0-9a-fA-F]+ +t +([^ ]+)')   # 't' - static (internally)
re_unresolved       = re.compile(' +U +([^ ]+)')               # 'U' - unresolved
re_first_file_name  = re.compile('^(.?[^.:]+.[^:]+)')

ReferenceLocation   = namedtuple("ReferenceLocation", ("file_name", "function"))

def detect_mentioned_headers(Output, SourceFile):  
    """Interprets the output of the preprocessor in order to determine the
    set of mentioned header files. 

    PATTERN: 
        hello.o: ../../../../src/hello.c \
         ../../../../src/print.h \
         ../../../../../component_framework/greet.h \
         world.h \

    RETURNS: Set of basenames of header files.
    """
    source_file = os.path.basename(SourceFile)
    index = Output.find(source_file)
    if index == -1: return set()

    remainder_index = index + len(source_file)
    if remainder_index >= len(Output): return set()

    def iterable(Remainder):
        for line in Remainder.split("\\"):
            line = line.strip()
            if not line: continue
            for name in line.split():
                basename = os.path.basename(name)
                if basename: yield basename

    return set(iterable(Output[remainder_index:]))


def detect_undeclared_identifiers(CompileOutput):
    """Consider the compilation output and find undeclared identifiers.

    Pattern:
    
       FILE-NAME ':' N : N ': error: unknown type name' 'X' ...
       FILE-NAME ':' N : N ': error: 'VariableName' undeclared  ...
       FILE-NAME ':' N : N ': warning: implicit declaration of function 'FuncName' ...

    RETURNS: 
    
       map: set of undeclared identifiers
 
    """
    re_undeclared_type     = re.compile("error: +unknown +type +name '([^']+)'")
    re_undeclared_variable = re.compile("error: +'([^']+)' +undeclared")
    re_undeclared_function = re.compile("warning: +implicit +declaration +of +function +'([^']+)'")

    result = set()
    for line in CompileOutput.splitlines():
        for regex in (re_undeclared_type, re_undeclared_variable, 
                      re_undeclared_function):
            match = regex.search(line)
            if match is None: continue
            identifier = match.groups()[0]
            result.add(identifier)
            break

    return result

def detect_missing_include_headers(CompileOutput):
    """Consider the compilation output and find missing header files. 

    Pattern:
    
       FILE-NAME ':' ... ':' HEADER-FILE-NAME ':' 'No such file or directory'

    RETURNS: 
    
       map: header-file --> (including file, line-number string)
 
    """
    if CompileOutput.find("no input files") != -1: 
        return {}

    def key_location_iterable(output):
        """YIELDS: (Header file name, (referring file, line number))
        """
        marker = "No such file or directory"
        for line in output.splitlines():
            verdict, including_file, remainder = inspect_line(line, marker)
            if not verdict: continue
            match = re_line_number.search(remainder)
            if match is not None: line_n_str = match.groups()[0]
            else:                 line_n_str = "<unknown>"
            
            match = re_missing_included.search(remainder)
            if match is None: continue
            
            included_file = match.groups()[0]
            yield included_file, (including_file, line_n_str)

    return get_key_collection(key_location_iterable(CompileOutput))
    
def detect_missing_library_file_stems(LinkOutput):
    """Consider the link output and find missing library files. 

    Pattern:
    
       "ld:" "cannot" "find" "-l" + LIBRARY-NAME 

    RETURNS: List of library files stems of the for 'libXXX' 
    
    Suffixes may depend on operating system, e.g. '.a' or '.so'
    on Unix and '.lib' and '.dll' on windows and the like.
    """
    def iterable(output):
        """YIELDS: (Header file name, (referring file, line number))
        """
        marker = "cannot"
        for line in output.splitlines():
            match = re_missing_lib.search(line)
            if match is None: continue 
            library_short_name = "lib%s" % match.groups()[0]
            yield library_short_name

    return [ file_stem for file_stem in iterable(LinkOutput) ]

def detect_implemented_references(NmOutput):
    """Considers the output of the 'nm' command to detect the implemented
    references of an object file. 
    
    RETURNS: [0] Externally visible functions.
             [1] Unresolved symbols.
             [2] Internal (static) functions.

    The 'ImplementedList' is the list of reference which are implemented in the
    object file. The 'Unresolved' tells what references are required from 
    other modules.
    """
    if not NmOutput: return [], [], []

    implemented_list = []
    static_list      = []
    unresolved_list  = []
    for line in NmOutput.splitlines():
        for container, regex in ((implemented_list, re_implemented), 
                                 (static_list,      re_static),
                                 (unresolved_list,  re_unresolved)):
            match = regex.search(line)
            if match is None: continue
            identifier = match.groups()[0]
            if   identifier.startswith("_GLOBAL__sub_"): continue
            elif identifier == ".text":                  continue
            container.append(identifier)
            break

    # No longer necessary with the '-C' option of 'nm'
    # def windowish(Reference):
    #     """On Windows, there might be a leading '_' stuck in front of the 
    #    reference name.
    #    """
    #    if Reference and Reference[0] == "_": return Reference[1:]
    #    else:                                 return Reference
    #
    #if common.is_windows():
    #    implemented_list = [ windowish(ref) for ref in implemented_list ]
    #    unresolved_list  = [ windowish(ref) for ref in unresolved_list ]

    return implemented_list, unresolved_list, static_list

def detect_missing_references(LinkOutput):
    """Considers linking output and extracts names of missing references.
    
    Pattern:
    
                            C-FILE-NAME ':' ... 'undefined reference to' FUNCTION-NAME
       OBJECT-FILE-NAME ':' C-FILE-NAME ':' ... 'undefined reference to' FUNCTION-NAME
    
    
    RETURNS: 
    
       map:   reference --> (file name, function name)
          
  
    That is, the dictionary maps from an unresolved object to the file name
    and the function where it has been referred.
    """
    def key_location_iterable(output):
        """YIELDS: (reference, (file-name, function-name))
        """
        last_function_mentioned = "<unknown>"
        for line in output.splitlines():
            function_name = inspect_function_note(line)
            if function_name is not None: 
                last_function_mentioned = function_name
                continue

            reference, file_name = extract_reference_file_name(line)

            if reference is None: continue
            yield reference, ReferenceLocation(file_name, last_function_mentioned)

    return get_key_collection(key_location_iterable(LinkOutput))

def inspect_function_note(Line):
    """Tries to find the mentioning of a function in a given line. 
    
    RETURNS: (Verdict, Function name)
    """
    Marker = "In function"

    verdict, dummy, dummy = inspect_line(Line, Marker)
    if not verdict: return None
    
    match = re_quoted.search(Line)
    if match is None: return None
    function_name = match.groups()[0]
    
    return function_name
        
def inspect_line(Line, Marker):
    """Searches for string 'Marker' in the line. Also, determines the concerned
    file as being given by the name at the beginning of the line until ':'.
    
    RETURNS: (Verdict, Referred File Name, Remaining line after ':')
    """
    if Line.find(Marker) == -1: return (False, "<no file>", "")
    i = Line.find(":")
    if i == -1: return (True, "<no file>", Line)
    referred_file = Line[:i]
    return (True, referred_file, Line[i:]) 

def get_key_collection(KeyValueIterable):
    """RETURNS: Dictionary, that maps
    
          key --> list of values which appear in pair with 'key'
       
    The 'key' may be an undefined reference, or header file that could not be
    found. The file list may be the list of files that require the reference, 
    or the list of files that tries to include the header.   
    """
    result = defaultdict(set)               
    for key, value in KeyValueIterable:
        result[key].add(value)
    return result

def on_error(MissingReferenceList, impossible_list):
    print "Error: analysis did not result in working compilation instructions."
    if impossible_list:
        print "Error: following modules could not possibly be compiled:"
        for file in impossible_list:
            print "Error:  %s" % file
    
    if MissingReferenceList:
        print "Error: following references could not be found:"
        for file in MissingReferenceList:
            print "Error:  %s" % file

def extract_reference_file_name(Line):
    marker    = "undefined reference to"
    file_name = None
    line      = Line
    notion_n  = 0
    while line:
        x = re_first_file_name.search(line)
        if x is None: break
        file_name = x.groups()[0]
        L         = len(file_name)
        line      = line[L:]
        if file_name.find(".c") == L - 2:
            break
        elif line and line[0] == ":":
            line      = line[1:]
            notion_n += 1
            if notion_n > 1: break
        else:
            break

    if file_name is None: 
        return None, None

    elif Line.find(marker) == -1: 
        return None, None 

    match = re_quoted.search(line)
    if match is None: 
        return None, None
    
    reference = match.groups()[0]
    return reference, file_name

