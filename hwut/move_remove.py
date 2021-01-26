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
import hwut.auxiliary.file_system as fs

def remove(cl, History_Item=None):
    """Removes a test application from the database and its related files 
       from the file system.
    """
    # We are not going to do a 'real' strategy, still using setup 
    # helps identifying directory and application.
    setup = Setup(cl)

    hi = HistoryItem_TestApplication_Deleted(setup.test_application_name)

    entry = __try_deletion(setup.test_directory, setup.test_application_name, hi) 
    if entry is None: return False
                       
    # Delete: OUT, GOOD files; Comment on temporary logic rule files.
    __delete_related_files(setup.test_directory, entry)
    
    return True

def move(cl):
    """Moves a test application from one place to another. 
    """
    # Determine source and target directory and filename
    source = cl.next("")
    target = cl.next("")
    source_dir, source_file = common.split_file_name(source)
    target_dir, target_file = common.split_file_name(target)

    if source_dir == target_dir:
        hi_0 = HistoryItem_TestApplication_move(source_file, target_file)
        hi_1 = None
    else:
        hi_0 = HistoryItem_TestApplication_move_to(source_file, target_file, target_dir)
        hi_1 = HistoryItem_TestApplication_move_from(source_file, target_file, source_dir)

    # Only if addition and deletion is possible, start with the process of moving
    if __addition_possible(target_dir, source_dir) == False:
        return

    entry = __if_deletion_possible_the_delete(source_dir, source_file, hi_0)
    if entry is None:
        return

    __add(target_dir, entry, hi_1)

    # Copy: OUT, GOOD files; Comment on temporary logic rule files.
    __copy_related_files(entry, source_dir, target_dir)
    # Delete: OUT, GOOD files; Comment on temporary logic rule files.
    __delete_related_files(source_dir, entry)

def __addition_possible(Dir, ApplicationName):
    """An application cannot be added if it already exists.
    """
    origin = os.getcwd()
    common.change_directory(Dir)

    # Read the test application database.
    common.test_db.read_db()

    if common.test_db.has_key(ApplicationName):
        io.move_remove_cannot_add_application_because_it_exists(Dir, ApplicationName)
        common.change_directory(origin)
        return False

    common.change_directory(origin)
    return True

def __add(Dir, Entry, HistoryItem):
    origin = os.getcwd()
    common.change_directory(Dir)

    # Read the test application database.
    common.test_db.read_db()

    # Delete the entry about the test application.
    common.test_db.delete(setup.test_application_name)
    common.test_db.write()

    common.history.init(os.getcwd())
    if HistoryItem is not None: common.history.append(HistoryItem)
    common.history.write()

    common.change_directory(origin)

def __if_deletion_possible_the_delete(Dir, FileName, HistoryItem):
    """A test application cannot be deleted, if it is not in the 
       correspondent database, or if it is still reported as make-
       dependent.

       RETURNS: None,           if nothing was deleted.
                TestDescription object that has been deleted from the database.
    """
    origin = os.getcwd()
    common.change_directory(Dir)

    # Read the test application database.
    common.test_db.read_db()
    
    # Get the information about the application
    entry = common.test_db.get(setup.test_application_name)
    if entry is None:
        io.remove_cannot_remove_application_since_not_in_database(setup.test_application_name)
        common.change_directory(origin)
        return None

    # Delete the application, if it is still there
    if entry.make_dependent_f():
        # Is it makeable --> check 'hwut-info' to see whether it is still reported.
        if setup.test_application_name in make.OLD_get_makeable_application_list():
            io.remove_cannot_remove_test_application_that_is_makeable(setup.test_application_name)
            common.change_directory(origin)
            return None

    # Delete the entry about the test application.
    common.test_db.delete(setup.test_application_name)
    common.test_db.write()

    # Add an entry in the history that the application has been deleted.
    common.history.init(os.getcwd())
    common.history.append(HistoryItem)
    common.history.write()

    common.change_directory(origin)
    return entry

def __delete_related_files(Dir, Entry):
    origin = os.getcwd()
    common.change_directory(Dir)

    test_sequence, dummy = Entry.get_Test_list()

    def remove(FileName):
        fs.try_remove(os.path.normpath(FileName))

    for info in test_sequence:
        remove(element.GOOD_FileName())
        remove(element.OUT_FileName())
        
    common.change_directory(origin)

def __copy_related_files(Entry, SourceDir, TargetDir):
    test_sequence, dummy = Entry.get_Test_list()

    target_dir = os.path.abspath(TargetDir)
    origin = os.getcwd()
    common.change_directory(SourceDir)

    def __move(FileName, TargetDir):
        file_name = os.path.normpath(FileName)
        content = fs.read_or_die(file_name).read()
        fs.open_or_die(os.path.normpath(TargetDir + "/" + file_name), "w").write(content)
        fs.try_remove(file_name)

    for info in test_sequence:
        __move("./GOOD/" + element.GOOD_FileName(), target_dir)
        __move("./OUT/" + element.OUT_FileName(),   target_dir)
        
    common.change_directory(origin)

