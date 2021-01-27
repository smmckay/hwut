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
import hwut.sos.c.smart_compile       as     smart_compile
import hwut.sos.c.smart_link          as     smart_link
from   hwut.sos.c.system              import try_nm
from   hwut.sos.c.output_interpreter  import detect_implemented_references
import hwut.sos.assembler             as     base

class Assembler(base.Assembler):
    """Object to handle compiling and linking. It collects information about 
    the compile and linking process.
    """
    def __init__(self, filesystem_db):
        base.Assembler.__init__(self, filesystem_db, 
                                CompilerC(filesystem_db),
                                LinkerC(filesystem_db))

class CompilerC(base.Compiler):
    def __init__(self, filesystem_db):
        base.Compiler.__init__(self, filesystem_db)

    def _compile(self, SourceFile):
        return smart_compile.do(SourceFile, self.include_dir_db, self.flag_list)

    def _get_headers(self, SourceFile):
        return list(smart_compile.do_get_mentioned_headers(SourceFile, 
                                                           self.include_dir_db, 
                                                           self.flag_list))
    def _get_references(self, ObjectFile):
        output = try_nm(ObjectFile)
        return detect_implemented_references(output)

class LinkerC(base.Linker):

    def __init__(self, filesystem_db):
        base.Linker.__init__(self, filesystem_db)

    def _link(self, ObjectFileList, LibraryFileList):
        return smart_link.do(ObjectFileList, self.library_dir_db, 
                             LibraryFileList, self.flag_list)


