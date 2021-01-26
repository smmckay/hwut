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
# PURPOSE: The file 'hwut-info.dat' in each test directory is the primary
#          source of information about the test applications in the directory
#          and how they are supposed to be executed. 
#
# .------------------------.    .-----------------------.    .-------------------.
# | File names reported by |    | File names in current |    | Remotely executed |
# | > make hwut-info       |    | directory.            |    |       Tests       |
# '------------------------'    '-----------------------'    '-------------------'
#            |                              |                          |
#            |                         match against                   |
#            |                      possitive patterns                 |
#            |                              |                          |
#            '---------------. .------------'                          |
#                            | |     .---------------------------------'
#                      exclude file names
#                     mentioned as '--not' 
#                              |
#               .-------------------------------.
#               | Set of test application names |
#               '-------------------------------'
# 
# This file contains functions to access the content of this hwut-info.dat and 
# to filter content of the current directory. As a special feature it may 
# generate 'hwut-info.dat' files for the case that it is missing. In that case, 
# it derives it from the 'old traditional way' of finding test executables.
#
# The following sections are possible:
#
# (1) Title
#
#     A title section describes the purpose of the tests in a single line.
# 
# (2) File patterns and anti-patterns:
# 
#     * Patterns that match against test applications and define the
#        interpreter sequence. 
#
#     * '--not' patterns for files of this directory which are NOT to be 
#               considered as test applications.
#
#     * '--coverage' path-pattern function-pattern
#               Tells that for files that match a given 'path-pattern' the 
#               only functions are considered that match athe 'function-
#               pattern'.
#
# (3) Documentation
#
#     A documentation section elaborates on the overall idea of the testing
#     provided in this directory. The content of documentation is free-style.
#
# A hwut-info.dat file may contain multiple sections. Sections are separated by
# dashed lines. Depending on the number of sections, their meaning is defined.
#
# EXAMPLE:
# 
#    This is the title of all tests.
#    ----------------------------------------
#    python  my-test*.py
#    --not   __init__.py
#    ----------------------------------------
#    In this directory some tests are done 
#    which are necessary to check whether ...
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
from   hwut.common                import HWUT_INFO_FILE_NAME
from   hwut.coverage.selector     import CoverageSelector
import hwut.auxiliary.make        as     make
import hwut.auxiliary.file_system as     fs
import hwut.auxiliary.executer.remote.parse_config as parse_remote_config 
import hwut.auxiliary.executer.remote.base         as remote 

import os
import sys
import stat
import fnmatch
from   collections import namedtuple

import re

class TestExecutionInfoDB(object):
    """.title   = Title of the tests in the current directory.
       .db      = Test execution database, i.e. a map:

                  test application name --> TestExecutionInfo.

       .comment = Comment on the tests of this directory.
       .selector_test     = Selector to determine what tests to consider.
       .selector_coverage = Selector to determine what files to ignore during
                            coverage analysis.
    """
    __slots__ = ("db", "title", "comment", "selector_coverage", "selector_test")
    def __init__(self, Db, Title, Comment, CoverageSelector, TestSelector):
        self.db                = Db
        self.title             = Title
        self.comment           = Comment
        self.selector_test     = TestSelector
        self.selector_coverage = CoverageSelector

    def admissible_iteritems(self):
        for name in self.selector_test.admissible_applications(self.db.iterkeys()):
            yield name, self.db[name]


class TestExecutionInfo(object):
    """Specifies the very basic information about test applications. That is, 
    it tells about 

        -- the test application's file name

        -- the sequence of interpreters used to execute the application.

        -- post processors of the standard output and error output that is
           received from the application.

        -- a flag that tells whether a build procedure (make) is involved
           to generate the test application.  
    """
    __slots__ = ("name", "interpreter_sequence", 
                 "stdout_post_processor", "stderr_post_processor", "make_f", 
                 "remote_config_id")
    def __init__(self, Name, InterpreterSequence, 
                 StdoutPostProcessor, StderrPostProcessor, 
                 RemoteConfigId):
        self.name                  = Name
        self.interpreter_sequence  = InterpreterSequence
        self.stdout_post_processor = StdoutPostProcessor
        self.stderr_post_processor = StderrPostProcessor
        self.make_f                = False
        self.remote_config_id      = RemoteConfigId

    def set_make_f(self):
        self.make_f = True

    def __str__(self):
        return "".join([
            "   name:             %s;\n" % self.name,
            "   interpreter_seq:  %s;\n" % self.interpreter_sequence,
            "   stdout_post_proc: %s;\n" % self.stdout_post_processor,
            "   stderr_post_proc: %s;\n" % self.stderr_post_processor,
            "   make_f:           %s;\n" % self.make_f,
        ])

def get_TestExecutionInfoDb(Selector):
    """RETURNS: TestExecutionInfoDB -- in case that this could be built.
                None                -- else.
    """
    title, basic_db, comment, coverage_selector = do()

    if basic_db is None:
        return None
    
    # We are NOT selecting here. Later we need to consider the whole database.
    # Selecting here, would impose a filter on what could be considered in 
    # the databse.
    return TestExecutionInfoDB(basic_db, title, comment, coverage_selector, 
                               Selector)

def do():
    """Consider the file 'hwut-info.dat' and the response of the Makefile
    to 'make hwut-info'. Test applications reported by 'make hwut-info' are
    always considered, except if they are cancelled by a '--not' line in the
    'hwut-info.dat' file. Other files of this directory need match one of
    the patterns in the pattern section, in order to be considered a test
    application.

    RETURNS: [0] Title for the tests in this directory
             [1] Basic database matching from file name patterns to information
                 about how to execute the test.
             [2] Comments on the tests in this directory.
             [3] Coverage Selector

    The [1] element is None, in case that no test applications could be found.
    """
    try:    
        fh = open(HWUT_INFO_FILE_NAME, "rb")
    except: 
        return __setup_by_Makefile_only()

    return __setup_by_hwut_info_and_Makefile(fh)

def __setup_by_hwut_info_and_Makefile(fh):
    """Extracts test application information from the 'hwut-info.dat' file and
    the Makefile if it is there. 
    
    -- Interpretation of Makefile by: 

           do_pattern_section() --> _filter() --> get_candidates()
                                --> make.get_makeable_application_list()

       where 'get_candidates()' collects the names of all files present in the
       directory plus the application names received by 'make hwut-info'.

    -- Remote execution setup and query by:

           do_pattern_section() --> _filter() --> get_candidates()
                                --> remote.get_remote_application_list()

    """
    # Parse the three sections of 'hwut-info.dat'
    while 1 + 1 == 2:
        # Title
        title, verdict     = do_text_section(fh)
        if not verdict: break

        # Patterns and Anti-Patterns
        basic_db, verdict, \
        coverage_selector  = do_pattern_section(fh)
        if not verdict: break

        # Comment
        comment, verdict   = do_text_section(fh)

        return title.strip(), basic_db, comment, coverage_selector

    print "Error: not enough sections in '%s'" % HWUT_INFO_FILE_NAME
    print "Error: required 3 sections for title, patterns, and comment."
    print "Error: all sections need to be seperated by dashed lines."
    sys.exit()

def __setup_by_Makefile_only():
    """Derive the setup SOLELY from the 'Makefile'.

    This function helps in case there is no 'hwut-info.dat' file. The Makefile
    if it is there. The interpretation of the Makefile happens through A

                      _filter(TrueDb={}) --> get_candidates()

    Passing an empty 'TrueDb' prevents that any file from the current directory
    is considered, apriori. An exception are those files which are reported
    by 'make hwut-info'.
    """
    title     = "<no file '%s', no title>" % HWUT_INFO_FILE_NAME
    basic_db  = _filter(TrueDb={}, FalseSet=set())
    comment   = "<no file '%s', no comment>" % HWUT_INFO_FILE_NAME

    if len(basic_db) == 0: basic_db = None

    return title, basic_db, comment, None

def do_text_section(fh):
    """Read text until the next dashed line.

    RETURNS: Text that has been read until the detection of the 
             first dashed line.
    """
    verdict = False
    result  = ""
    while 1 + 1 == 2:
        line = fh.readline()
        if not line: 
            break
        stripped_line = line.strip()
        if stripped_line.find("----") == 0:
            verdict = True
            break
        result += line

    return result, verdict

def do_pattern_section(fh):
    """Parses 'hwut-info.dat'. Then, it filters files in the current directory 
    according to the parsed content. The test file names in reported by the
    Makefile upon 'make hwut-info' are also considered.

    Some tests may be built by 'make'. In that case, the 'make_f' is set to 
    'True', else it is False.
       
    RETURNS: A map:
 
                        file name --> TestExecutionInfo

             None is returned, if no file "hwut_info.dat" has been found.

    A TestExecutionInfo consists of: 
            
             - the test application name
             - the interpreter list
             - the stdout post processor
             - the stderr post processor

    The keys of the map are the names of files to be executed. For each file the
    sequence of interpreter names tells how the script may be executed. For 
    example:

             ... "mine.txt": (["awk", "filter.awk"], False), ...

    says that the 'awk' program is to be used to run 'filter.awk' which will
    interpret the file 'mine.txt'. When a file is directly handled no such 
    interpreters are necessary. The 'False' tells, that the file is not 
    made by make.

    NOTE: There is another source of test file specifications: 'Makefiles'
    """
    true_db, false_set, remote_config_db, coverage_selector = _parse(fh)

    return _filter(true_db, false_set, remote_config_db), True, coverage_selector

def _parse(fh):
    """RETURNS:

       [0] true_db: A map that maps from file name patterns to a tuple with:
                    [0] The sequence of interpreters which needs to be applied 
                        to execute the file
                    [1] The post processor of stdout (or None)
                    [2] The post processor of stderr (or None)

       [1] false_set: A set of file name patterns for files which are not
                      subject to testing.

       [2] remote configuration database: 
            
                    config-id --> RemoteConfiguration

       [3] coverage_selector

       None, None, None, None is returned if no 'hwut-info.dat' files has been found.

    Lines starting with '##' are considered command lines.
    """
    def snap_line(fh):
        """See comment of 'snap_line_core().'
        """

        while 1 + 1 == 2:
            id, line = snap_line_core(fh)

            # End of file --> break
            if line is None: break
            
            line = expand_environment_variables(line)

            # Error in variable expansion --> next line
            if line is None: continue

            break
           
        return id, line

    def snap_line_core(fh):
        """RETURNS: 0, None -- empty line
                    1, text -- 'negated' line
                    2, text -- stderr post processor
                    3, text -- stdout post processor
                    4, text -- application specification
                    5, text -- coverage not: path-pattern + function-pattern
                    6, text -- coverage:     path-pattern + function-pattern
                    7, text -- remote:       type':' name ';' '{' list-of( name ':' value ';') '}'
        """
        line = fh.readline()
        if not line: return None, None

        line = line.strip()
        if   not line:                          return 0, None
        elif line.find("---")   == 0:           return None, None
        elif line.find("##")    == 0:           return 0, None
        elif line.find("--not") == 0:           return 1, line[len("--not"):].strip()
        elif line.find("|&")    == 0:           return 2, line[len("|&"):].strip()
        elif line.find("|")     == 0:           return 3, line[len("|"):].strip()
        elif line.find("--coverage-not") == 0:  return 5, line[len("--coverage-not"):].strip()  # FIRST
        elif line.find("--coverage") == 0:      return 6, line[len("--coverage"):].strip()      # SECOND (NOT vice versa)
        elif line.find("--remote") == 0:        return 7, line[len("--remote"):].strip()        # SECOND (NOT vice versa)
        # elif line.find("--build") == 0:   return 6, line[len("--build"):].strip()
        # elif line.find("--define") == 0:  return 7, line[len("--define"):].strip()
        elif line.find("--") == 0:              
            print "%s: option '%s' unknown." % (HWUT_INFO_FILE_NAME, line.split()[0])
            sys.exit()
            return None, None
        else:                                   
            return 4, line

    def snap_post_processors(fh):
        stdout_post_proc = None
        stderr_post_proc = None
        while 1 + 1 == 2:
            pos = fh.tell()
            line_type, line = snap_line(fh)
            if   line_type == 2: stdout_post_proc = line
            elif line_type == 3: stderr_post_proc = line
            else:                break
        fh.seek(pos) 
        return stdout_post_proc, stderr_post_proc

    def snap_TestExecutionInfo(fh, line):
        fields               = line.split()
        file_name_pattern    = fields[-1]   
        interpreter_sequence = fields[:-1]

        if file_name_pattern in true_db:
            print "Error: '%s' has beem defined more than once." % file_name_pattern

        stdout_post_proc, stderr_post_proc = snap_post_processors(fh)            

        return file_name_pattern, TestExecutionInfo(file_name_pattern, interpreter_sequence, 
                                                    stdout_post_proc, stderr_post_proc, None)

    true_db = {}
    false_set = set()

    # All patterns of directories are considered relative to the directory where the 
    # 'hwut-info.dat' file was located.
    coverage_selector       = CoverageSelector()
    remote_configuration_db = {}

    while 1 + 1 == 2:
        line_type, line = snap_line(fh)
        if line_type is None: 
            break
        elif line_type == 0: 
            continue
        elif line_type == 1:
            false_set.update(line.split())
        elif line_type == 4:
            pattern, test_app = snap_TestExecutionInfo(fh, line)
            true_db[pattern]  = test_app
        elif line_type == 5:
            anti_path_pattern, anti_function_pattern = get_coverage_selector_patterns(line)
            coverage_selector.add_negative(anti_path_pattern, anti_function_pattern)
        elif line_type == 6:
            path_pattern, function_pattern = get_coverage_selector_patterns(line)
            coverage_selector.add_positive(path_pattern, function_pattern)
        elif line_type == 7:
            config = parse_remote_config.do(line)
            if config is not None:
                remote_configuration_db[config.id] = config

        # elif line_type == 6:
        #    build_target_pattern, \
        #    build_dependency_list, \
        #    build_commands       = get_build_rule(line)

    if not remote_configuration_db: remote_configuration_db = None
    return true_db, false_set, remote_configuration_db, coverage_selector

def _filter(TrueDb, FalseSet, RemoteConfigurationDb=None):
    """Find all finds in the current directory which may be subject to testing
    according to the 'hwut-info.dat' file. 

    The keys of 'TrueDb' are understood as 'fnmatch' regular expressions. That 
    is '*' is a wildcard for any matching letter and '?' may match a single 
    letter.

    RETURNS: A map:
 
              file name --> (sequence of interpreter names, make_f)

    The 'file name' is a test which is available and can be executed. The 
    'sequence of interpreter names' is what is required for the interpretation
    or parsing of the test. If the file itself is executable (may be by a 
    'shebang') then no interpreters may be required.
    """
    def is_excluded(FileName):
        """RETURNS: True  -- if FileName matches a name in FalseSet. 
                    False -- if not.
        """
        if FileName in FalseSet: 
            return True
        for pattern in FalseSet:
            if fnmatch.fnmatch(FileName, pattern): return True
        return False

    def get_TestExecutionInfo(FileName, MakeF, RemoteConfigId):
        """RETURNS: TestExecutionInfo, if FileName matches something in 'TrueDb'. 
                    None, else.

        Files which are reported by 'make hwut-info' are ALWAYS considered,
        except if they are explicitly taken out by '--not'.
        """
        if is_excluded(FileName): # Matching entry in 'FalseSet' forbids 
            return None           # further consideration.

        # -- Get entry by match against 'TrueDB' patterns
        test_app = TrueDb.get(FileName)
        if test_app is None: 
            for pattern, candidate in TrueDb.iteritems():
                if fnmatch.fnmatch(FileName, pattern): 
                    test_app = candidate
                    break
    
        # -- No match => if make-able generate entry anyway.
        if test_app is None:
            if not MakeF: return None
            test_app = TestExecutionInfo(FileName, [], None, None, RemoteConfigId)

        if MakeF: test_app.set_make_f()
        return test_app

    # map: pattern --> TestExecutionInfo
    basic_db = {}
    iterable = get_candidates(MakeOnlyF=not TrueDb, 
                              RemoteConfigurationDb=RemoteConfigurationDb)

    for file_name, make_f, remote_config_id in iterable:
        test_app = get_TestExecutionInfo(file_name, make_f, remote_config_id)
        if test_app is None: continue
        basic_db[file_name] = test_app

    return basic_db

def get_candidates(MakeOnlyF, RemoteConfigurationDb):
    """RETURNS: list of tuples (file_name, make_f, remote_config_id)

        make_f           = True,  if application is made by 'make'/Makefile.
                           False, else.

        remote_config_id = None, if application is NOT remotely located.
                           else, if application lives on the site reached by 
                                 remote_config_id.

    The file names listed are all files in the current directory plus the files
    which are reported by the Makefile ("make hwut-info"). The second element 
    in the result tuples tells wether the file is 'maked' or just is there.
    """
    # .---.
    # | 1 | Makeable applications
    # '---'
    makeable_set = set(make.get_makeable_application_list())
    file_name_list = [
        (file_name, True, None) for file_name in makeable_set
    ]

    if MakeOnlyF: return file_name_list

    # .---.
    # | 2 | Other files from the directory
    # '---'
    file_name_list.extend(
        (file_name, False, None) 
        for file_name in fs.get_file_name_list_in_directory()
        if file_name not in makeable_set
    )

    # .---.
    # | 3 | Remotely-located test applications
    # '---'
    file_name_list.extend(
        (app, False, remote_config_id) 
        for remote_config_id, app in remote.get_remote_application_list(RemoteConfigurationDb)
    )

    file_name_list.sort()
    return file_name_list
    
def auto_generate(TrueDb, FalseSet):
    """Auto-generates the 'hwut-info.dat' file based on the given information.
    The 'TrueDb' is a map of lists. Each element of the list corresponds to a
    specification. The key is a pattern which may match file names, the value 
    is the sequence of interpreters. 

    Example:  

          TrueDb = {
                "first.sh":    [],
                "second.py":   ["python"],
                "third-a.txt": ["awk",    "filter.awk"],
                "third-b.txt": ["awk",    "filter.awk"],
                "third-c.txt": ["awk",    "filter.awk"],
          }

    The 'FalseSet' specifies the files which are never to be consired as part
    of the test.

    The first list specifies that the script 'first.sh' can be executed from
    the command line without any further interpreter specification. File
    'second.py' is interpreted by python. The files 'third-a.txt' to 'third-c.txt'
    are processed by an awk-script which is interpreted by awk.
    """

    # If the file is already there, then we will not auto-generate it!
    if os.access(HWUT_INFO_FILE_NAME, os.R_OK):
        print "Error: refused to auto-generate '%s'." % HWUT_INFO_FILE_NAME
        print "Error: File already exists."
        return

    fh = fs.open_or_die(HWUT_INFO_FILE_NAME, "wb")

    if TrueDb:
        max_element_n = max(len(spec) for spec in TrueDb)
        L_array       = [ 0 ] * (max_element_n + 1)
        for file_pattern, interpreter_sequence in TrueDb.iteritems():
            i = 0
            for i, x in enumerate(interpreter_sequence):
                if len(x) > L_array[i]: L_array[i] = len(x)
            if len(file_pattern) > L_array[i+1]:
                L_array[i+1] = len(file_pattern)
     
        for file_pattern, interpreter_sequence in TrueDb.iteritems():
            for i, x in enumerate(interpreter_sequence):
                fh.write(x)
                fh.write(" " + " " * (L_array[i] - len(x)) + " ")
            fh.write("%s\n" % file_pattern)

    for i, spec in enumerate(sorted(list(FalseSet))): 
        if i % 10 == 0: fh.write("\n--not ")
        fh.write("%s " % spec)

    fh.close()
        
def access(Mode):
    """Tries to access the 'hwut-info.dat' file in the current directory.
    RETURNS: File handle to read from 'hwut-info.dat'
             None,       if access has failed.
    """
    try:
        return open(HWUT_INFO_FILE_NAME, Mode)
    except:
        pass

    try:
        os.chmod(HWUT_INFO_FILE_NAME, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        return open(HWUT_INFO_FILE_NAME, Mode)
    except:
        return None

def get_coverage_selector_patterns(Line):
    """The --coverage line is followed by two patterns: The 'path-pattern' and
    optionally the 'function-pattern'.

    RETURNS: [0] path pattern
             [1] function pattern 
                 = None if there's no anti-function pattern, that is every 
                 function is excluded.

    If a file matches the path pattern it is considered for coverage analysis. But, 
    all functions in this file must now match the function pattern in order to be   
    considered.
    """
    def clean_dir(D):
        if D and (D[-1] == "\\" or D[-1] == "/"): return D[:-1]
        else:                                     return D

    pattern_list = Line.split()
    if not pattern_list:
        print "Error: Require at least one pattern following --coverage"
        sys.exit()

    path_pattern = clean_dir(pattern_list[0])
    if len(pattern_list) < 2:
        return path_pattern, None

    function_pattern = pattern_list[1]
    if len(pattern_list) > 2:
        print "Error: More than two patterns found following --coverage"
        sys.exit()

    return path_pattern, function_pattern
    
re_env  = re.compile("\\${([^}]+)}")
def expand_environment_variables(Line):
    """Tries to expand environment variables in the given 'Line'. Terms in '${ ... }'
    expressions are expanded to the value of th corresponding environment variable.

    RETURNS: None   if there was a reference to an environment variable which is not 
                    defined.
             string containing the env-variable replaced line. This may be very well
                    the exact same line as in the input.
    """
    global re_env

    if Line.find("${") == -1: return Line

    line = Line
    while 1 + 1 == 2:
        match = re_env.search(line)
        if match is None: break
        groups = match.groups()
        if len(groups) != 1: break
        variable = groups[0]

        replacement = os.environ.get(variable)
        if replacement is None:
            print "Error: undefined environment variable %s in line" % variable
            print "Error: '%s'" % Line
            return None

        # Make sure that any whitespace is deleted: .strip()
        line = re_env.sub(replacement.strip(), line, 1)

    return line
    
    
