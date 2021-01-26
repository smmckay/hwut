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
import hwut.io.select             as     select
import hwut.auxiliary.path        as     path
import hwut.auxiliary.file_system as     fs
from   collections                import defaultdict, namedtuple

import os
import sys

class Assembler(object):
    """Object to handle compiling and linking. It collects information about 
    the compile and linking process.
    """
    __slots__ = ("compiler", "linker")

    def __init__(self, filesystem_db, TheCompiler, TheLinker):
        assert isinstance(TheCompiler, Compiler)
        assert isinstance(TheLinker, Linker)
        self.compiler = TheCompiler
        self.linker   = TheLinker

    @classmethod
    def from_Setup(cls, Setup, filesystem_db):
        result = cls(filesystem_db)

        result.compiler.flag_list = Setup.user_compile_args + Setup.user_args
        result.linker.flag_list   = Setup.user_link_args    + Setup.user_args
        return result

    def compile_and_link(self, SourceFileList, ObjectFileList, LibraryFileList):
        """Attempts to compile the given list of source files. Missing header
        directories are automatically located--if possible. 

        ADAPTS:  compiler.source_to_object_db

        RETURNS: [0] Uncompiled sources file database:

                     name of source file --> missing header files.

                 [1] Set of unresolved references
                 [2] Set of implemented references
        """
        uncompiled_source_list, \
        object_file_list        = self.compiler.do_list(SourceFileList)

        if not object_file_list:
            return uncompiled_source_list, set(), set()

        object_file_list.extend(
            f for f in ObjectFileList if f not in object_file_list
        )

        application,          \
        missing_reference_db, \
        missing_lib_set       = self.linker.do(object_file_list,
                                               LibraryFileList) 

        unresolved_set  = set(missing_reference_db.iterkeys())
        implemented_set = self.compiler.get_implemented_references(object_file_list)

        return uncompiled_source_list, unresolved_set, implemented_set

    def clean_up(self):
        """Remove the files that have been created during analysis.
        """
        fs.try_remove_files(self.compiler.trash)
        self.compiler.trash.clear()
        fs.try_remove_files(self.linker.trash)
        self.linker.trash.clear()

        fs.try_remove_files(self.compiler.source_to_object_db.itervalues())
        self.compiler.source_to_object_db.clear()

class Compiler(object):
    """Manage the compilation process.

       * compiles
       * aggregates information about include directories
       * registers relation between source and generated objects
       * stores information about failed compilations
       * extracts information about references in files.

    An object of this class memoizes reference informations in order to avoid
    extracting the information from source, object and library files over 
    and over again. 
    """
    __slots__ = ("flag_list", 
                 "include_dir_db", 
                 "source_to_object_db", 
                 "bad_sources_db", 
                 "trash", 
                 "__memoize_reference_db")

    def __init__(self, filesystem_db):
        self.flag_list              = []
        self.include_dir_db         = IncludeDirDb(filesystem_db)
        self.source_to_object_db    = {}
        self.bad_sources_db         = {}
        self.trash                  = set()
        self.__memoize_reference_db = {}

    def _compile(self, SourceFile):
        assert False, "Call to member function that needs to be defined in derived class."

    def _get_headers(self, SourceFile):
        assert False, "Call to member function that needs to be defined in derived class."

    def do(self, SourceFile):
        """Do the best to compile the given source file. May be, new include 
        directories need to be added.
        """
        if SourceFile in self.source_to_object_db: 
            return self.source_to_object_db[SourceFile]
        elif SourceFile in self.bad_sources_db: 
            return None

        object_file,        \
        missing_header_set, \
        output              = self._compile(SourceFile)

        if object_file is not None: 
            self.source_to_object_db[SourceFile] = object_file
        else:
            self.bad_sources_db[SourceFile]      = (missing_header_set, output)
            print "Error: unable to compile '%s'" % path.relative(SourceFile)
            if missing_header_set: 
                print "Error: missing headers:"
                for header in sorted(missing_header_set):
                    print "Error:   \"%s\"" % header

        return object_file

    def do_list(self, SourceFileIterable):
        """Compile a list of source files.

        RETURNS: [0] List of files that could not be compiled.
                 [1] List of object files that have been buildt.
        """
        bad_source_list  = []
        good_object_list = []
        for source_file in SourceFileIterable:
            object_file = self.do(source_file)
            if object_file is None: bad_source_list.append(source_file)
            else:                   good_object_list.append(object_file)
        return bad_source_list, good_object_list

    def get_function_info(self, SourceFile):
        """RETURNS: [0] externally linked functions implemented in SourceFile
                    [1] statically linked (internal) functions. 
        """
        object_file = self.do(SourceFile)
        if object_file is None:
            extern_function_list = []
            static_function_list = []
        else:
            extern_function_list, \
            dummy, \
            static_function_list  = self.get_references(object_file)

        return extern_function_list, static_function_list

    def get_references(self, ObjectFile):
        """RETURNS: [0] externally linked functions
                    [1] Unresolved symbols.
                    [2] statically linked functions
        """
        entry = self.__memoize_reference_db.get(ObjectFile)
        if entry is None:
            entry = self._get_references(ObjectFile)
            self.__memoize_reference_db[ObjectFile] = entry
        return entry

    def get_implemented_references(self, ObjectFileList):
        """RETURNS: The references implemented in the given object files.
        """
        result = set()
        for f in ObjectFileList:
            new_implemented_set, dummy, dummy = self.get_references(f)
            result.update(new_implemented_set)
        return result

    def get_include_headers(self, SourceFile):
        """RETURNS: Headers included in SourceFile.
        """
        return self._get_headers(SourceFile) 

    def implements_main(self, SourceFile):
        extern_list, dummy = self.get_function_info(SourceFile)
        if not extern_list and not dummy:
            if SourceFile in self.bad_sources_db:
                print "Error: cannot compile '%s'" % SourceFile
                print "#output:", self.bad_sources_db[SourceFile]
            else:
                print "Error: no functions found in '%s'"
            sys.exit(-1)

        return "main" in extern_list

class Linker(object):
    """Manage the linking process.
    """
    __slots__ = ("flag_list", "library_dir_db", "trash")

    def __init__(self, filesystem_db):
        self.flag_list      = []
        self.library_dir_db = LibraryDirDb(filesystem_db)
        self.trash          = set()

    def do(self, ObjectFileList, LibraryFileList=[]):
        application,          \
        missing_reference_db, \
        missing_lib_set       = self._link(ObjectFileList, LibraryFileList)

        if application is not None:
            self.trash.add(application)

        if missing_reference_db is None:
             print "Error: linking completely failed."
             sys.exit(-1)

        return application, missing_reference_db, missing_lib_set


FileDb_Entry = namedtuple("FileDB_Entry", 
                          ("directory", "location_set"))

class FileDb(dict):
    """
    A FileDb develops a database that allows to tell from what directory a
    'referred file' needs to be taken, and it tells what files refer to it.

        file name --> .directory:    Directory where the file taken 
                      .location_set: Set of files where referred file is used. 
    
     

    """
    def __init__(self, FileToDirectoryDb):
        """FileToDirectoryDb: Required to find directories for a referred file.

                referred file --> list of directories where it is found

        """
        dict.__init__(self)
        
        self._directory_db = FileToDirectoryDb

        # Maintain a preferred set of directories to avoid asking the user
        # over and over again.
        self._preferred_set = set()

    def determine_directories(self, SearchedFileList, SourceFile=None):
        """Tries to update the _db with directories from the file system so
        that all files in SearchedFileList can be accessed. 

        RETURN: Set of unfound files
        """
        ambiguity_db = defaultdict(set)
        unfound_set  = set()
        for file_name in SearchedFileList:

            known = self.get(file_name)
            if known is not None:
                known.location_set.add(SourceFile)
                continue

            dir_set = self._directory_db.get(file_name)

            if not dir_set: 
                unfound_set.add(file_name)
            elif len(dir_set) == 1:
                directory       = path.relative(next(iter(dir_set)))
                self[file_name] = FileDb_Entry(directory, set([SourceFile]))
            else:
                ambiguity_db[file_name].update(dir_set)

        if ambiguity_db:
            self.__disambiguify(ambiguity_db, SourceFile)

        return unfound_set

    def get_directories(self, SourceFile=None):
        """RETURNS: Directories that are required to access the files which are
                    referred by SourceFile.
        """
        if SourceFile is None: 
            return set(
                entry.directory for entry in self.itervalues()
            )
        else:
            return set(
                entry.directory
                for entry in self.itervalues()
                    if SourceFile in entry.location_set
            )

    def __disambiguify(self, AmbiguityDb, SourceFile):
        entry_list = AmbiguityDb.items() 
        entry_list.sort(key=lambda x: - len(x[1])) # sort by directory list length

        for file_name, directory_set in entry_list:
            if not self._preferred_set.isdisjoint(directory_set): 
                choice = self._preferred_set.intersection(directory_set).pop()
            else:
                directory_list = [path.relative(x) for x in directory_set]
                choice_index = select.directory(file_name, directory_list)
                choice       = directory_list[choice_index]
                self._preferred_set.add(choice)

            self[file_name] = FileDb_Entry(choice, set([SourceFile]))

    def __str__(self):
        return "#%i [%s]" % (len(self._db), "".join(
            "%s --> %s\n" % (key, value) for key, value in self.iteritems()
        ))


class IncludeDirDb(FileDb):

    def __init__(self, FileSystemDb):
        FileDb.__init__(self, FileSystemDb.include_file_db)

    def get_include_dir_by_source_dir(self, SourceFileSet):
        result = defaultdict(set)
        for source in SourceFileSet:
            source_dir = os.path.dirname(source)
            result[source_dir].update(self.get_directories(source))

        return result

    def has_header(self, Header):
        """RETURNS: True  -- if the Header was found in the database.
                    False -- else.
        """
        return Header in self.values()

class LibraryDirDb(FileDb):
    def __init__(self, CHint):
        FileDb.__init__(self, CHint.library_file_db)

    def update(self, filesystem_db, MissingLibFileStems):
        """Tries to update the lib_path_list with directories, so that all
        missing libraries can be found. The libraries are specified by their
        file names. The suffixes '.a' and '.so' (Unix) are appended automatically.

        RETURN: Set of unfound library file stems 

        That is, in case of 'False', it does not make sense to try any further 
        to link the objects under considerations.
        """
        if not MissingLibFileStems: return set()

        def get_candidates(FileStem):
            # DOS: return ("%s.lib" % FileStem, "%s.dll" % FileStem)
            return (FileStem, "%s.a" % FileStem, "%s.so" % FileStem)

        def select(new_dir_set):
            if not new_dir_set: return None
            return path.relative(new_dir_set.pop())
            
        unfound_set = set()
        for file_stem in MissingLibFileStems:
            found_f = False
            for candidate in get_candidates(file_stem):
                if candidate in self._db: 
                    found_f = True
                    continue
                chosen = select(candidate, filesystem_db.library_file_db[candidate])
                if chosen is None: continue

                self._db[candidate] = chosen
                found_f = True
                break

            if not found_f: unfound_set.add(file_stem)

        return unfound_set
        
    def get_directories(self):
        """RETURNS: All directories in database.
        """
        result = []
        for directory_list in self.itervalues():
            result.extend(path.relative(x) for x in directory_list)
        return result

