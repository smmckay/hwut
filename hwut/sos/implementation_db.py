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
import hwut.io.select as     select

from   collections    import defaultdict, namedtuple
from   copy           import copy
import os

ImplementationFile = namedtuple("ImplementationFile", 
                                ("file_name", "implentation_type"))
class ImplementationType:
    SOURCE        = 0
    LIBRARY       = 1
    OBJECT        = 2
    CRASH_ON_CALL = 3

class Requirement:
    def __init__(self): 
        self.source_file_list   = set()
        self.library_file_list  = set()
        self.object_file_list   = set()
        self.crash_on_call_list = set()

    @staticmethod
    def from_database(db):
        result = Requirement()
        result.source_file_list   = db[ImplementationType.SOURCE] 
        result.library_file_list  = db[ImplementationType.LIBRARY] 
        result.object_file_list   = db[ImplementationType.OBJECT] 
        result.crash_on_call_list = db[ImplementationType.CRASH_ON_CALL]
        return result

    def update(self, Other):

        self.source_file_list.update(Other.source_file_list)
        self.library_file_list.update(Other.library_file_list)
        self.object_file_list.update(Other.object_file_list)
        self.crash_on_call_list.update(Other.crash_on_call_list)

class ImplementationDb:
    def __init__(self):
        # map: reference name --> list of 'Implementation' objects.
        self.implemented_reference_to_file_list_db = defaultdict(list)
        # map: file name      --> set of implemented references
        self.implemented_file_to_reference_set_db = defaultdict(set)

        # map: reference name --> list of files that require it.
        self.required_reference_to_file_list_db = defaultdict(list)
        # map: file name      --> list of required references
        self.required_file_to_reference_set_db  = defaultdict(set)

    def find_references(self, UnresolvedSet, ImplementedSet):
        """Searches in the reference databases and generates a list of source, 
        library, and object files. 

        UnresolvedSet  -- references not found in the user's sources.
        ImplementedSet -- references found in the users' sources.

        RETURNS: [0] Unresolved references
                 [1] Requirement: [0] List of source files
                                  [1] List of library files
                                  [2] List of object files

        """
        ImplementationTypeList = [
            ImplementationType.SOURCE,
            ImplementationType.LIBRARY,
            ImplementationType.OBJECT,
            ImplementationType.CRASH_ON_CALL,
        ]

        db = dict(
            (itype, set()) for itype in ImplementationTypeList
        )

        prev_unresolved_set = None
        unresolved_set      = UnresolvedSet
        implemented_set     = copy(ImplementedSet)
        chosen              = Chosen()
        while prev_unresolved_set != unresolved_set:
            prev_unresolved_set = copy(unresolved_set)
        
            for ft, file_set in self.__find(chosen, unresolved_set, implemented_set):
                db[ft].update(file_set)

        return Requirement.from_database(db)

    def __find(self, chosen, unresolved_set, implemented_set):
        """Tries to find unresolved references mentioned in 'unresolved_set' 
        in the present database. Files that implement references are taken into
        consideration--their references also need to be implemented. 
        
        RETURNS:  iterable: (file type, file name set)

        Where the file type maps the type of the files in the set. Each file in 
        the set implements a reference.
        """
        assert not unresolved_set.intersection(implemented_set)

        def update(unresolved_set, implemented_set, NewUnresolved, NewImplementedSet):
            """Adapts the sets of unresolved and implemented references. 
            """

            implemented_set.update(NewImplementedSet)
            unresolved_set.difference_update(NewImplementedSet)

            # 'new_unresolved_set' shall contain nothing that has been 
            # implemented before.
            new_unresolved_set.difference_update(implemented_set)

            # 'not superset' means: there is something in 'new_unresolved_set'
            #                       which is not in 'unresolved_set'.
            if not unresolved_set.issuperset(new_unresolved_set):
                unresolved_set.update(new_unresolved_set)

            assert not unresolved_set.intersection(implemented_set)

        db = defaultdict(set)
        while unresolved_set:
            reference    = unresolved_set.pop()
            if reference in implemented_set: continue

            alternatives = self.implemented_reference_to_file_list_db.get(reference)

            if not alternatives:       
                file_name, implentation_type = reference, ImplementationType.CRASH_ON_CALL
            elif len(alternatives) == 1: 
                file_name, implentation_type = next(iter(alternatives))
            else:
                file_name, implentation_type = chosen.select(reference, set(alternatives))

            if implentation_type != ImplementationType.CRASH_ON_CALL:
                new_implemented_set, \
                new_unresolved_set   = self._get_reference_info(file_name, implentation_type) 
            else:
                new_implemented_set = set([reference])
                new_unresolved_set  = set()

            # A file, that implements 'main' cannot possibly be considered.
            if "main" in new_implemented_set: 
                print "Error: Try to resolve reference '%s'" % reference
                print "Error: in '%s'." % file_name
                print "Error: But this file contains 'main()' function."
                continue

            db[implentation_type].add(file_name)

            update(unresolved_set,     implemented_set, 
                   new_unresolved_set, new_implemented_set)

        return db.iteritems()


    def _analyze_and_enter(self, File, FileType, DerivedFile=None):
        """Extracts reference information from 'File'. Implemented references
        are added to 'db', unreferenced references are added to 'require_db'.
        """
        implemented_list, \
        required_list     = self._extract_reference_info(File, FileType, DerivedFile)
        if not implemented_list and not required_list: 
            return False
    
        for reference in implemented_list:
            self._enter_implementation(File, FileType, reference)
        for reference in required_list:
            self._enter_requirement(File, FileType, reference)

        return True

    def _enter_implementation(self, FileName, FileType, Reference):
        """Register: 'Reference' is implemented in 'FileName'.
        """
        entry = self.implemented_reference_to_file_list_db[Reference]
        ifile = ImplementationFile(FileName, FileType)
        if ifile not in entry:
            entry.append(ifile)
        self.implemented_file_to_reference_set_db[FileName].add(Reference)

    def _enter_requirement(self, FileName, FileType, Reference):
        """Register: 'Reference' required/referred in 'FileName'.
        """
        entry = self.required_reference_to_file_list_db[Reference]
        ifile = ImplementationFile(FileName, FileType)
        if ifile not in entry:
            entry.append(ifile)
        self.required_file_to_reference_set_db[FileName].add(Reference)

    def _get_reference_info(self, File, FileType):
        """RETURNS: [0] set of implemented references in file
                    [1] set of required references in file
        """
        if File not in self.required_file_to_reference_set_db:
            if not self._analyze_and_enter(File, FileType):
                return set(), set()

        return self.implemented_file_to_reference_set_db[File], \
               self.required_file_to_reference_set_db[File]


class Chosen:
    def __init__(self):
        # Set of directories from which files have been chosen.
        # (Directories that appear first have preference)
        self.__dir_list = []

        # Files that have been chosen before to implement some references.
        # map: (file name, file type) --> set of references
        self.__file_db = defaultdict(set)

        # Functions that are user-chosen to be implemented as 'crash-on-call'
        self.__crash_on_call_stubs = set()

        # Read from previous session, if there is some
        ## self.__previous_choice_db = self.__read_fly()

    def select(self, Reference, FileSet):
        """Assume that the reference can be taken out of more than one file--
        all of the files being present in FileSet. This function makes a choice
        from which file the reference has to be take. There are three stages:

                  (0) If the reference has been asked to crash-on-call.
                  (1) A file that has been chosen before
                  (2) A file from a directory from where a file has been 
                      chosen before. 
                  (3) User interaction.

        FileSet: Set of tuples (file name, file type)

        RETURNS: File name, File type
        """
        #previous = self.__previous_choice_db.get(Reference)
        #if previous is not None:
        #    print "Recall for: '%s'" % Reference
        #    print "Use:        '%s'" % previous[0]
        #    return previous

        if Reference in self.__crash_on_call_stubs:
            return Reference, ImplementationType.CRASH_ON_CALL

        # (1) Is there a file that has been chosen before?
        chosen_before = FileSet.intersection(self.__file_db.iterkeys())
        if chosen_before: 
            return next(iter(chosen_before))   

        # (2) Is there a directory that has been chosen before?
        file_name, implentation_type = self.__select_by_directory(FileSet)
        if file_name: 
            return file_name, implentation_type

        # (3) User interaction.
        return self.__user_interaction(Reference, FileSet)

    def __user_interaction(self, Reference, FileSet):
        """Interact on the standard input/output to determine what file shall 
        be chosen to implement the given reference. If 'crash-on-call' is 
        selected, the a stub will be implemented that crashes upon call.
        """
        file_list    = []
        implentation_type_db = {}
        for f, ft in sorted(FileSet, key=lambda x: (x[1], x[0])):
            implentation_type_db[len(file_list)] = ft
            file_list.append(f)

        file_index, \
        prefer_directory_f = select.implementation(Reference, file_list)

        # Crash-on-call stub required.
        if file_index == -1:
            self.__crash_on_call_stubs.add(Reference)
            return Reference, ImplementationType.CRASH_ON_CALL

        # File determined to implement reference
        file_name         = file_list[file_index]
        implentation_type = implentation_type_db[file_index]
        self.__register_user_choice(Reference, file_name, implentation_type) 
        ## self.__record_fly(Reference, file_name, implentation_type, prefer_directory_f)
        return file_name, implentation_type

    def __select_by_directory(self, FileSet):
        """RETURNS: Name of file, if it was located in a preferred directory.
        """
        result = None, None
        for file_name, implentation_type in FileSet:
            dir_name = os.path.dirname(file_name)
            if dir_name in self.__dir_list:
                if result is None: result = file_name, implentation_type
                else:              return None, None         # Not unique.
        return result

    def __register_user_choice(self, Reference, FileName, ImplementationType, PreferDirF=False):
        if PreferDirF:
            directory = os.path.dirname(FileName)
            if directory not in self.__dir_list:
                self.__dir_list.append(directory)

        self.__file_db[(FileName, ImplementationType)].add(Reference)

    def __LATER_IMPLEMENTATION_read_fly(self):
        result = {}

        try: 
            fh = open("hwut-previous-selection.txt", "rb")
        except:
            return result

        print "Note: Recall choices from 'hwut-previous-choices.txt'."
        print "Note: Delete the file if this is not desired!"

        lol    = fly.read_list_list(fh, 4)
        if lol is None: 
            return result

        for reference, file_name, implementation_type_str, prefer in lol:
            implementation_type = base.ImplementationType.from_string(implementation_type_str)

            result[reference] = (file_name, implementation_type)

            if implementation_type == base.ImplementationType.CRASH_ON_CALL:
                self.__crash_on_call_stubs.add(file_name)
            else:
                prefer_directory_f = (prefer == "True")
                self.__register_user_choice(reference, file_name, 
                                            implementation_type, prefer_directory_f)
                                        
        fh.close()
        return result

    def __LATER_IMPLEMENTATION_record_fly(self, Reference, file_name, implentation_type, PreferDirF):
        try: 
            fh = open("hwut-previous-selection.txt", "wab")
        except:
            return
        fh.write("[ %s; %s; %s; %s; ]\n" % (Reference, file_name, implentation_type, PreferDirF))
        fh.close()





