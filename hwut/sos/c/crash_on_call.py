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
import hwut.common                as common
import hwut.auxiliary.file_system as fs
import hwut.auxiliary.path        as path

import os
from   itertools import chain


__name_db = {} # FunctionSet --> crash-on-call file name that has been generated

def init():
    """Before analysis, the old 'crash-on-call' file needs to be deleted. Otherwise
    it might be considered for analysis.
    """
    global __name_db
    fs.try_remove_glob("%s*.[co]" % common.HWUT_FILE_STEM_CRASH_ON_CALL)
    __name_db.clear()

def do(assembler, R):
    """RETURNS: [0] Unresolved reference (should be empty!)
    """
    unresolved_set = set()
    previous       = 1
    while previous != unresolved_set:
        previous = unresolved_set

        dummy,          \
        unresolved_set, \
        dummy           = assembler.compile_and_link(R.source_file_list, 
                                                     R.object_file_list, 
                                                     R.library_file_list)

        if not unresolved_set: break

        R.source_file_list.add(
            do_core(unresolved_set)
        )

    return unresolved_set

def do_core(FunctionSet):
    """Provides a source file that implements the crash-on-call functions for 
    a given set of undefined functions. 

    If the file has not yet been written, the 'writer' is called that writes 
    it.

    RETURNS: File name of the crash-on-call file.
    """
    file_name, implemented_f = get_file_name(FunctionSet)
    if implemented_f:
        return file_name

    fh = fs.open_or_die(file_name, "wb")
    write(fh, FunctionSet)
    fh.close()
    return file_name

def write(fh, FunctionSet):
    assert type(FunctionSet) == set

    fh.write(
        "/*_____________________________________________________________________________\n"
        " *\n"
        " * Crash-on-Call Stubs: (HWUT - generated code)\n"
        " *\n"
        " * This module implements functions which are supposed to crash upon call.\n"
        " * Their function signature differs (most probably) from the original one,\n"
        " * but this is not an issue for the linker--IT WILL LINK ANYWAY!\N"
        " *\n"
        " * If the function call does not cause a crash, then the 'exit()' call ensures\n"
        " * that the program will exit. Crash-on-call stubs are ONLY to be used for\n"
        " * functions that are absolutely not related to the unit under test.\n"
        " *\n"
        " * Make sure that the test program makes a 'printf(\"<termination>\n\");' call\n"
        " * right before officially terminating. Otherwise, HWUT might not detect\n"
        " * premature terminations.\n"
        " *\n"
        " * To comply with some pedantics, prototypes are given before definitions.\n"
        " *___________________________________________________________________________*/\n"
        "#include \"stdlib.h\"\n"
        "#include \"stdio.h\"\n"
        "\n"
        "/* Prototypes                                                                */\n"
        "static void self_crash_on_call_print(const char* N);\n"
    )

    for function in sorted(FunctionSet):
        fh.write("void %s(void);\n" % function)

    fh.write(
        "\n"
        "/* Definitions                                                               */\n"
    )
    fh.write(
        "static void self_crash_on_call_print(const char* N) {\n"
        "    printf(\"Unexpected call to '%s' -- abort!\", N);\n"
        "}\n"
    )
    for function in sorted(FunctionSet):
        fh.write("void %s(void) { self_crash_on_call_print(\"%s\"); exit(-1); }\n" % (function, function))

def get_file_name(FunctionSet):
    """RETURNS: [0] Name of the file that implements crash-on-call for the
                    given function set. 
                [1] True, if the file has already been written.
                    False, if not.
    """
    global __name_db

    def suffix(N):
        if N == 0: return ""
        else:      return "-%i" % N

    function_set_id = tuple(sorted(FunctionSet))

    file_name = __name_db.get(function_set_id)
    
    if file_name is not None:
        return file_name, True

    new_index     = len(__name_db)
    file_name     = "%s%s.c" % (common.HWUT_FILE_STEM_CRASH_ON_CALL, 
                                suffix(new_index))
    __name_db[function_set_id] = file_name

    return file_name, False

