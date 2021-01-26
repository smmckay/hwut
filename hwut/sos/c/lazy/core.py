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

import hwut.sos.c.core          as     sos
import hwut.sos.c.result        as     result
from   hwut.sos.c.assembler     import Assembler
from   hwut.sos.c.filesystem_db import FileSystemDb
import hwut.sos.c.crash_on_call as     crash_on_call

import hwut.auxiliary.path        as path         
import hwut.auxiliary.file_system as fs         

import os
from   itertools import chain
from   copy      import deepcopy
import tempfile

def do(Setup):
    """Analyzes a given SourceFile and extracts the implemented functions. The
    functions are distinguished according to their being externally linked or
    statically. Next, include directories and references are determined so that
    the build environment can be setup. 

    For each function in the file, there is a test file template setup in C.
    Then, a Makefile is written which enables the build of all tests including
    all required links. 
    """
    SourceFile            = Setup.first_argument
    filesystem_db         = FileSystemDb.from_Setup(Setup)
    assembler             = Assembler.from_Setup(Setup, filesystem_db)
                          
    R                     = analyze(assembler, filesystem_db, SourceFile)

    include_header_list   = assembler.compiler.get_include_headers(SourceFile)

    extern_function_list, \
    static_function_list  = assembler.compiler.get_function_info(SourceFile)

    extern_test_list,     \
    static_test_list      = write_tests(extern_function_list, 
                                        static_function_list, 
                                        include_header_list,
                                        SourceFile)

    write_Makefile(Setup.output_makefile, 
                   assembler, SourceFile,  
                   extern_test_list, static_test_list, R)

    assembler.clean_up()

def analyze(assembler, filesystem_db, SourceFile):
    tmp_file_name = tempfile.mktemp(".c", dir="./")

    # Create a dummy file that implements 'main()'.
    fh = fs.open_or_die(tmp_file_name, "wb")
    fh.write("int main(int argc, char** argv) { return 0; }\n")
    fh.close()

    assembler.compiler.trash.add(tmp_file_name)

    R = sos.analyze(assembler, filesystem_db, [tmp_file_name, SourceFile])
    R.source_file_list.discard(tmp_file_name)
    return R

def write_Makefile(MakefileName, assembler, SourceFile, extern_list, static_list, R):
    """Writes a Makefile which can build all tests. The tests are given in 

       -- extern_list, containing the file names of tests for externally 
                       linked functions. 

       -- static_list, containing the file names of tests for statically 
                       linked functions. 
    """
    result.init_construction(["INCLUDES", "LIBRARIES", "LIBDIRS", "OBJECTS"])
    crash_on_call.init()

    assembler.compiler.do_list(extern_list)
    extern_build_list = [
        sos.setup_build(assembler, 
                        path.replace_extension(file_name, ".exe"), 
                        R, ExtraSources=[ file_name, SourceFile ]) 
        for file_name in extern_list
    ]

    # Make sure, that the source file is not linked against the application
    # for static functions.
    R.source_file_list.discard(SourceFile)

    assembler.compiler.do_list(static_list)
    static_build_list = [
        sos.setup_build(assembler, 
                        path.replace_extension(file_name, ".exe"), 
                        R, ExtraSources=[ file_name ]) 
        for file_name in static_list
    ]

    result.write_makefile(MakefileName, 
                          extern_build_list + static_build_list)

def write_tests(ExternFunctionList, StaticFunctionList, IncludeHeaderList, SourceFile):
    """SourceFile -- the file for which Unit Test templates shall be written.

    This function analysis the functions present in 'SourceFile'.  For each
    of the functions it develops a hwut-style test source file.  It
    distinguishes between externally linked functions and static functions.
    Static functions are tested with the source file included on top. The
    according test files end with '-static' before the extension.

    RETURNS: [0] List of generated test file names for externally linked funcs.
             [1] List of generated test file names of static funcs.
             
    """
    assert type(IncludeHeaderList) == list

    extern_test_list = [
        get_test_file(SourceFile, function, IncludeHeaderList)
        for function in ExternFunctionList
    ]

    # Static functions need to include the source file.
    included_header_list = IncludeHeaderList + [ SourceFile ]

    static_test_list = [
        get_test_file(SourceFile, function, included_header_list, "-static")
        for function in StaticFunctionList
    ]

    return extern_test_list, static_test_list

def get_test_file(SourceFile, FunctionName, IncludeHeaderList, Suffix=""):
    """Write a basic template test file.

    RETURNS: File name of the generated test files.
    """
    global template_txt

    file_name = "test-%s%s.c" % (FunctionName, Suffix)
    fh        = fs.open_or_die(file_name, "wb")

    include_txt = "".join(
        "#include \"%s\"\n" % h for h in IncludeHeaderList
    )

    txt = template_txt.replace("INCLUDES", include_txt) 
    txt = txt.replace("FUNCTION",          FunctionName) 
    txt = txt.replace("SOURCE",            os.path.basename(SourceFile))

    fh.write(txt)
    fh.close()
    return file_name
        
template_txt = """
/* PURPOSE: 
 *
 *    Test template for function: SOURCE/FUNCTION
 *
 * This file contains an auto-generated template by the HWUT Unit Test Tool.
 * It is advised to answer the following questions in the initial comment.
 *
 *              WHAT DOES THE FUNCTION?
 *              WHAT ARE INPUTS, OUTPUTS, HISTORY DEPENDENCIES?
 *              WHY IS THIS TEST CONSIDERED TO BE SUFFICIENT?
 *
 * Also, it is good to mentione references to research or requirement docs.
 *
 * AUTHOR: Name and/or Email
 * ORGANIZATION
 * DATE or HISTORY
 *___________________________________________________________________________*/

#include "hwut_unit.h"
#include "stdio.h"

INCLUDES

/* It is good style to build the sets on a set of functions for the following
 * tasks:                                                                    */

static void setup(void); /* A function that makes the test independent from 
                          * any history or external influences.              */
static void print(void); /* A function that prints the unit under test or the 
                          * functions input/output.                          */
static void test(int);   /* A function which executes the test. That is, it
                          * sets it up, applies inputs, and prints output.   */

int
main(int argc, char** argv)
{
    /* Refer to the function name, so that it is recognized as an
     * unresolved symbol and the code generator will try to resolve it.      */
    void*  dummy = FUNCTION;

    hwut_info("SOURCE: FUNCTION;\\n"
              "CHOICES: One, Two, Three;\\n");

    hwut_if_choice("One") {
        test(1);
    }
    hwut_if_choice("Two") {
        test(2);
    }
    hwut_if_choice("Three") {
        test(3);
    }
}

static void
test(int N)
{
    (void)N;
    setup();

    /* Test FUNCTION */

    print();
}

static void 
setup(void)
{
}

static void 
print(void)
{
}
"""

