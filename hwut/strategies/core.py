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
import hwut.auxiliary.file_system as     fs
import hwut.auxiliary.path        as     aux
import hwut.preparation.hwut_info as     hwut_info
from   hwut.test_db.result        import TestResult
from   hwut.test_db.core          import TestDB
import hwut.io.messages           as     io
import hwut.io.csv                as     csv

import time
import os

class CoreStrategy:

    def __init__(self, Setup):
        assert Setup.__class__.__name__ == "Setup"

        self.__break_up_f    = False
        self.__failed_only_f = Setup.failed_only_f
        self.setup                                 = Setup
        self._test_sequence_empty_f                = False
        self._multiple_directory_f                 = False
        self.__warn_if_no_test_application_found_f = True

        # _dir_result_list:  [directory] --> total result
        self._dir_result_list = []

        # Database of all results:
        #     list of tuples: [0] directory
        #                     [1] test application name
        #                     [2] TestResult (containing name of CHOICE)
        self._result_db = []

        self._current_dir = None
        self._missing_good_file_db = {}  # map: directory --> list of test applications
        #                                #      that do not have files in the GOOD/ directory. 
        self._test_db     = None

    def missing_good_file_list(self):
        """RETURN: List of missing good files in current directory.
        """
        result = self._missing_good_file_db.get(self._current_dir)
        if result is None: return []
        else:              return result

    def missing_good_file_list_add(self, TestInfo):
        """Add a file to the list of missing good files in the current 
        directory.
        """
        the_list = self._missing_good_file_db.get(self._current_dir)
        if the_list is None:
            the_list = []
            self._missing_good_file_db[self._current_dir] = entry
        the_list.append(TestInfo)

    def start_directory_tree(self, DirectoryList):
        self._multiple_directory_f = True
        # Derived class' handler for start directory tree 
        self._start_directory_tree(DirectoryList)

    def execution_name(self):
        return None

    def start_directory(self, Dir, TestSelector):
        """RETURNS: Test sequence for the current directory determined by 
                                  the 'TestSelector'.
                    []            if there is no test sequence in the 
                                  current directory.
                    None          If the current directory is not relevant for 
                                  HWUT.
        """
        self._current_dir = Dir

        #
        # Find all tests that are relevant in this directory
        #
        tei_db = hwut_info.get_TestExecutionInfoDb(TestSelector)
        if tei_db is None: return None
        self._test_db = TestDB.from_cache()

        io.on_directory_enter(self._current_dir, tei_db.title, 
                              self.get_referred_date(), 
                              self.execution_name())

        self._missing_good_file_db[self._current_dir] = [] 

        test_sequence,    \
        skipped_test_list = self.get_test_sequence(tei_db) 

        self.register_skipped_tests(skipped_test_list)

        if   not test_sequence:                 self.set_test_sequence_empty_f()
        elif not self.is_only_database_query(): fs.ensure_directory_structure()

        # Derived class' handler for start directory
        self._start_directory(test_sequence)

        return test_sequence

    def end_directory(self):
        if not self.is_only_database_query() and self._test_db is not None:
            self._test_db.write()
        self._test_db = None

        # Derived class' handler for end directory
        return self._end_directory()

    def end_directory_tree(self):
        dirs_with_missing_good_files = [
            directory
            for directory, test_list in self._missing_good_file_db.iteritems()
            if test_list
        ]
        io.print_missing_good_files(self._missing_good_file_db)
        if self._dir_result_list or self.warn_if_no_test_application_found():
            io.print_summary(self._dir_result_list, dirs_with_missing_good_files)

        csv.write_result_db(self._result_db, 
                            self.setup.test_reference_table_file_out)

        # Derived class' handler for end directory tree
        self._end_directory_tree()

    # Default implementations of what should be implemented in derived classes:
    def _start_directory_tree(self, DirList): pass
    def _start_directory(self, TestSequence): pass
    def _end_directory(self):                 return None # default: no result
    def _end_directory_tree(self):            pass
    #__________________________________________________________________________

    def get_test_sequence(self, TeiDb):
        """TeiDb    -- TestExecutionInfoDB
        """
        self.coverage_selector = TeiDb.selector_coverage

        # (*) Update the database on new content
        self._test_db.update(self, TeiDb)

        # (*) Derive the sequence of Test objects
        test_sequence,    \
        skipped_test_list = self._test_db.get_test_sequence(TeiDb)

        # (*) Error handling, in case that there is no test sequence
        if not test_sequence \
           and not self.handle_only_failed_experiments() \
           and self.warn_if_no_test_application_found():
            io.on_no_test_application_found(TeiDb.selector_test, os.getcwd())

        return test_sequence, skipped_test_list

    def do(self, element):
        print "Strategy::do(element) not implemented"
        sys.exit(0)

    def register_skipped_tests(self, SkippedTestList):
        def iterable(TestList):
            for test_info in TestList:
                for result in test_info.description.result_list():
                    yield test_info.description, result.choice

        for description, choice in iterable(SkippedTestList):
            self._result_db.append(
                (self._current_dir, description, TestResult(choice, "SKIP", None, 0))
            )

    def warn_if_no_test_application_found(self):
        return self.__warn_if_no_test_application_found_f

    def set_warn_if_no_test_application_found(self, Value):
        self.__warn_if_no_test_application_found_f = Value
       
    def break_up_requested(self):
        return self.__break_up_f

    def set_break_up_request(self):
        self.__break_up_f = True

    def handle_only_failed_experiments(self):
        return self.__failed_only_f

    def xml_database_write_permission(self):
        return True

    def is_only_database_query(self):
        return False

    def get_referred_date(self):
        return time.strftime("%Yy%mm%dd %Hh%M")

    def set_test_sequence_empty_f(self):
        self._test_sequence_empty_f = True

class NullStrategy(CoreStrategy):
    def __init__(self, Setup):
        pass

    def do(self, element):
        pass

    def break_up_requested(self):
        return False

    def handle_only_failed_experiments(self):
        return False

    def xml_database_write_permission(self):
        return True

    def is_only_database_query(self):
        return False

    def get_referred_date(self):
        return time.asctime()

