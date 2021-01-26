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
from   hwut.sos.c.output_interpreter  import detect_missing_library_file_stems, \
                                             detect_missing_references
from   hwut.sos.c.system              import try_link

def do(ObjectFileList, library_dir_db, LibraryList, AddLinkFlagList):
    """Try to link the given object files. Detect names of missing references. 
    Updates 'library_dir_db' according to missing libraries. 
    
    RETURNS: [0] application name
                 None, if linkage failed

             [1] UnresolvedDb

             [2] Unfound Libraries

    ADAPTS:  library_dir_db --> new library paths

    UnresolvedDb: 

            map: reference --> list of (file-name, function) 

    That is, it maps from a missing reference name to a list of files/functions 
    where it has been referenced.
    """
    # ONLY accept lists of ObjectFileList. The sequence is important!
    assert type(ObjectFileList) == list
    if not ObjectFileList:
        return None, None, {}

    unresolved_db    = {}
    missing_lib_set  = set()
    prev_library_set = False
    library_set      = True
    while prev_library_set != library_set:
        prev_library_set = library_set

        library_dir_list    = library_dir_db.get_directories()

        application, output = try_link(ObjectFileList, LibraryList,
                                       library_dir_list,
                                       AddLinkFlagList)
        if application is not None: 
            # self.tmp.register_application(application)
            break

        library_set = detect_missing_library_file_stems(output)
        if not library_set: # Missing libraries not the reason for failure. 
            break           # => Abort!

        # Find the missing libraries in the filesystem.
        # => update content of 'library_dir_db'.
        missing_lib_set = library_dir_db.update(filesystem_db, 
                                                library_set)
        if missing_lib_set: # Not all libraries have been found; 
            break           # => Abort!

    if application is None: unresolved_db = detect_missing_references(output)
    else:                   unresolved_db = {}

    return application, unresolved_db, missing_lib_set

