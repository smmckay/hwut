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
import hwut.common             as common
import hwut.auxiliary.executer as executer

import tempfile
import os

def try_preprocess(SourceFile, IncludeDirList, AddFlagList):
    """Tries to preprocess the 'SourceFile' in order to find the list of 
    included header files. 
    """
    assert common.all_isinstance(IncludeDirList, (str,unicode))
    assert common.all_isinstance(AddFlagList, (str,unicode))

    # C-Preprocessor:  -MM --> get include dependencies, but do not consider
    #                          system headers
    #                  -MG --> no error on unfound include files
    #                  
    cl = [ "cpp", "-MM", "-MG",  ] 
    cl.extend(AddFlagList)
    cl.extend("-I%s" % directory for directory in IncludeDirList)
    cl.append(SourceFile)

    return executer.do_stdout(cl).replace("\\", "/")

def try_compile(SourceFile, IncludeDirList, AddFlagList):
    """Tries to compile the given file into an object file. It does NOT try
    to link.
    
    IncludeDirList:  List of directories where include files can be found.
    
    AddFlagList:     Additional flags passed to the compiler.

    RETURNS: [0] Object file name that was compiled
                 None -- if compilation failed

             [1] Textual output of compilation

    """
    assert common.all_isinstance(IncludeDirList, (str,unicode))
    assert common.all_isinstance(AddFlagList, (str,unicode))

    tmp_file_name = tempfile.mktemp(".o", dir="./")

    cl = [ "gcc", "-c", "-Wimplicit" ]
    cl.extend(AddFlagList)
    cl.extend("-I%s" % directory for directory in IncludeDirList)
    cl.append(SourceFile)
    cl.append("-o")
    cl.append(tmp_file_name)

    verdict, output = try_command_line(cl, tmp_file_name)

    if verdict: 
        return tmp_file_name, output

    # Make 100% sure that the object file does not exist
    try:    os.remove(tmp_file_name)
    except: pass

    # Report, that compilation failed --> [0] is None
    return None, output

def try_link(ObjectFileList, LibraryList, LibraryDirList, AddFlagList):
    """Tries to link a given set of (object files). 
    
    LibraryList:    Optional list of pesky '-lSomething' flags (i.e. short cuts
                    for libSomething.a or libSomething.so). Other libraries may 
                    be specified in ObjectFileList.
                  
    LibraryDirList: Lists where libraries could be found. 
    
    AddFlagList:    Additional flags doing whatsoever.  

    RETURNS: [0] Name of application being buildt
                 None, if build failed. 

             [1] Textual output of linking process.
    """
    assert common.all_isinstance(ObjectFileList, (str,unicode))
    assert common.all_isinstance(LibraryDirList, (str,unicode))
    assert common.all_isinstance(LibraryList, (str,unicode))
    assert common.all_isinstance(AddFlagList, (str,unicode))

    tmp_file_name = tempfile.mktemp(".exe", dir="./")

    cl = [ "gcc" ]
    cl.extend(ObjectFileList)
    cl.extend(LibraryList)
    cl.extend("-L%s" % directory for directory in LibraryDirList)
    cl.extend(AddFlagList)    
    cl.append("-o")
    cl.append(tmp_file_name)

    verdict, output = try_command_line(cl, tmp_file_name)

    if verdict: return tmp_file_name, output 
    else:       return None, output
    
__memoize_nm_db = {}
def try_nm(ObjectFile):
    """Calls the 'nm' utility to find reference implemented in object files.
    """
    global __memoize_nm_db
    entry = __memoize_nm_db.get(ObjectFile)
    if entry is None:
        cl = [ "nm", 
               "-C", # demangle original names (avoid '_' for windows)
               ObjectFile ] 
        entry = executer.do_stdout(cl)
        __memoize_nm_db[ObjectFile] = entry
    return entry

def try_command_line(CmdLine, TmpFileName):
    """Excutes a command line. 

    RETURNS: (TmpFileName produced?, Output)

    The first return value tells whether the temp file has been produced. This
    may be used as an indicated whether the command was successful.
    """
    assert common.all_isinstance(CmdLine, (str, unicode))

    out_str, err_str  = executer.do_stdout_and_stderr(CmdLine)
    verdict = os.path.exists(TmpFileName)
    #if not verdict and not out_str and CmdLine:
    #    print "Error: '%s' could not be executed." % CmdLine[0]
    return verdict, out_str + err_str 

