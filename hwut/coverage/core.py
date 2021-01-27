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

from   collections import defaultdict
import os
import fnmatch
from   operator    import itemgetter

class Coverage(object):
    """Line and branch coverage data storage. A Coverage object can be specified
    directly by the values for line and brach coverage. But, those value can 
    also be derived from line and coverage databases (see '.from_databases()').

    A line coverage database must have the following structure:

             map: line-number --> covered_f

    Similarly, a branch coverage database must have the structure

             map: branch-id   --> covered_f

    For this class, the branch-id's structure is unimportant. If there is no 
    branch at all the coverage is reported as 'None'.
    """
    __slots__ = ("line", "branch")

    def __init__(self, LineCoverage, BranchCoverage):
        self.line   = LineCoverage
        self.branch = BranchCoverage
    
    @staticmethod
    def from_databases(LineDb, BranchDb, LineBegin, LineEnd, TotalF=False):
        result = Coverage(
            Coverage.get_line_coverage(LineDb, LineBegin, LineEnd),
            Coverage.get_branch_coverage(BranchDb, LineBegin, LineEnd, TotalF)
        )
        return result
                
    @staticmethod
    def get_line_coverage(CombinedLineDb, LineBegin, LineEnd):
        """Determines line coverage of lines from 'LineBegin' to 'LineEnd'. If
        there are no lines, then a coverage of '1.0' is returned.

        RETURNS: line coverage.
        """
        coverage   = 0
        line_count = 0
        for line_n, covered_f in CombinedLineDb.iteritems():
            if line_n >= LineBegin and line_n < LineEnd: 
                if covered_f: coverage += 1
                line_count += 1
        if line_count == 0: return 1.0
        else:               return float(coverage) / float(line_count)

    @staticmethod
    def get_branch_coverage(CombinedBranchDb, LineBegin, LineEnd, TotalF):
        """Determines average branch coverage determined from the given
        database. Only those blocks are considered which lie in between 
        'LineBegin' and 'LineEnd'.
                    
        RETURNS: -- Average branch coverage.
                 -- None, if there is no branch in that range.

        In case of 'Total', the branch coverage is '1' if there is no branch 
        at all.
        """
        coverage     = 0
        branch_count = 0
        for branch_id, covered_f in CombinedBranchDb.iteritems():
            line_n = branch_id[0]
            if line_n >= LineBegin and line_n < LineEnd: 
                if covered_f: coverage += 1
                branch_count  += 1

        if branch_count == 0: return 1.0 if TotalF else None
        else:                 return float(coverage) / float(branch_count)

    def __repr__(self):
        return "{ line: %s; branch: %s; }" % (self.line, self.branch)

class CoverageDB_Entry:
    """Contains the coverage information about a single file which as been
    collected during parsing. The constructor of this class post-processes the
    parsed data.
    """
    __slots__ = ("file_name", 
                 "sub_coverage_db", 
                 "branch_cov_db", "branch_cov_db")

    def __init__(self, FileInfo):
        self.file_name                   = FileInfo.file_name
        self.__file_info_list            = [ FileInfo ]
        self.total                       = None
        self.test_id_list_by_function_db = defaultdict(list)
        self.test_list_by_function_db    = defaultdict(list)
        self.sub_coverage_db             = {}

    def merge(self, FileInfo):
        """Merge the data from 'FileInfo' with the data that is currently 
        present.
        """
        assert self.file_name == FileInfo.file_name
        self.__file_info_list.append(FileInfo)

    def get_test_list_by_function_db(self, TestIdDb):
        if TestIdDb is not None:
            def adapt(TestId):
                if not TestId: return None
                else:          return TestIdDb.get(TestId)
        else:
            def adapt(TestId): 
                return "%s" % TestId

        result = defaultdict(list)
        for file_info in self.__file_info_list:
            for line_begin, line_end, function_name in file_info.function_iterable():
                coverage = Coverage.from_databases(file_info.line_db, 
                                                   file_info.branch_db, 
                                                   line_begin, line_end)
                if coverage.line == 0: continue

                result[function_name].append((adapt(file_info.test_id), coverage))

        return result

    @staticmethod
    def is_admissible_line(IntervalList, LineN):
        for begin, end in IntervalList:
            if   LineN < begin: continue
            elif LineN < end:   return True
        return True
        
    def merge_line_db_list(self):
        """Merge the line databases from the FileInfo-s in FileInfoList.
        """
        line_db = {}
        for file_info in self.__file_info_list:
            for line_n, covered_f in file_info.line_db.iteritems():
                prev_covered_f = line_db.get(line_n)
                if prev_covered_f is None or prev_covered_f == False:
                    line_db[line_n] = covered_f
        return line_db

    def merge_branch_db_list(self):
        """Merge the branch databases from the FileInfo-s in FileInfoList.
        """
        branch_db = {}
        for file_info in self.__file_info_list:
            for branch_id, covered_f in file_info.branch_db.iteritems():
                prev_covered_f = branch_db.get(branch_id)
                if prev_covered_f is None or prev_covered_f == False:
                    branch_db[branch_id] = covered_f
        return branch_db

    def finalize(self, TestIdDb):
        """Derives the following data from the collected information:

                TestIdDb: test id --> (application name, choice name)

        .sub_coverage_db: A database that maps from function name to 'Coverage'.
        .total:           A 'Coverage' object that includes all admissible 
                          functions.
        .test_list_by_function_db: A map from function name to list of
                                   associated tests.
        """
        # (*) Extract line and branch coverage databases for all admissible 
        #     functions.
        line_db   = self.merge_line_db_list() 
        branch_db = self.merge_branch_db_list() 

        # (*) Each 'FileInfo' object should contain all functions. So one object is 
        #     enough to iterate over all.
        self.sub_coverage_db = dict(
            (name, Coverage.from_databases(line_db, branch_db, line_begin, line_end))
            for line_begin, line_end, name in self.function_iterable()
        )

        # (*) Collect all coverage over all lines of the file
        #
        self.total = Coverage.from_databases(line_db, branch_db, 0, 1e37, TotalF=True)

        # (*) Collect for each function the test application names and choice names 
        #     which cause some coverage.
        self.test_list_by_function_db = self.get_test_list_by_function_db(TestIdDb)

    def function_iterable(self):
        """Iterate over all covered functions of the file which is represented
        by this object. Functions appear uniquely.
    
        YIELDS: line_begin, line_end, function_name
    
        for every function that is at least once considered to be admissible for
        consideration.
        """
        done_set = set()
        for file_info in self.__file_info_list:
            for line_begin, line_end, name in file_info.function_iterable():
                if name in done_set: continue
                yield line_begin, line_end, name
                done_set.add(name)

    def __str__(self):
        return "".join([
            "file:            %s\n" % path.relative(self.file_name), 
            "total:           %s\n" % self.total,
            "sub_coverage_db: %s\n" % self.sub_coverage_db,
            "test_id_list_by_function_db: %s\n" % dict(self.test_list_by_function_db),
        ])

class CoverageDB(dict):
    def iterable_rows(self):
        def count(Entry, Name):
            test_list = Entry.test_list_by_function_db.get(Name) 
            if test_list is None: return 0, 0
            ok_n   = 0
            fail_n = 0
            for test, coverage in test_list:
                if test is None:                    continue
            return ok_n, fail_n 

        def collect(test_db, Entry, Name):
            """Collect tests that test the function 'Name'. Using a dictionary
            avoids double mentioning of same tests. 
            """
            test_list = Entry.test_list_by_function_db.get(Name) 
            if test_list is None: return

            for test, dummy in test_list:
                if test is None: continue
                key          = (test.description.file_name(), test.choice())
                test_db[key] = test
            
        def get_info(entry):
            line_cov   = 0
            branch_cov = 0
            n          = 0
            test_db    = {}
            for function_name, coverage in sorted(entry.sub_coverage_db.iteritems(), 
                                                  key=itemgetter(0)):
                if coverage.branch is None:
                     if coverage.line != 0: branch_cov += 1.0
                else:                                              
                    branch_cov += coverage.branch
                line_cov += coverage.line
                n        += 1

                collect(test_db, entry, function_name)

            if n != 0:
                line_cov   = line_cov   * 100.0 / n
                branch_cov = branch_cov * 100.0 / n
                # At least report 1% to say it is not zero
                if branch_cov < 1.0 and branch_cov > 0: branch_cov = 1.0
            else:
                branch_cov = 100.0

            ok_n   = 0
            fail_n = 0
            for test in test_db.itervalues():
                if test.result().verdict == "OK": ok_n   += 1
                else:                             fail_n += 1
            
            return line_cov, branch_cov, ok_n, fail_n

        yield "file-name", "line coverage[%]", "branch coverage [%]", "ok", "fail"

        for file_name, entry in sorted(self.iteritems(), key=itemgetter(0)):
            line_cov, branch_cov, ok_n, fail_n = get_info(entry)
            file_name = path.relative_to_home_pretty(file_name)
            yield file_name, "%i" % line_cov, "%i" % branch_cov, "%i" % ok_n, "%i" % fail_n
    

