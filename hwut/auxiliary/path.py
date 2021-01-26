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
import hwut.common      as common
from   hwut.common      import __safe_path as __safe_path

import sys
import os
import stat
import binascii
from   glob        import glob
from   fnmatch     import fnmatch
from   collections import defaultdict


def strip_dot_slash(Filename):
    if len(Filename) > 2 and Filename[:2] == "./": return Filename[2:]
    else:                                          return Filename

def ensure_dot_slash(Filename):
    if len(Filename) > 2 and Filename[:2] != "./": return "./" + Filename
    else:                                          return Filename

def get_protocol_file_name(Entry, Choice, OutputF=False):
    """Get the name of the protocol file that corresponds to a test application 
       and a specific choice. The protocol file name in the output directory **does**
       contain always the choice. In the GOOD directory, it is possible that
       all choices produce the **same** output. Then, the protocol file name does not
       contain the choice.
    """
    safe_choice = Choice.replace("/", "-slash-")
    safe_choice = safe_choice.replace("\\", "-backslash-")
    safe_choice = safe_choice.replace(":", "-colon-")
    safe_choice = safe_choice.replace("#", "-hash-")
    safe_choice = safe_choice.replace(";", "-semi-colon-")
    safe_choice = safe_choice.replace(" ", "-space-")
    safe_choice = safe_choice.replace("\t", "-tabulator-")
    safe_choice = safe_choice.replace("\n", "-newline-")
    safe_choice = safe_choice.replace("\r", "-retour-")

    arg_str = ""
    if OutputF and safe_choice != "":            
        # ./OUT files differ always by choice
        arg_str = "--" + safe_choice
    elif safe_choice != "" and not Entry.all_choices_same_result_f(): 
        # ./GOOD files may be the same for all choices, see 'else:'
        arg_str = "--" + safe_choice
    else:
        # If all choices produce the same result then the GOOD files do not contain
        # the choice in the filename.
        pass

    candidate = Entry.file_name() + arg_str + ".txt"
    a_code = ord('a'); z_code = ord('z')
    A_code = ord('A'); Z_code = ord('Z')

    final = []
    for letter in candidate:
        code = ord(letter)
        if   code >= a_code and code <= z_code: final.append(letter)   # do not rely on isalpa(), since that may be local
        elif code >= A_code and code <= Z_code: final.append(letter)
        elif letter.isdigit():                  final.append(letter)
        elif letter in [".", "-", "_"]:         final.append(letter)
        else:                                   final.append("0x%2X" % code) 

    return "".join(final)

def split_path(Path):
    """Split the path according to the corresponding operating system."""
    assert type(Path) != list
    remainder = os.path.normpath(Path)
    tail      = "(empty)"
    path_chain = []
    while tail != "":
        remainder, tail = os.path.split(remainder)
        if tail != "": path_chain.append(tail)
    path_chain.append(remainder)
    path_chain.reverse()
    return path_chain

def good_path(Directory, FileName):
    """Builds a good relative path consisting of the 'Directory' and the
    'File'.
    
    RETURNS: None      -- in case of non-existing path
             Path name
    """
    if not Directory: return FileName
    path = "%s/%s" % (Directory, FileName)
    path = os.path.normpath(path)
    try:    return relative(path)
    except: return None

def recursive_subdirectory_iterable(DirList, ExcludeDirPatternList=None):
    """Walks recursive along the each directory found in 'DirList'. 

    YIELDS: directory name (relative path to 'os.getcwd()')
    """
    assert type(DirList) == list
    done_set = set()
    for over_directory in DirList:
        over_directory = os.path.normpath(over_directory)
        yield over_directory
        done_set.add(over_directory)
        for directory, dummy, dummy in os.walk(over_directory):
            directory = os.path.normpath(relative(directory))
            if directory in done_set:                         continue
            elif     ExcludeDirPatternList is not None \
                 and match(directory, ExcludeDirPatternList): continue

            yield directory
            done_set.add(directory)

def files_of_directory(Dir, ExtensionList=None):
    file_list = [ "%s/%s" % (Dir, f) for f in os.listdir(Dir) ]

    if ExtensionList is None:
        return [ 
            f for f in file_list if os.path.isfile(f) 
        ]
    else:
        return [ 
            f for f in file_list
              if os.path.isfile(f) and any(f.endswith(x) for x in ExtensionList)
        ]

def close_directory_iterable(FocusDir, MaxDepth=None):
    """Walks through directories close to this directory first, then it searches
    for directories in nesting directories.
    
    MaxDepth tells how many directories at max. one should go backwards.
    
    YIELDS: directory name (relative path to 'os.getcwd()')
    """
    yield relative(FocusDir)

    path  = os.path.abspath(FocusDir)
    depth = -1
    while path and (MaxDepth is None or depth < MaxDepth): 
        depth += 1
         
        previous_path       = path
        path, sub_dir_to_me = os.path.split(path)
         
        for sub_dir in os.listdir(path):
            if sub_dir == sub_dir_to_me: continue
            directory = good_path(path, sub_dir)
            if not os.path.isdir(directory): continue
             
            for directory in recursive_subdirectory_iterable([directory]):
                yield directory
        
class FindAndSortDb:
    __slots__ = ("directory_set", "extension_list", "location_dir_db")

    def __init__(self):
        self.root_directory_db = defaultdict(set)
        self.selector_list     = []

    def register(self, DirectorySet, ExtensionList, location_db):

        selector_id = len(self.selector_list)
        self.selector_list.append((ExtensionList, location_db))

        for directory in DirectorySet:
            self.root_directory_db[os.path.abspath(directory)].add(selector_id)

    def do(self, ExcludePatternList, ExcludeDirPatternList, AbsolutePathF):
        """Iterates over all directories and their subdirectories found in FindAndSortDb.
        According to the given matches, it sorts the file names into specific 
        databases as they are given as the third argument of each 'line'.

        FindAndSortDb = list of the following:

              [0] -> set of directories of concern
              [1] -> file name pattern to be matched
              [3] -> database where the entry has to be made

        APPLIES: Changes the dictionaries given as [3] so that they contain an
                 updated mapping:

                       source file base name --> directory set

                 The directory set contains all directory where the file has 
                 been found.
        """
        db = self.get_directory_db(ExcludeDirPatternList)
            
        result     = defaultdict(set)
        backup_dir = os.getcwd()
        for directory, selector_id_set in sorted(db.iteritems()):
            try:    
                os.chdir(directory)
            except: 
                os.chdir(backup_dir)
                continue

            # Get list of file names in the directory
            file_name_list = os.listdir(os.getcwd())
            if ExcludePatternList:
                file_name_list = [ 
                    f for f in file_name_list if not match(f, ExcludePatternList) 
                ]

            os.chdir(backup_dir)

            for extension_list, location_db in (self.selector_list[sid] for sid in selector_id_set):
                concern_list = [
                    f for f in file_name_list if any((f.endswith(e) and f != e) for e in extension_list)
                ]

                rel_directory = None
                for f in concern_list: 
                    if rel_directory is None: 
                        rel_directory = relative(os.path.abspath(directory))
                    location_db[f].add(rel_directory) 

        os.chdir(backup_dir)
        return result

    def get_directory_db(self, ExcludeDirPatternList):
        """RETURNS: map

                 directory --> set of (Extension, location_db) pairs

        where 'directory' is a subdirectory of the given list of root directories.
        """
        result = defaultdict(set)
        for root_directory, selector_id_set in self.root_directory_db.iteritems():
            for directory in recursive_subdirectory_iterable([root_directory], ExcludeDirPatternList):
                result[directory].update(selector_id_set)
        return result

def is_subdirectory(Parent, Candidate):
    """RETURNS: True  -- if Candidate == Parent, or Candidate is 
                         a subdirectory of Parent.
                False -- else.
    """
    def normalize(Dir):
        return os.path.realpath(os.path.abspath(os.path.normpath(Dir)))

    normal_parent    = normalize(Parent)
    normal_candidate = normalize(Candidate)

    # Cut the directories from the tail of 'candidate' until either
    # the parent is equal to the 'head', or it is shorter than the
    # parent.
    L         = len(normal_parent)
    remainder = normal_candidate
    while len(remainder) >= L:
        remainder, tail = os.path.split(remainder)
        remainder = normalize(remainder)
        if remainder == normal_parent: return True

    return False
    
def relative_to_home_pretty(Dir):
    adapted_name = Dir
    home_dir     = common.home_directory()
    if adapted_name.startswith(home_dir):
        adapted_name = Dir[len(home_dir):]

    if adapted_name in ("", "./", "."):
        return "(this directory)"

    # safe, see entry of this function
    if adapted_name[0] == "/": adapted_name = adapted_name[1:]

    return adapted_name 

def match(Name, PatternList):
    for pattern in PatternList:
        if fnmatch(Name, pattern): return True
    return False

def replace_extension(FileName, Ext):
    return "%s%s" % (os.path.splitext(FileName)[0], Ext)

def verify_existence(FileSet):
    """RETURNS: True  -- if all files in SourceFileSet exist.
                False -- if not.

    """
    ok_f = True
    for file_name in FileSet:
        if os.path.isfile(file_name): continue
        print "Error: file '%s' does not exist." % file_name
        ok_f = False
    return ok_f

def relative(Path, RDir=None):
    """The 'relpath' may fail on operating systems, that have 'drive letters'.
    In that case, fall back on the absolute path.
    """
    if RDir is None: RDir = os.curdir

    try: 
        result = os.path.relpath(Path, RDir)
    except:
        result = os.path.abspath(Path)

    return result
