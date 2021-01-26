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
import fnmatch

class TestSelector:
    """Selector object to distinguish between tests which are considered and
    those which are skipped. The selection process works as follows:

        (1) If .reference_table is None: consider all tests--apriori.
            Else:                        consider tests in reference table.
        (2) Use directory pattern to filter remaining tests.
        (3) Use application file pattern to filter remaining tests.
        (4) Use choice pattern to filter remaining tests.
        (5) Use additional attributes of the tests to filter remaining tests.
            (Example, 'make_failed_only_f', 'good_only_f', ...)

    The filter scheme is applied stepwise:

        .admissible_directories()  --> delivers directories to be considered.
        .admissible_applications() --> delivers applications ... 
    """
    def __init__(self, ReferenceTable, DirName, AppName, Choice, 
                 FailedOnlyF, MakeFailedOnlyF, GoodOnlyF):
        self._reference_table    = ReferenceTable
        self._dir_pattern        = DirName
        self._app_pattern        = AppName
        self._choice_pattern     = Choice
        self._failed_only_f      = FailedOnlyF
        self._make_failed_only_f = MakeFailedOnlyF
        self._good_only_f        = GoodOnlyF

    @property
    def app_pattern(self): return self._app_pattern
    @property
    def choice_pattern(self): return self._choice_pattern
    @property
    def dir_pattern(self): return self._dir_pattern
    @property
    def failed_only_f(self): return self._failed_only_f
    @property
    def make_failed_only_f(self): return self._make_failed_only_f
    @property
    def good_only_f(self): return self._good_only_f

    def admissible_directories(self, DirNameList):
        return TestSelector._matching_list(self._dir_pattern, DirNameList)

    def admissible_applications(self, AppNameList):
        return TestSelector._matching_list(self._app_pattern, AppNameList)
    
    def is_admissible(self, Result):
        Choice      = Result.choice
        LastVerdict = Result.verdict
        assert Choice is not None

        if     self._choice_pattern \
           and not fnmatch.fnmatch(Choice, self._choice_pattern): 
            return False
        elif self._make_failed_only_f: return LastVerdict == "MAKE FAILED"
        elif self._good_only_f:        return LastVerdict == "OK"
        elif self._failed_only_f:      return LastVerdict != "OK"
        else:                          return True

    @staticmethod
    def _matching_list(Pattern, NameList):
        if not Pattern:
            return NameList
        else:
            return [
                name for name in NameList if fnmatch.fnmatch(name, Pattern)
            ]


