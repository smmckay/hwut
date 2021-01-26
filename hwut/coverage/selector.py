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
from   collections import defaultdict
import os
import fnmatch

class CoverageSelector:
    """Selects directory, files, and functions to be considered for coverage 
    analysis. A 'CoverageSelector's decision about admissibility is accessed 
    by the functions

       .file.is_admissible(FileName)

            which tells whether the 'FileName' is to be considered for 
            coverage analysis.

       .function.is_admissible(FuncName)

            which tells whether the 'FuncName' is to be considered.

    Before '.function.is_admissible()' can be called the function selector
    must be setup for a specific file by

       .function.setup(FileName)

    ___________________________________________________________________________

    SPECIFICS:

    A 'CoverageSelector' is setup through a configuration in a 'hwut-info.dat'
    file. As a result, both, the file and the function selector of this object
    contain a 'good_db' and a 'bad_db'. The general idea is that 

        (i)  A 'good database' restricts by defining what is good. If it is
             not defined, then everything is good--apriori.

        (ii) A 'bad database' restricts by extracting what is bad from the set
             that remains.
    ___________________________________________________________________________
    """
    def __init__(self): 
        self.reference_table = None
        self.file     = FileSelector()
        self.function = FunctionSelector()

    def add_positive(self, PathPattern, FunctionPattern):
        """Add a selection rule, that says:

        -- DO consider files that match 'AntiPathPattern', except for 
        -- those functions in there which DO match the 'AntiFunctionPattern'.

        At the end, if a function does not match one anti pattern, it is enough
        to be considered.
        """
        CoverageSelector._add(self.file.good_db, self.function.good_db, 
                              PathPattern, FunctionPattern)


    def add_negative(self, AntiPathPattern, AntiFunctionPattern):
        """Add a selection rule, that says:

        -- Do NOT consider files that match 'AntiPathPattern', except for 
        -- those functions in there which do NOT match the 'AntiFunctionPattern'.

        At the end, if a function does not match one anti pattern, it is enough
        to be considered.
        """
        CoverageSelector._add(self.file.bad_db, self.function.bad_db, 
                              AntiPathPattern, AntiFunctionPattern)

    @staticmethod
    def _add(absolute_db, db, PathPattern, FunctionPattern):
        if os.path.basename(PathPattern) == PathPattern:
            path_f = False
            name   = PathPattern
        else:
            path_f = True
            name   = os.path.abspath(PathPattern)
       
        # 'absolute_db' contains files/paths which are not to appear at all.
        # 'db' contains for files/paths/ what functions are forbidden. 
        # => 'db' is more permissive (if bad), or restrictive (if good) 
        # and outrules 'absolute_db'.
        if FunctionPattern is None:       
            if name not in db:               
                absolute_db[name] = path_f  
        else:
            if name in absolute_db: 
                absolute_db.remove(name)
            db[name].add((path_f, FunctionPattern))

    def absolute_bad_paths(self):
        return self.file.bad_db.keys()

class FileSelector:
    """________________________________________________________________________
    Determines based on its 'good_db' and 'bad_db' whether a file with a
    given name has to be considered for coverage analysis.

        good_db: path pattern --> path_f (True, if path, False, if pattern)
                 => keys of good_db are the patterns of selected files.
        bad_db:  path pattern --> path_f (True, if path, False, if pattern)
                 => keys of bad_db are the patterns of disallowed files.
    __________________________________________________________________________
    """
    def __init__(self):
        self.good_db = {}   
        self.bad_db  = {}

    def is_admissible(self, FileName):
        """Considers the directory and base name of the given file. For the 
        decision process.

        RETURNS: True if admissible, False if not.
        """
        if   not self.good_db:                                pass
        elif not FileSelector._match(self.good_db, FileName): return False

        if   not self.bad_db:                                 pass
        elif FileSelector._match(self.bad_db, FileName):      return False

        return True

    def admissible_iterable(self, FileNameList):
        for file_name in FileNameList:
            if self.is_admissible(file_name):
                yield file_name

    def bad_patterns(self):
        return self.bad_db.keys()

    def good_patterns(self):
        return self.good_db.keys()

    @staticmethod
    def _match(absolute_db, FileName):
        """RETURNS: True  -- if 'FileName' matches a path in 'absolute_db'
                    False -- if not
        """
        abs_name = os.path.abspath(FileName)
        name     = os.path.basename(FileName)

        for pattern, path_f in absolute_db.iteritems():
            if path_f: 
                if fnmatch.fnmatch(abs_name, pattern): return True
            else:
                if fnmatch.fnmatch(name, pattern):     return True

        return False

class FunctionSelector:
    """________________________________________________________________________
    An object of this class is able to distinguish between functions which
    have to be considered and which need not. After the object has been 
    setup properly for a particular file, the member function 
    
                        .is_admissible(FuncName)

    provides an answer to the question, whether a 'FuncName' is a function to 
    be considered. 
    ___________________________________________________________________________
    INTERNAL:

        .good_db: path pattern --> SELECTED function patterns.
        .bad_db:  path pattern --> DISALLOWED function patterns.

    Due to a call to '.setup(FileName)' the set good_patterns and bad_patterns
    is determined.

        .good_pattern_set --> set of function name patterns which are allowed for
                         the given file. 

        .bad_pattern_set --> set of function name patterns which are not to
                              be considered for current file.

    See functions '.is_admissible()' and '._match()' for an explanation of the
    filtering process.
    ___________________________________________________________________________
    """
    def __init__(self):
        self.good_db = defaultdict(set)
        self.bad_db  = defaultdict(set)

        # The 'good_pattern_set' and the 'bad_pattern_set' are determined upon call 
        # to '.setup()' for a particular file.
        self.good_pattern_set = None
        self.bad_pattern_set  = None

    def setup(self, SourceFileName):
        """Prepares '.good_pattern_set' and '.bad_pattern_set' for the function 
        '.is_admissible' to be called for functions of the given file.
        """
        abs_file_name = os.path.abspath(SourceFileName)

        self.good_pattern_set = FunctionSelector._prepare(self.good_db, 
                                                          abs_file_name)
        self.bad_pattern_set  = FunctionSelector._prepare(self.bad_db, 
                                                          abs_file_name)

    @staticmethod
    def _prepare(Db, AbsFileName):
        if not Db: return None

        base_name = os.path.basename(AbsFileName)
        result    = None
        for pattern, info_set in Db.iteritems():
            for path_f, function_pattern in info_set:
                # path_f: True  -- 'pattern' is understood as path.
                #         False -- 'pattern' is understood as file.
                if path_f: candidate = AbsFileName
                else:      candidate = base_name

                if not fnmatch.fnmatch(candidate, pattern): continue

                if result is None: result = set()
                result.add(pattern)                 
        
        return result

    def is_admissible(self, FuncName):
        """If there's one single pattern in the PatternSet that does not
        match 'FuncName' then it is admissible.

        RETURNS: True  -- if FuncName is addmissble.
                 False -- if it is not.
        """
        if self.good_pattern_set is None:
            pass
        elif not FunctionSelector._match(self.good_pattern_set, FuncName):
            return False

        if self.bad_pattern_set is None:
            pass
        elif FunctionSelector._match(self.bad_pattern_set, FuncName):
            return False

        return True

    @staticmethod
    def _match(PatternSet, FuncName):
        """RETURNS: True  -- if there is a pattern that matches 'FuncName'.
                    False -- if not.
        """
        if FuncName in PatternSet: return True

        for pattern in PatternSet:
            if   pattern is None: continue
            elif fnmatch.fnmatch(FuncName, pattern): return True
        return False


