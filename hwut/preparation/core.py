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
"""PURPOSE: 

   (1) Determine list of test applications:

       * their file names.
       * the interpreter sequence to execute them (if required).
       * if or if not they are buildt by 'make.

   (2) Access the attributes related to each test execution file:

       * make-required? 
         --> 'make the test file'
       * data in cache older then test file 
         --> execute the test with '--hwut-info'
         --> test data.
   
   (3) Derive the test sequence.

       * for each test find the choices
       * build a list of pairs (test file, choice). Each pair represents a 
         test to be executed.
         
(C) Frank-Rene Schaefer
_______________________________________________________________________________
"""
import hwut.preparation.hwut_info as hwut_info

def do(TheFilter):
    assert False
    """Determine the test sequence, i.e. what tests need to be run with what
    options.  


             .---------------.            .----------------.
             | hwut_info.dat |            | Makefile       |
             '---------------'            | hwut-info: ... |
                    |                     '----------------'
                    |                             |
                    '------------..---------------'
                                 ||
            .----------------------------------------------.
            |            brief test list                   |
            | list of (test, interpreter-sequence, make_f) |
            '----------------------------------------------'
                                 |
                               filter 
                            on test name
                                 |             
          .--------------.       |       .--------------.   
          | test         |   2   |    1  | ADM/database |
          | application  +------>|<------| (info cache) |
          | --hwut-info  |       |       '--------------' 
          '--------------'       |
                               filter
                            on test info
                                 |
                         .---------------.
                         | test sequence |
                         '---------------'
                              
    RETURNS: A list of TestSequenceElement-s. 

    A TestSequenceElement is an isolated test run.
    """

    # brief_test_db: test file name --> (interpreter sequence, make_f)
    #
    brief_test_db = hwut_info.do()
    if brief_test_db is None:
        # Create a "hwut_info.dat" file based on test information that is taken
        # in the 'old fashion' of HWUT.
        brief_test_db = ancient_preparation.adapt_to_new_format()

    # test_list: list of Test objects 
    #
    # with information about CHOICES, SAME, etc. flags and options. 
    test_list = get_test_information(brief_test_db, TheFilter)

    # test_sequence: list of pairs (Test, Choice)
    #
    # where each pair stands for a separate test run.
    test_sequence = get_test_sequence(test_list, TheFilter)

    return test_sequence
    
class Filter:
    """Allows to setup filter conditions for tests to be considered:

        .previous_ok_f       --> only test that previously succeeded
        .choice_pattern      --> only tests where choice matches 'choice_pattern'.
                                 Patterns are matched by 'fnmatch'.
        .application_pattern --> like 'choice_pattern' for applications.
    """
    def __init__(self):
        self.__previous_ok_f       = None
        self.__application_pattern = None
        self.__choice_pattern      = None
    @property
    def previous_ok_f(self):       return self.__previous_ok_f
    @property
    def application_pattern(self): return self.__application_pattern
    @property
    def choice_pattern(self):      return self.__choice_pattern

    def accept(self, Test, Choice):
        """Check whether the 'test/choice' combination fits the requirement
        of the filter. 
    
        RETURN: True  -- if combination is ok.
                False -- if not.
        """
        if     self.__application_pattern is not None \
           and not fnmatch.fnmatch(Test.file_name, self.__application_pattern):
            return False
        elif   self.__choice_pattern is not None \
           and not fnmatch.fnmatch(Choice, self.__choice_pattern):
            return False
        elif   self.__previous_ok_f is not None \
           and not (Test.previous_ok_f == self.__previous_ok_f):
            return False
        else:
            return True

def get_test_information(BriefTestDb, TheFilter):
    """Get for every test detailed information. In order to get the test 
    information, HWUT first tries to access the database. If the content is 
    not up-to-date it interviews the file itself.

    The 'test_info_provider' delivers information for the given test name.
    It may get it from the database (cache) or from interacting with the 
    test file.

    To reduce the interaction with test applications and databases, this
    function already uses filter information on test application names
    provided by 'TheFilter'.

    RETURNS: List of 'Test' objects--one for each test file.
    """
    def get_Test(FileName, InterpreterSequence, MakeF):
        test = test_info_provider.get(FileName)
        test.configure(InterpreterSequence, MakeF)
        return test

    if TheFilter.application_pattern is None:
        return [
            get_Test(file_name, info[0], info[1])
            for file_name, info in brief_test_db.iteritems()
        ]
    else:
        return [
            get_Test(file_name, info[0], info[1])
            for file_name, info in brief_test_db.iteritems()
            if fnmatch.fnmatch(file_name, TheFilter.application_pattern)
        ]
    
def get_test_sequence(TestList, TheFilter):
    """Consider for each test its possible choices and builds list of pairs 
    (test, choice). This list describes the sequence of tests to be executed.
    Before, an element is added to the sequence it is checked whether it complies
    to the requirements in 'TheFilter'.

    RETURNS: The test sequence.
    """
    test_sequence = []
    for test in TestList:
        choice_list = test.result_list()
        if choice_list is None:
            if TheFilter.accept(test):
                test_sequence.append(TestSequenceElement(test, None))
        else:
            test_sequence.extend(
                TestSequenceElement(test, choice) 
                for choice in choice_list if TheFilter.accept(test, choice)
            )
    return test_sequence
            
    
    

    
