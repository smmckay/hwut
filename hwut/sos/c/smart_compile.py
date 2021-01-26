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
from   hwut.sos.c.output_interpreter  import detect_missing_include_headers, \
                                             detect_mentioned_headers, \
                                             detect_undeclared_identifiers
from   hwut.sos.c.system              import try_preprocess, \
                                             try_compile
import os

def do(SourceFile, include_dir_db, AddCompileFlagList):
    """Tries to compile the given file name and determines the missing include
    header directories. This function does NOT link.

    Compilation fails, as long as name declarations are missing.
    Compilation, however, does not require all references to be
    implemented.

    RETURNS: [0] OutputFileName
                 None -- if no working compilation environment was found.

             [1] Unfound header files.

             [2] Compilation output

    ADAPTS:  include_dir_db --> new include paths

    If 'OutputFileName' is not None, then the compilation was succesful.
    """
    assert isinstance(SourceFile, (str, unicode))

    missing_set = do_preprocess(SourceFile, include_dir_db, AddCompileFlagList)
    if missing_set:
        txt = "missing headers:\n%s" % "".join("   %s\n" % h for h in sorted(missing_set))
        return None, missing_set, txt

    return __apply_compiler(SourceFile, include_dir_db, AddCompileFlagList)

def do_preprocess(SourceFile, include_dir_db, AddCompileFlagList):
    """Use C-Preprocessor to determiens include directories required for 
    'SourceFile' and stores them in the 'include_dir_db'. Using the
    preprocessor is faster than repeated calling the compiler.

    NOTE:   Headers in the current directory might be left out!

    RETURN: Set of missing headers.
    """
    prev_header_set = False
    header_set      = True
    while prev_header_set != header_set:
        prev_header_set = header_set

        header_set = do_get_mentioned_headers(SourceFile, include_dir_db, 
                                              AddCompileFlagList)

        # Find the missing headers in the filesystem.
        # => update content of 'include_dir_db'.
        missing_header_set = include_dir_db.determine_directories(header_set, 
                                                                  SourceFile)
        if missing_header_set: 
            break # Not all include headers have been found; Abort!

    return missing_header_set

__memoize_header_db = {}
def do_get_mentioned_headers(SourceFile, IncludeDirDb, AddCompileFlagList):
    global __memoize_header_db
    entry = __memoize_header_db.get(SourceFile)
    if entry is None: 
        include_dir_set = IncludeDirDb.get_directories(SourceFile)
        output          = try_preprocess(SourceFile, include_dir_set, 
                                         AddCompileFlagList)
        entry = detect_mentioned_headers(output, SourceFile)
        __memoize_header_db[SourceFile] = entry
    return entry

def __apply_compiler(SourceFile, include_dir_db, AddCompileFlagList):
    """Compile (but not link) the given source file. The 'include_dir_db'
    is occasionally adapted, if new headers are required. 

    RETURNS: [0] object file
                 None -- in case of failure 

             [1] missing header list.

             [2] compilation output
    """
    prev_header_set = True
    header_set      = False
    while prev_header_set != header_set:
        prev_header_set = header_set

        include_dir_set     = include_dir_db.get_directories(SourceFile)

        object_file, output = try_compile(SourceFile, include_dir_set, 
                                          AddCompileFlagList)

        header_set          = set(detect_missing_include_headers(output).keys())
        undeclared_set      = set(detect_undeclared_identifiers(output))
        missing_header_set  = include_dir_db.determine_directories(header_set, 
                                                                   SourceFile)

        if object_file is not None:
            break

    return object_file, missing_header_set, output

