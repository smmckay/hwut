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
import hwut.auxiliary.path           as     path
import hwut.io.select                as     select
from   hwut.auxiliary.path           import good_path
import hwut.common                   as     common


from   collections import defaultdict
import os

class FileSystemDb(object):
    """Provides information that supports the search for missing references.
    """
    __slots__ = ("include_file_db", "source_file_db", 
                 "library_file_db", "object_file_db", 
                 "consider_source_files_as_include_files_f",
                 "ctags_root_dir_list")

    def __init__(self):
        self.include_file_db = defaultdict(set)
        self.source_file_db  = defaultdict(set)
        self.library_file_db = defaultdict(set)
        self.object_file_db  = defaultdict(set)

    def source_ext(self):  assert False, "Must be implemented in derived class"
    def object_ext(self):  assert False, "Must be implemented in derived class"
    def header_ext(self):  assert False, "Must be implemented in derived class"
    def library_ext(self): assert False, "Must be implemented in derived class"

    @classmethod
    def from_Setup(cls, Setup, SourceFilesAreIncludeFilesF=True, IncludeFileDbF=True):
        result = cls()   

        if not IncludeFileDbF:
            self.library_file_db = None
            self.object_file_db  = None
            self.source_file_db  = None

        result.preparation(
            RootDirList                 = Setup.hint_root_dir_list, 
            RootDirListIncludes         = Setup.hint_root_dir_list_include,
            RootDirListSources          = Setup.hint_root_dir_list_source,
            RootDirListObjects          = Setup.hint_root_dir_list_objects,
            RootDirListLibraries        = Setup.hint_root_dir_list_libraries,
            ExcludePatternList          = Setup.hint_exclude_pattern_list,
            ExcludeDirPatternList       = Setup.hint_exclude_dir_pattern_list,
            SourceFilesAreIncludeFilesF = SourceFilesAreIncludeFilesF
        )

        return result

    def preparation(self, 
                    RootDirList                 = ["../../../"], 
                    RootDirListIncludes         = [],
                    RootDirListSources          = [],
                    RootDirListObjects          = [], 
                    RootDirListLibraries        = [],
                    ExcludePatternList          = [], 
                    ExcludeDirPatternList       = [], 
                    SourceFilesAreIncludeFilesF = True):

        common.set_verbosity_f(True)

        if not RootDirListIncludes:  include_dir_set = RootDirList
        else:                        include_dir_set = RootDirListIncludes
        if not RootDirListSources:   source_dir_set  = RootDirList
        else:                        source_dir_set  = RootDirListSources
        if not RootDirListLibraries: library_dir_set = RootDirList
        else:                        library_dir_set = RootDirListLibraries
        if not RootDirListObjects:   object_dir_set  = RootDirList
        else:                        object_dir_set  = RootDirListObjects

        if common.get_ctags_application() is not None:
            self.ctags_root_dir_list = source_dir_set
        else:
            self.ctags_root_dir_list = None
            print "Warning: Using sos/sols while 'ctags' has not been installed or not"
            print "Warning: specified in environment variable HWUT_CTAGS_APP."

        # Sorting Database:
        # [0] -> set of directories of concern
        # [1] -> file name pattern to be matched
        # [3] -> database where the entry has to be made
        sort_db = path.FindAndSortDb()
        if self.include_file_db is not None:
            sort_db.register(include_dir_set, self.header_ext(),  self.include_file_db)
            # Every source file can also be included (to access static functions)
            if SourceFilesAreIncludeFilesF:
                sort_db.register(include_dir_set, self.source_ext(),  self.include_file_db)

        if self.library_file_db is not None:
            sort_db.register(library_dir_set, self.library_ext(), self.library_file_db)

        if self.object_file_db is not None:
            sort_db.register(object_dir_set,  self.object_ext(),  self.object_file_db)

        if self.source_file_db is not None:
            sort_db.register(source_dir_set,  self.source_ext(),  self.source_file_db)

        # Iterate recursively through sub directories and sort the found files
        # into the databases for include, source, library, and object file
        # names.
        sort_db.do(ExcludePatternList, 
                   ExcludeDirPatternList, 
                   AbsolutePathF=True)

    @staticmethod
    def disambiguify_all(db):
        result = set()
        for file_name, directory_set in db.iteritems():
            if not directory_set:       
                pass

            elif len(directory_set) == 1:                 
                result.add(next(iter(directory_set)))

            elif any(d in result for d in directory_set): 
                # If there is a directory in 'directory_set' that has already 
                # been chosen, then take that. 
                pass
            else:
                directory_list = [path.relative(x) for x in directory_set]
                choice_index   = select.directory(file_name, directory_list)
                choice         = directory_list[choice_index]
                result.add(choice)

        return result

    def source_file_list(self):
        for base_name, directory_set in self.source_file_db.iteritems():
            for directory in directory_set:
                yield good_path(directory, base_name) 




