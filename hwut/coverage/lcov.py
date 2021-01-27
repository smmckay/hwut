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
# PURPOSE: 
#
# Parse the content of LCOV coverage information files as they are produced by
# 'lcov' and 'geninfo' by Peter Oberparleiter. The two mentioned programs are
# used to measure code coverage of C-programs. The result of the parsing is a
# database with the following structure:
#
#  coverage_db:  
#     .-----------.   .-------------------------------------------------.
#     | file name |-->| .file_name                                      |
#     '-----------'   | .test_list_by_function_db:                      |
#                     |    function name --> list [ (Test, Coverage) ]  |
#                     | .total:                                         |
#                     |    { .line; .branch; }                          |
#                     | .sub_coverage_db:                               |
#                     |    .---------------.   .---------.              |
#                     |    | function name |-->| .line   |              |
#                     |    '---------------'   | .branch |              |
#                     |                        '---------'              |
#                     '-------------------------------------------------'                     
#______________________________________________________________________________
#
# Manager:
#
# The interface to this module, as used by the test strategy is the 'Manager'.
# The 'Manager' can be (and is) applied in strategies which are applied 
# to directory trees. It has three member functions according to the three 
# major events of the strategies:
#
#               .on_test_done()
#               .on_directory_done()
#               .on_directory_tree_done()
#
# Upon a terminated test, the according '.info' files are collected. Once, a
# directory is done, its '.info' files are combined into one. Finally, all 
# directory's '.info' files are combined into one for the directory tree. The
# manager can respond to queries by the following functions:
#______________________________________________________________________________
# 
# The core functionality of this module is provided by the following functions:
#
#   parse(InfoFile) --> parsing the .info file (output of lcov).
#
#   save(TestName)  --> derives .info files for '.gcda' files in current 
#                       directory and saves them.
#
#   collect()       --> collects all .info files in a list of directories
#                       and derives a single .info file: 'hwut-lcov.info'.
#______________________________________________________________________________
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import hwut.common                 as common
import hwut.auxiliary.path         as path
import hwut.auxiliary.file_system  as fs
from   hwut.coverage.selector  import CoverageSelector
from   hwut.coverage.core      import Coverage, \
                                      CoverageDB, \
                                      CoverageDB_Entry
import hwut.auxiliary.executer.core as     executer

import sys
import os
import glob
from   copy        import copy
from   operator    import attrgetter, \
                          itemgetter
from   collections import namedtuple, \
                          defaultdict
import tempfile

# For LCOV/Gcov to work well, the following variables need to be set:
environment_db = { "LANG": "en", "LC_ALL": "", }

class Manager:
    """Manages the collection and parsing of 'lcov-related' data in the frame
    of strategies that walk along directory trees.
    """
    def __init__(self, NameF):
        """If NameF is set, then coverage results are labelled with the tests. 
        This allows to determine the tests which tested a particular function. 
        """
        self.mark_result_with_test_f      = NameF
        self.test_id_db                   = {}  # map: test-id --> Test object
        self.info_file_list               = []  # .info files of directory tree
        self.info_file_for_directory_tree = "hwut-lcov-all.info"
        self.coverage_db                  = CoverageDB()
        
    def on_test_done(self, TestInfo, Selector):
        test_id        = "%i" % len(self.test_id_db)
        info_file_list = save(test_id, self.mark_result_with_test_f, Selector)
        if info_file_list is None: return

        self.info_file_list.extend(info_file_list)
        self.test_id_db[test_id] = TestInfo

        # Absorb content of '.info' files into 'coverage_db'
        parser = Parser(Selector, self.coverage_db)
        for file_name in info_file_list:
            parser.do(file_name)
        
    def on_directory_tree_done(self):
        """Collect the .info files of all directories and build a single 
        .info file for the directory tree. 

        RETURNS: Coverage Database is shown in the head of this file.
        """
        for entry in self.coverage_db.itervalues():
            entry.finalize(self.test_id_db)

        collect(self.info_file_list, self.info_file_for_directory_tree)
        return self.coverage_db

def parse(InfoFile, TestIdDb=None, CovSelector=None):
    """Parse the 'InfoFile' which is of LCOV's '.info' file format. The 
    'TestIdDb' associates test-ids with Test objects.
    
    RETURNS: A coverage database as shown in the entry of this module.
    """
    if CovSelector is None: CovSelector = CoverageSelector()

    parser = Parser(CovSelector, {})
    parser.do(InfoFile)
    for file_name, content in parser.coverage_db.iteritems():
        content.finalize(None)
    return parser.coverage_db

def save(TestName, NamingF, Selector=None):
    """Save the current coverage data in and '.info' file which can later
    be processed by 'lcov'. The 'TestName' must be a unique identifier over
    all tests.

    This function iterates over all sub directories of the current directory.

    This function removes the '.gcda' files of the current directory.

    RETURNS: List of paths.

    The return value consists of the Absolute path of all '.info' files that 
    have been created.
    """
    global environment_db

    def extract_desired(InfoFileName, Selector):
        if Selector is None: return
        call_lcov(InfoFileName, "--extract", Selector.file.good_patterns())
        
    def remove_undesired(InfoFileName, Selector):
        if Selector is None: return
        call_lcov(InfoFileName, "--remove", Selector.file.bad_patterns())

    def call_lcov(InfoFileName, Mode, Patterns):
        """Call 'lcov' to '--remove' files or '--extract' files from the 
        content information of the data file.
        """
        if not Patterns: return

        tmp_file_name = tempfile.mktemp(".info", dir="./")

        option_list = [
            "-o",   tmp_file_name, 
            "--rc", "lcov_branch_coverage=1", 
            Mode,   InfoFileName
        ]
        option_list.extend(p for p in Patterns)

        cmd_line = common.get_lcov_application() + option_list

        executer.do(cmd_line, EnvDb=environment_db) 

        try: 
            os.rename(tmp_file_name, InfoFileName)
        except:
            pass

    # First, check whether there are actually some '.gcda' files in the current
    # directory. If not, then there is no need to collect lcov data.
    gcda_db = _gcda_db_construct()
    if not gcda_db: 
        print "Error: no coverage files found. Did you compile with '-coverage'?"
        # print "Error: cwd:", os.getcwd()
        # print "Error: gcda-files:", glob.glob("*.gcda")
        return None

    info_file_list = []
    backup_dir     = os.getcwd()
    for i, item in enumerate(gcda_db.iteritems()):
        directory, gcda_file_list = item 

        os.chdir(directory)

        info_file_name = "%s-%i.info" % (TestName, i)
        _gcda_files_collect(info_file_name, TestName, NamingF) 
        #if info_file_name == "13-0.info": os.system("cat 13-0.info")

        extract_desired(info_file_name, Selector)
        remove_undesired(info_file_name, Selector)

        fs.try_remove_files(gcda_file_list)
        info_file_list.append(os.path.abspath(info_file_name))
        os.chdir(backup_dir)

    return info_file_list

def collect(InfoFileList, ResultInfoFile):
    """Collect all data from the files in 'InfoFileList' and combine them into
    'ResultInfoFile'.
    """
    def filter(FileName):
        """And .info file that does not contain 'end_of_record' is not a good
        lcov output file.
        """
        fh = fs.open_or_die(FileName, "rb")
        verdict_f = (fh.read().find("end_of_record") != -1)
        fh.close()
        return verdict_f

    # Filter out files that have size zero or are not present.
    # (Current version of lcov may actuall fail to collect data without
    #  this filtering.)
    file_list = [
        file_name for file_name in InfoFileList
        if filter(file_name)
    ]

    if not file_list:
        # No files => generate empty output file.
        fh = fs.open_or_die(ResultInfoFile, "wb")
        fh.close()
    
    option_list = [
        "-o", ResultInfoFile, "--rc", "lcov_branch_coverage=1"
    ]
    option_list.extend(
        _get_add_file_options(file_list)
    )
    executer.do(common.get_lcov_application() + option_list)

def _get_add_file_options(InfoFileList):
    result = []
    for file_name in InfoFileList:
        result.append("-a")
        result.append(path.relative(file_name))
    return result

def _gcda_db_construct():
    """gcda_db: directory name --> list of gcda files in there.

    Consider the current working directory and all of its sub directories.
    Only those directories are entered which contain .gcda files.
    """
    backup_dir = os.getcwd()

    def add_if_has_gcda_files(gcda_db, Directory):
        if Directory in gcda_db: return
        
        os.chdir(Directory)
        file_list = glob.glob("*.gcda")
        if file_list: gcda_db[Directory] = file_list
        os.chdir(backup_dir)
        
    result         = {}
    last_directory = None
    for directory, dummy, dummy in os.walk(backup_dir):
        if directory == last_directory: continue
        add_if_has_gcda_files(result, directory)
        last_directory = directory
    return result

def _gcda_files_collect(InfoFileName, TestName, NamingF):
    """Collects content of all '.gcda' files in current directory and combines
    them into a single '.info' file.
    """
    option_list = [
        "--capture", 
        "--directory", ".", 
        "--rc",        "lcov_branch_coverage=1",
        "-o",          InfoFileName
    ]
    if NamingF: 
        option_list.extend(["--test-name", TestName])

    cmd_line = common.get_lcov_application() + option_list
    executer.do(cmd_line, EnvDb=environment_db)

#______________________________________________________________________________
#
# .info-file parser:
#
class ParserData_File:
    def __init__(self, AbsSourceFileName=""):
        self.file_name      = AbsSourceFileName
        self.test_id        = ""

        self.function_db  = []
        self.branch_db    = {}
        self.line_db      = {}

    def function_iterable(self):
        """Iterate over functions. 

        YIELDS:  line number of begin, line number of end, function name
        """
        if not self.function_db:
            return

        # Sort by line number
        self.function_db.sort(key=itemgetter(0))

        line_begin, name, coverage_f = self.function_db[0]
        for line_end, next_name, next_coverage_f in self.function_db[1:]:
            if coverage_f:
                yield line_begin, line_end, name
            line_begin  = line_end
            name        = next_name
            covervage_f = next_coverage_f

        if coverage_f:
            yield line_begin, 1e37, name

Function = namedtuple("Function", ("line_begin", "name", "coverage_f"))

def new_source_file(data, MObj):
    if data.current is None:
        data.current = ParserData_File()
    data.current.file_name = MObj.group(1)

    # The function name filter must be adapted to the given file name.
    if data.selector is not None:
        data.selector.function.setup(data.current.file_name)

def attr_test_name(data, MObj):
    if data.current is None:
        data.current = ParserData_File()
    data.current.test_id = MObj.group(1)

def function_db_register(data, MObj):
    line_begin    = int(MObj.group(1))
    function_name = MObj.group(2)

    # 'new_source_file()' --> 'selector.function.setup(file name)'
    # => 'selector.function.is_admissible()' can be called.
    if data.selector is not None:
        coverage_f = data.selector.function.is_admissible(function_name)
    else:
        coverage_f = True

    data.current.function_db.append(
        Function(line_begin, function_name, coverage_f)
    )

def branch_db_register(data, MObj):
    line_begin   = int(MObj.group(1))
    block_id     = int(MObj.group(2))
    branch_index = int(MObj.group(3))
    passed_f     = MObj.group(4)

    # NOTE: The 'block_id' and 'branch_index' do not seem to identify a block
    #       distincly. Include the block's line number to be precise.
    branch_id = (line_begin, block_id, branch_index)
    if branch_id in data.current.branch_db:
        print "Error: Block/Branch mentioned twice for one file/test."
        print "Error: file: %s" % data.current.file_name
        print "Error: branch_id", branch_id
        return

    data.current.branch_db[branch_id] = (passed_f == "1")

def line_db_register(data, MObj):
    line_begin  = int(MObj.group(1))
    pass_number = int(MObj.group(2))
    
    data.current.line_db[line_begin] = not (pass_number == 0)

def end_of_record(data, MObj):
    data.on_end_of_record()

class Parser:
    __slots__ = ("current", "coverage_db", "selector")

    match_box = [
        (common.re_compile("^%s" % pattern), function) 
        for pattern, function in [
            ("TN:([^\n]+)",                              attr_test_name),
            ("SF:([^\n]+)",                              new_source_file),
            ("FN:([0-9]+),([^\n]+)",                     function_db_register),
            ("BRDA:([0-9]+),([0-9]+),([0-9]+),([^\n]+)", branch_db_register),
            ("DA:([0-9]+),([0-9]+)",                     line_db_register),
            ("end_of_record",                            end_of_record),
        ]
    ]

    def __init__(self, CovSelector, CoverageDb):
        self.selector    = CovSelector
        self.coverage_db = CoverageDb
        self.clear()

    def clear(self):
        self.current = None

    def do(self, FileName):
        try:    fh = fs.open_or_die(FileName, "rb")
        except: return None

        self.clear()
        for mobj, function in Parser.match_iterable(fh):
            function(self, mobj)

    def on_end_of_record(self):
        """End of record. That is the description of a coverage/test case has
        ended. Translate the parsed data into a 'CoverageDB_Entry'.
        """
        if self.current is None: 
            return

        if    self.selector is None \
           or self.selector.file.is_admissible(self.current.file_name): 
            entry = self.coverage_db.get(self.current.file_name)
            if entry is None:
                self.coverage_db[self.current.file_name] = CoverageDB_Entry(self.current)
            else:
                entry.merge(self.current)

        self.current = None

    @classmethod
    def match_iterable(cls, fh):
        """Iterate over matching lines for 'match_box'.

        YIELDS: [0] Match object when a line has matched.
                [1] Function that needs to be called.

        The content of the match can be read from the match object's 'group(i)'
        member function.
        """
        for line in fh.readlines():
            for regex, function in cls.match_box:
                mobj = regex.match(line)
                if mobj is None: continue
                yield mobj, function
                break

