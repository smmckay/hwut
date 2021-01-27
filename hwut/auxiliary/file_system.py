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
import hwut.auxiliary.path as path
import hwut.io.messages    as io
import hwut.common         as common

import tempfile
import os
import sys
import stat
import glob

class DebugFh:
    def __init__(self, FileName, Mode):
        self.fh = open(FileName, Mode)
        print("fh_%i = open(\"%s\", \"%s\")" % (id(self.fh), FileName, Mode))

    @property
    def name(self):
        return "DebugFh: \'%s\'" % (id(self.fh), self.fh.name)

    def read(self, N):
        before = self.fh.tell()
        result = self.fh.read(N)
        after  = self.fh.tell()
        print("fh_%i.read(%s) # %i->%i" % (id(self.fh), N, before, after))
        return result

    def seek(self, X0, X1=0):
        before = self.fh.tell()
        result = self.fh.seek(X0, X1)
        after  = self.fh.tell()
        print("fh_%i.seek(%s,%s) # %i->%i" % (id(self.fh), X0, X1, before, after))

    def tell(self):
        result = self.fh.tell()
        print("fh_%i.tell() # %i" % (id(self.fh), result))
        return result

def raise_write_protection(Dir):
    """Find files in Dir that are not write protected and make them write protected"""
    error_n = 0
    try:    file_iterable = os.listdir(Dir)
    except: error_n += 1; file_iterable = []

    for file in file_iterable:
        # Never Change Directories that Contain Configuration Management Information
        if os.path.isfile(file) == False: continue
        try:    io.on_raise_write_protection(Dir, file)
        except: error_n += 1
        chmod(Dir + "/" + file, stat.S_IREAD)

    if error_n:
        print("Error: failed to raise write protection for files in")
        print("Error: %s" % Dir)

def get_hwut_unrelated_files():
    test_sequence_element_list = common.test_db.get_test_sequence_up_to_date()

    expected_list = set()
    for element in test_sequence_element_list:
        expected_list.add(os.path.normpath(element.GOOD_FileName()))
        expected_list.add(os.path.normpath(element.OUT_FileName()))
        expected_list.add(os.path.normpath(element.file_name()))
        if element.description.temporal_logic_f():
            for file in element.description.temporal_logic_rule_file_list():
                expected_list.add(os.path.normpath(file))


    expected_list.add(os.path.normpath("./%s" % HWUT_DATABASE_FILE))

    def get_content(Dir):
        return map(lambda x: os.path.normpath(Dir + "/" + x),
                   os.listdir(os.path.normpath(Dir)))

    work_list  = get_content(".")
    work_list += get_content("./ADM")
    work_list += get_content("./GOOD")
    work_list += get_content("./OUT")

    unknown_dir_list  = set()
    unknown_file_list = set()

    for file in work_list:
        if os.path.isdir(file):
            if file not in ["ADM", "GOOD", "OUT"]:
                unknown_dir_list.add(file)
        elif file not in expected_list:
            unknown_file_list.add(file)

    return unknown_file_list, unknown_dir_list

def get_TEST_directories():
    TEST_directory_name   = common.TEST_DIR_NAME
    L_TEST_directory_name = len(TEST_directory_name)

    # -- find all sub-dirs that are ./TEST-directories
    def __check_end(Name, End):
        # cut any trailing slash or backslash
        while len(Name) > 1 and Name[-1] in ["/", "\\"]:
            Name = Name[:-1]
        # now, one can use python's 'os.path.basename' since the name does not end with '/'
        return os.path.basename(Name) == End

    current_directory = os.getcwd()
    # Use dictionary to provide list of unique elements
    test_dir_db = {}
    for root, dir_list, file_list in os.walk("./", topdown=False):
        for dir in dir_list:
            # do not consider the TEST directories in configuration management data (CVS, Subversion)
            if dir.find(".svn") != -1: continue
            if dir.find("CVS") != -1:  continue
            if __check_end(dir, TEST_directory_name):
                test_dir_db[root + "/" + dir] = True

    # -- add the current directory, if it is called 'TEST_directory_name'
    if __check_end(current_directory, TEST_directory_name):
        test_dir_db[current_directory] = True

    test_dir_list = test_dir_db.keys()

    test_dir_list.sort()

    return map(os.path.normpath, test_dir_list)

def open_or_None(FileName, Mode):
    try:
        return open(FileName, Mode)
    except:
        return None

def open_or_die(FileName, Mode, NoteF=True):
    assert "b" in Mode, \
           "To be compatible with windows, all files should be opened in binary mode!"
    try:
        #if os.access(FileName, os.F_OK) and "w" in Mode:
        #    chmod(FileName, stat.S_IWRITE)
        return open(FileName, Mode)
    except:
        if NoteF:
            print("Cannot open file '%s'" % FileName)
        #chmod(common.HWUT_DATABASE_FILE, stat.S_IWRITE)
        #try:    fh = open(common.HWUT_DATABASE_FILE, "wb"); fh.write(txt)
        #except: io.on_file_access_error(common.HWUT_DATABASE_FILE)
        #return
        sys.exit(-1)

def open_one_or_die(FileNameList, Mode):
    for file_name in FileNameList:
        if True:
            fh = open(file_name, Mode)
            return fh
        try:
            pass
        except:
            continue
        print("Error: cannot open any of files: %s" % FileNameList)
        sys.exit(-1)

def read_or_die(FileName, NoteF=True):
    try:
        fh = open(FileName, "rb")
    except:
        if NoteF:
            print("Cannot read file '%s'" % FileName)
        sys.exit(-1)

    content = fh.read()
    fh.close()
    return content

def move_away(OldFileName):
    if not os.path.isfile(OldFileName):
        return None
    tmp_file_name = tempfile.mktemp(".backup", dir="./")
    rename_file(OldFileName, tmp_file_name)
    return tmp_file_name

def rename_file(old_file_name, new_file_name, PrevUserStatement="YES"):
    if old_file_name is None:
        return "YES"

    if os.access(new_file_name, os.F_OK):
        os.chmod(new_file_name, stat.S_IWRITE)

    if not os.access(old_file_name, os.F_OK):
        io.on_file_does_not_exist(old_file_name)
        return "NO"

    #user_statement = PrevUserStatement
    #if os.access(new_file_name, os.F_OK):
    #    user_statement = select.on_file_request_overwrite(new_file_name)
    #    if user_statement in ["NO", "NEVER"]: return user_statement

    # -- rename old file to new file
    try:    os.rename(old_file_name, new_file_name)
    except: return "NO"

    return "YES" # user_statement

def is_there_an_OUT_file(TestInfo):
    return os.access(TestInfo.OUT_FileName(), os.F_OK)

def ensure_GOOD_file_exists(TestInfo):
    file_name = TestInfo.GOOD_FileName()
    if os.access(file_name, os.F_OK): return
    open_or_die(file_name, "wb").close()

def get_GOOD_output(TestInfo):
    txt = read_or_die(TestInfo.GOOD_FileName())

    crc32 = binascii.crc32(txt)
    crc32_orig = TestInfo.choice().good_file_crc_32()
    if  crc32_orig is not None and crc32 != crc32_orig:
        io.error_crc32_mismatch(TestInfo)
        common.history.register(HistoryItem_CRCError(TestInfo.file_name(), TestInfo.choice(),
                                                     crc32_orig, crc32))

        # -- adapt the crc32 value for the given choice
        TestInfo.choice().set_good_file_crc_32(crc32)
        return txt

    return txt

def get_file_name_list_in_directory():
    return [
        path.strip_dot_slash(file_name)
        for file_name in os.listdir(os.getcwd()) if os.path.isfile(file_name)
    ]

def ensure_existence(FileSystemObject, OnErrorComment, DirectoryF=False):
    if os.access(FileSystemObject, os.F_OK) == False:
        if OnErrorComment != "":
            comment = OnErrorComment.replace("$$NAME$$", FileSystemObject)
            io.on_file_system_object_does_not_exist(FileSystemObject, comment)
        return False
    return True

def ensure_directory_structure():
    """Makes sure that ./OUT, ./GOOD, and ./ADM exist in the current directory."""
    for directory in ["OUT", "GOOD", "ADM"]:
        if not os.access(directory, os.F_OK):
            os.mkdir(directory)

def try_remove_files(FileList):
    for file_name in FileList:
        try_remove(file_name)

def try_remove(FileName):
    try:    os.remove(FileName)
    except: pass

def try_remove_glob(FileNamePattern):
    try:    os.remove(glob.glob(FileNamePattern))
    except: pass

def try_remove_recursively(Dir, Pattern):
    # Delete any possible trailing object files.
    for directory in path.recursive_subdirectory_iterable([Dir]):
        backup = os.getcwd()
        os.chdir(directory)
        try_remove_files(glob.glob(Pattern))
        os.chdir(backup)

def chmod(FileName, Mode):
    try:
        os.chmod(FileName, Mode)
    except:
        pass
