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
import hwut.sos.implementation_db     as     base
import hwut.io.select                 as     select
from   hwut.auxiliary.path            import good_path
import hwut.auxiliary.ctags_interface as     ctags

from   collections import defaultdict, namedtuple
from   operator    import itemgetter


import os
from   copy import copy

class ImplementationDb(base.ImplementationDb):
    """Database containing information about what references are present in
    what files. 

    Objects of this class are constructed via one of the following:

                ImplementationDb.with_ctags()
                ImplementationDb.without_ctags()

    """
    def __init__(self, assembler):
        base.ImplementationDb.__init__(self)
        self.assembler = assembler

    @classmethod
    def with_ctags(cls, assembler, FileSystemDb):
        result = cls(assembler)
        result.__extract_references({}, 
                                    FileSystemDb.library_file_db, 
                                    FileSystemDb.object_file_db)

        extension = ".c"
        for reference, file_name in ctags.reference_source_iterable(FileSystemDb.ctags_root_dir_list, "c"):
            if os.path.basename(file_name) == extension: continue
            result._enter_implementation(file_name, 
                                         base.ImplementationType.SOURCE, 
                                         reference)

        return result

    @classmethod
    def without_ctags(cls, assembler, FileSystemDb):
        result = cls(assembler)
        result.__extract_references(assembler.compiler.source_to_object_db, 
                                    FileSystemDb.library_file_db, 
                                    FileSystemDb.object_file_db)
        return result

    def clear(self):
        self.implemented_file_to_reference_set_db.clear()
        self.implemented_reference_to_file_list_db.clear()
        self.required_file_to_reference_set_db.clear()
        self.required_reference_to_file_list_db.clear()

    def __extract_references(self, SourceToObjectDb, LibraryFileDb, ObjectFileDb): 
        """Extracts reference information from sources, libraries, and object 
        files. 
        """
            
        for source_file, object_file in SourceToObjectDb.iteritems():
            self._analyze_and_enter(source_file, 
                                    base.ImplementationType.SOURCE, 
                                    object_file)

        for library_file, directory_set in LibraryFileDb.iteritems():
            for directory in directory_set:
                self._analyze_and_enter(good_path(directory, library_file), 
                                        base.ImplementationType.LIBRARY)

        for object_file, directory_set in ObjectFileDb.iteritems():
            for directory in directory_set:
                self._analyze_and_enter(good_path(directory, object_file),
                                        base.ImplementationType.OBJECT)

    def _extract_reference_info(self, File, FileType, DerivedFile):
        """Extracts implemented and required reference from the specified 'File'.

        RETURNS: [0] List of implemented references
                 [1] List of required/unresolved references.
        """
        if FileType == base.ImplementationType.SOURCE and DerivedFile is None:
            # File has not yet been compiled.
            DerivedFile = self.assembler.compiler.do(File)
            if DerivedFile is None: 
                return None, None

        if DerivedFile is not None: considered_file = DerivedFile
        else:                       considered_file = File

        implemented_list, \
        required_list,    \
        dummy             = self.assembler.compiler.get_references(considered_file)

        return implemented_list, required_list

    def get_string(self, NiceNameDb):
        def nice(Name):
            if Name in NiceNameDb: return NiceNameDb[Name]
            else:                  return Name

        def nice_item_list(Db):
            item_list = [
               (nice(file_name), whatsoever)
               for file_name, whatsoever in Db.iteritems()
            ]
            return sorted(item_list, key=itemgetter(0))

        def nice_list(List):
            return sorted([nice(name) for name in List])

        def do_reference_db(txt, Name, FoundDb):
            txt.append("  %s:\n" % Name)
            txt.extend(
                "    %8s --> %s\n" % (reference, "".join("((%s)), " % x for x in nice_list(implementation_set)))
                for reference, implementation_set in nice_item_list(FoundDb)
            )

        def do_file_db(txt, Name, Db):
            txt.append("  %s:\n" % Name)
            if not Db: 
                txt.append("    <empty>\n")
                return 

            L = max(len(file_name) for file_name in Db)
            for file_name, reference_list in nice_item_list(Db):
                txt.append("    ((%s)): %s" % (file_name, " " * (L-len(file_name))))
                for reference in reference_list:
                    txt.append('%s; ' % reference)
                txt.append("\n")

        iterable = self.implemented_reference_to_file_list_db.items()
        txt = []
        source_db = dict(
            (reference, [f for f, ft in file_list if ft == base.ImplementationType.SOURCE]) 
            for reference, file_list in iterable
        )

        do_reference_db(txt, "source_db", source_db)
        txt.append("\n")

        library_db = dict(
            (reference, [f for f, ft in file_list if ft == base.ImplementationType.LIBRARY]) 
            for reference, file_list in iterable
        )
        do_reference_db(txt, "library_db", library_db)
        txt.append("\n")

        object_db = dict(
            (reference, [f for f, ft in file_list if ft == base.ImplementationType.OBJECT]) 
            for reference, file_list in iterable
        )
        do_reference_db(txt, "object_db", object_db)

        txt.append("\n")
        do_file_db(txt, "required_file_to_reference_set_db",    self.required_file_to_reference_set_db)
        txt.append("\n")
        do_file_db(txt, "implemented_file_to_reference_set_db", self.implemented_file_to_reference_set_db)
        txt.append("\n")

        return "".join(txt)

