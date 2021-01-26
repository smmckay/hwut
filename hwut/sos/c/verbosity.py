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
import hwut.common                    as     common

def verbose_print_linkage_step(fh, _UnresolvedDb, _SelectionDb):
    """Print what has happened in this iteration step. That is what undefined
    references have been detected and what references have been resolved.  
    """
    if not common.verbosity_f(): return

    for reference, location_set in _UnresolvedDb.iteritems():
        implementation = _SelectionDb.get(reference)
        if implementation is None: continue

        location_list = sorted(list(location_set))
        fh.write("# '%s' referred in '%s'\n" % (reference, location_list[0].file_name))
        space = " %s              " % (" " * len(reference))
        for location in location_list[1:]:
            fh.write("# %s'%s'\n" % (space, location.file_name))
        
        fh.write("#    taken from '%s'\n" % implementation.chosen)
        if implementation.remaining_list:
            fh.write("#    ignored alternatives: '%s'\n" % implementation.remaining_list[0])
            for remaining in implementation.remaining_list[1:]:
                fh.write("#                          '%s'\n" % remaining)
           
def verbose_print_compile_step(fh, _MissingHeaderDb, _IncludeDirDb):
    """Print what headers where missing and where they have been found.
    """
    if not common.verbosity_f(): return

    for header, location_set  in _MissingHeaderDb.iteritems():
        if not _IncludeDirDb.has_header(header): continue

        location_list = sorted(list(location_set))
        source_file   = location_list[0][0]
        fh.write("# '%s' included from '%s'\n" % (header, source_file))
        space = " %s                  " % (" " * len(header))
        for location in location_list[1:]:
            fh.write("# '%s'\n" % (space, location))

def verbose_print_unresolved_references(fh, _UnresolvedReferenceSet, _UnresolvedDb):
    """Prints the remaining unresolved references.
    """
    if not common.verbosity_f(): return

    fh.write("Following references could not be found:\n")
    for reference, location_set in _UnresolvedDb.iteritems():
        if reference not in _UnresolvedReferenceSet: continue
        location_list = sorted(list(location_set))
        fh.write("      '%s' from '%s'\n" % (reference, location_list[0].file_name))
        space =  " %s             " % (" " * len(reference))
        for location in location_list[1:]:
            fh.write("%s'%s'\n" % (space, location.file_name))

def verbose_error_on_compilation_failed(fh, SourceFile, UnfoundHeaderSet):
    if not common.verbosity_f(): return
    
    fh.write("Compilation of file '%s' failed;" % SourceFile)
    if UnfoundHeaderSet: 
        fh.write("missing headers:\n")
        for header in sorted(list(UnfoundHeaderSet)):
            fh.write("    '%s'\n" % header)
    else:                
        fh.write("\n")

    
