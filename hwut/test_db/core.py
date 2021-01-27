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
"""hwut_info.dat --> all available test applications.
   ADM/cache.fly --> cache with informations about test applications.
"""

import hwut.test_db.hwut_info_interview  as     interview
import hwut.auxiliary.file_system        as     fs
from   hwut.test_db.description          import TestDescription, E_Hist
import hwut.common                       as     common

import os
import sys
import stat
import fnmatch
from   copy import deepcopy


class TestDB:
    """Map:

             test application name --> TestDescription

    The test description describes how to perform the test what the choices are, etc.
    Based on the TestDescription objects of TestExecutionInfo can be constructed that
    tell how tests need to be executed.
    """
    def __init__(self, Password):
        """The constructor is only to be called from 'from_cache()'
        """
        assert Password == "caller: from_cache()"

        self.__db            = {}   # map: test application name --> TestDescription
        self.__referred_date = ""

        self.__db_dir        = None # DEBUG: Detect mismatching read/store locations.

    @classmethod
    def from_cache(cls):
        result = cls(Password="caller: from_cache()")
        result.read()
        return result

    def register(self, AppNameSet):
        """Based on the consideration of 'hwut-info.dat' and the current directory,
        a list of applications has been derived. The apps mentioned in AppNameSet
        are ALL available applications. 

            -- App from AppNameSet not yet in database => add.
            -- App from database not in AppNameSet     => delete.

        The deletion and addition of applications is reported in a 'history' object.

        Changes in the TestDescription are NOT reported in the 'history'.
        """
        history = []
        for key in self.__db.keys(): 
            if key not in AppNameSet: 
                history.append((E_Hist.APP_DELETED, key))
                del self.__db[key]

        for key in AppNameSet: 
            if key not in self.__db: 
                history.append((E_Hist.APP_NEW, key))
                self.__db[key] = TestDescription(key)

        return history

    def register_entry(self, AppName, NewDescr):
        """Registers the new TestDescription for the given AppName. Any change
        is reported in a 'history' object. 
        
        RETURNS: 'history', i.e. a list of history items which report change.
        """
        assert AppName != "#none#"
        descr = self.__db.get(AppName)

        if descr is None: 
            self.__db[AppName] = NewDescr
            return []

        history = self.__db[AppName].absorb_TestDescription(NewDescr)

        return history
        
    def update(self, Strategy, TeiDb):
        """Strategy -- strategy to be applied on directories and files.
           TeiDb    -- map: test application name --> TestExecutionInfo
        """
        if Strategy.is_only_database_query() or Strategy.handle_only_failed_experiments():
            return

        missing_set = set()
        self.register(set(TeiDb.db.iterkeys()))

        # Make sure, that all required test applications are present
        for name, tei in TeiDb.admissible_iteritems(): 
            if not self.setup_test_application(name, tei):
                missing_set.add(name)

        # Update the test descriptions
        for name, tei in TeiDb.admissible_iteritems(): 
            if name in missing_set: continue
            new_descr = interview.do(name, tei.interpreter_sequence,
                                     self.get_last_interview_time(name))
            if new_descr is None: continue
            
            new_descr.absorb_TextExecutionInfo(tei)

            self.register_entry(name, new_descr)

        return

    def get_last_interview_time(self, AppName):
        """RETURNS: Time -- last time when the application was interviewed with
                            '--hwut-info'.
                    None -- if it has never been interviewed.
         
        It is assumed that an entry for the test application already exists!
        """
        descr = self.__db.get(AppName)
        if descr is None: 
            return -1
        return descr.hwut_info_request_system_time()

    def get(self, AppName):
        return self.__db.get(AppName)

    def write(self):
        """Writes all existing information about files into a database."""
        # __db_dir = Directory where the current database has been read. If this
        #            changed, then there is a major problem!
        assert self.__db_dir == os.getcwd()

        fh = fs.open_or_None(common.HWUT_DATABASE_FILE, "wb")
        if fh is None:
            print "Error: Cannot write '%s'" % common.HWUT_DATABASE_FILE
            return

        for file_name, entry in sorted(self.__db.iteritems(), 
                                       key=lambda x: (x[1].group(), x[1].title())):
            fh.write("{\n")
            entry.fly_write(fh)
            fh.write("}\n")

        fh.close()

    def read(self):
        if self.__db_dir == os.getcwd(): 
            return

        self.__db.clear()

        # Store directory where the dabase is supposed to be read.
        # (It is not a problem, if the database reading fails. The
        #  important thing is that we stick with the same directory.)
        self.__db_dir = os.getcwd()

        fh = fs.open_or_None(common.HWUT_DATABASE_FILE, "rb")
        if fh is None: return

        while 1 + 1 == 2:
            descr = TestDescription.from_fly(fh)
            if descr is None: break
            self.register_entry(descr.file_name(), descr)
            
    def referred_date(self):
        return self.__referred_date

    def get_test_sequence(self, TeiDb):
        sequence      = []
        skipped_tests = []

        def sort_key(Pair):
            """Sort by: (1) Group 
                        (2) Title 
                        (3) Application Name
            """
            dummy, D = Pair
            return (D.group(), D.title(), D.file_name())

        def iterable():
            for name in TeiDb.selector_test.admissible_applications(TeiDb.db.iterkeys()):
                description = self.__db.get(name)
                if description is None: continue
                yield name, description

        for name, description in sorted(iterable(), key=sort_key):
            sub_sequence, \
            sub_skipped   = description.get_Test_list(TeiDb.selector_test)
            skipped_tests.extend(sub_skipped)

            if not sub_sequence: continue
            # Sort by 'choice'
            sub_sequence.sort(key=lambda t: t.result().choice)
            sub_sequence[0].set_first_f()
            sub_sequence[-1].set_last_f()
            sequence.extend(sub_sequence)

        for i, test in enumerate(sequence):
            test.set_execution_sequence_index(i)

        return sequence, skipped_tests

    def setup_test_application(self, AppName, Tei):
        """RETURNS: True  -- if the executable has been made accessible.
                    False -- if it was not possible to make an executable with the 
                             given name.

        Writes a warning, if it is not possible to generate executable.
        """
        # (*) If App requires to be made, make it.
        if Tei.make_f:
            if not self.__db[AppName].make():
                # Following is reported by 'MAKE FAILED'. No extra msg necessary.
                # print "Warning: '%s' cannot be built." % AppName
                return False

        # (*) Check whether file is present
        if not os.access(AppName, os.F_OK):
            print "Warning: '%s' not found." % AppName
            return False

        # (*) Check whether executable rights are in place
        elif not os.access(AppName, os.X_OK | os.R_OK):
            # Try to make it executable and readable
            try:   os.chmod(AppName, stat.S_IREAD | stat.S_IEXEC)
            except: pass
            if not os.access(AppName, os.X_OK | os.R_OK):
                print "Warning: '%s' cannot be made executable." % AppName
                return False

        # (*) Oll Korrekt.
        return True



