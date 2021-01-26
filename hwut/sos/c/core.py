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
"""PROCESS:

       SOURCES TO         :        ,----------------------------------------------.     
      BE COMPILED         |        |               DIRECTORY SEARCH               |
           |              |        '----------------------------------------------'
           |              |                 :             :              :
           |              |<===== OR ======>|             |              |
           |              |                 |             |              |
           |              |               found         found          found 
           |              |            source files   libraries     object files
           |              |                 |             |              |
           |              |                 |             |              |
         SMART          CTAGS:            SMART           |              |
      COMPILATION    search source     COMPILATION        |              |
           |        files and find          |             |              |
           |          references            |             |              |
        derived           |              derived          |              |
      object file         |            object files       |              |
           |              |                 |             |              |                        
          get             |                 |             |              |                        
       unresolved         |                get           get            get
       references         |             references    references     references
           |              :                 :             :              :
           |        ,------------------------------------------------------------.     
           |        |                IMPLEMENTATION DATABASE                     |
           |        |            What references can be found where?             |
           |        '------------------------------------------------------------'
           |                               |
           '-----------------------.       |<--------------.
                                   |       |               |
                                RESOLVE UNRESOLVED         |
                                   REFERENCES              |
                                       |            undone |
                                       +-------------------'
                                       |              
                                       |        
                           .-----------------------.
                           | SET OF REQUIRED FILES |
                           '-----------------------'
                                       |
                                       :
                                 Write Makefile

SMART COMPILATION: 

  --> include_dir_db: Header file --> directory from where it is taken.
  --> object_file:    Name of the generated object file.

  This process applies a pure compilation.

RESOLVE UNRESOLVED REFERENCES:

  --> library_dir_db: Library file --> directory from where it is taken.

  Selects files from implementation database in order to access resolve
  unresolved references.

  This process performs a linking operation.

_______________________________________________________________________________

AUTHOR: Frank-Rene Schaefer
_______________________________________________________________________________
"""

from   hwut.sos.c.assembler         import Assembler
from   hwut.sos.c.filesystem_db     import FileSystemDb
from   hwut.sos.c.implementation_db import ImplementationDb
from   hwut.sos.c.declaration_db    import DeclarationDb
import hwut.sos.c.result            as     result
import hwut.sos.c.crash_on_call     as     crash_on_call

import hwut.common                  as     common
import hwut.auxiliary.file_system   as     fs
import hwut.auxiliary.executer      as     executer
import hwut.auxiliary.path          as     path

import os
import sys
import tempfile
from   copy         import copy
from   collections  import defaultdict, \
                           namedtuple
from   glob         import glob
from   itertools    import chain
from   operator     import itemgetter
from   copy         import deepcopy

def do(Setup):
    # -- Filesystem Database:
    #    Source files, header files, library files, and object files. 
    #
    filesystem_db = FileSystemDb.from_Setup(Setup)
    assembler     = Assembler.from_Setup(Setup, filesystem_db)


    test_source_file_list,   \
    support_source_file_list = setup_application_and_sources(Setup, assembler)
    if not test_source_file_list:
        print "Error: no source file implementing a 'main()' function."
        return

    do_core(test_source_file_list, support_source_file_list, 
            Setup.output_makefile, filesystem_db, assembler)

def do_initialization_help(Setup):
    """Implement the SOSI (safe our souls initially) feature. 

        mini-Makefile:
        
           It tries to collect as many include paths as possible and 
           writes an initial mini-Makefile. The mini-Makefile has the
           sole purpose to initiate the user to have something compiling.

        default '#include'-s:

           From the given list of 'hint identifiers' it tries to 
           identify header files that might be included in order to 
           access those identifiers. Those are written on top of the
           specified source files.
    """
    if Setup.first_argument is None:
        print "Error: missing filename."
        sys.exit(-1)
    application_source = Setup.first_argument
    source_file_list   = [ application_source ] + Setup.hint_source_list 

    # mini-Makefile:
    # 
    # -- find include header files
    filesystem_db     = FileSystemDb.from_Setup(Setup, 
                                                SourceFilesAreIncludeFilesF = False,
                                                IncludeFileDbF              = True)
    include_path_list = FileSystemDb.disambiguify_all(filesystem_db.include_file_db)

    result.write_mini_makefile(Setup.output_makefile, source_file_list, include_path_list)

    return 0

    # default '#include'-s:
    #
    # -- find identifiers in header file directories.
    if filesystem_db.ctags_root_dir_list is None:
        declaration_db = DeclarationDb.without_ctags(Setup.identifier_list,
                                                     include_path_list)
    else:
        declaration_db = DeclarationDb.with_ctags(Setup.identifier_list,
                                                  include_path_list)

    __add_include_headers(source_file_list, declaration_db)

def do_core(TestSourceFiles, SupportSourceFileList, 
            MakefileName, filesystem_db, assembler):
    """Generate an application from each test source file in 'TestSourceFiles'. 
    Additionally, to the files in the filesystem_db, user specified support
    source files may be given. The 'MakefileName' says how the Makefile is
    to be named.
    """

    # -- Prepare the 'build' procedure for the Makefile
    result.init_construction(["INCLUDES", "LIBRARIES", "LIBDIRS", "OBJECTS"])
    crash_on_call.init()

    def get_build(assembler, filesystem_db, TestSourceFile, OtherSourceFileList):
        application_name = path.replace_extension(TestSourceFile, ".exe") 

        source_file_list = [TestSourceFile] + OtherSourceFileList

        R = analyze(assembler, filesystem_db, source_file_list)

        return setup_build(assembler, application_name, R) 

    build_list = [
        get_build(assembler, filesystem_db, f, SupportSourceFileList)
        for f in TestSourceFiles
    ]

    # -- Write the Makefile
    #
    result.write_makefile(MakefileName, build_list)

    assembler.clean_up()

    return 

def analyze(assembler, filesystem_db, UserSourceFileList):
    """RETURNS: Requirement -- set of required crash-on-call stubs.
                            -- set of required source files.
                            -- set of required library files.
                            -- set of required object files.
    """
    # -- Compile user's files: --> source files that cannot be compiled
    #                          --> unresolved references
    #                          --> implemented references in sources
    user_unresolved_reference_set, \
    user_implemented_reference_set = analyze_references(assembler, 
                                                        UserSourceFileList)

    R = find_references(assembler, filesystem_db, 
                        UserSourceFileList,
                        user_unresolved_reference_set, 
                        user_implemented_reference_set)


    # -- Implement the 'crash-on-calls'
    unresolved_set = crash_on_call.do(assembler, R)

    __comment_crash_on_call(unresolved_set, UserSourceFileList)

    return R

def find_references(assembler, filesystem_db, UserSourceFileList, 
                    user_unresolved_reference_set, 
                    user_implemented_reference_set):

    # -- Implementation database: What references are defined in what files?
    #
    implementation_db = setup_implementation_db(filesystem_db, assembler)

    # -- Resolve unresolved references.
    #
    R = implementation_db.find_references(user_unresolved_reference_set,
                                          user_implemented_reference_set)

    R.source_file_list.update(UserSourceFileList)

    return R

def setup_application_and_sources(Setup, assembler):
    application_source = Setup.first_argument

    user_source_file_list = [ application_source ] + Setup.hint_source_list
    if not path.verify_existence(user_source_file_list):
        sys.exit(-1)

    test_list    = list()
    support_list = list()
    for f in user_source_file_list:
        if assembler.compiler.implements_main(f): test_list.append(f)
        else:                                     support_list.append(f)

    return test_list, support_list

def setup_build(assembler, ApplicationName, R, ExtraSources=None):
    if ExtraSources is not None:
        R = deepcopy(R)
        R.source_file_list.update(ExtraSources)

    result.object_file_db.prepare(R.source_file_list)

    return result.SetupBuild.from_analysis(ApplicationName, assembler, R)

def analyze_references(assembler, user_source_file_list):
    uncompiled_source_list,   \
    unresolved_reference_set, \
    implemented_reference_set \
            = assembler.compile_and_link(user_source_file_list, [], [])

    error_f = False
    if uncompiled_source_list:
        print "Error: The following user file(s) could not be compiled."
        for file_name in sorted(uncompiled_source_list):
            info = assembler.compiler.bad_sources_db[file_name]
            missing_header_set, output = info
            print "Error: '%s'" % file_name
            if missing_header_set: 
                print "Error: Headers not found:"
                for header in sorted(list(missing_header_set)):
                    print "Error: '%s'" % header
            else:
                for line in output.splitlines():
                    print "%s" % line
        sys.exit(-1)

    if unresolved_reference_set is None:
        print "Error: initial compilation of source files failed."
        sys.exit(-1)

    return unresolved_reference_set, \
           implemented_reference_set

def setup_implementation_db(filesystem_db, assembler):
    """Prepares the implementation database that tells what references 
    are implemented in what files. If the 'ctags' utility is available, 
    then it is used to quickly find references in source files. Otherwise,
    compilation and object file investigation is applied.

    RETURNS: ImplementationDb
    """
    if filesystem_db.ctags_root_dir_list is None:
        # Reference database by compilation (a little slow).
        uncompileable_source_file_set \
                = assembler.compiler.do_list(filesystem_db.source_file_list())

        implementation_db = ImplementationDb.without_ctags(assembler, 
                                                           filesystem_db) 
    else:
        # Reference database by 'ctags' (very fast)
        implementation_db = ImplementationDb.with_ctags(assembler, 
                                                        filesystem_db) 

    return implementation_db

def __comment_crash_on_call(UnresolvedSet, UserSourceFileList):

    def print_sources(FileList):
        for file_name in FileList: 
            print "Warning: source file: '%s'" % file_name

    if UnresolvedSet:
        print_sources(UserSourceFileList)
        print "Warning: following references could not be determined."
        for reference in sorted(UnresolvedSet):
            print "Warning:   '%s'" % reference

def __add_include_headers(SourceFileList, DeclarationDb):

    include_header_txt = "".join([
        "#include \<%s\>  /* --> %s */\n" % (file_name, "".join("%s, " % i for i in identifier_list))
        for file_name, identifier_list in DeclarationDb.iteritems()
    ])

    include_header_txt = [
       "/* BEGIN -- Proposed include headers (generated by 'hwut sosi')\n"
       " *\n"
       " * PURPOSE: Try to provide the user with required header files so that initial\n"
       " *          compilation can be setup quickly.                                  */\n\n",
       "".join(include_header_txt),
       "\n/* END -- Proposed include headers.                                          */\n" 
    ]

    for source_file in SourceFileList:
        fh = fs.open_or_die(source_file, "rb")
        original_content = fh.read()
        fh.close()

        fh = fs.open_or_die(source_file, "wb")
        fh.write(include_header_txt)
        fh.write("\n")
        fh.write(original_content)
        fh.close()

