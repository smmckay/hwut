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
import hwut.io.messages           as io
import hwut.common                as common
import hwut.auxiliary.make        as make
import hwut.auxiliary.path        as aux
import hwut.auxiliary.file_system as fs
#
from   hwut.test_db.selector import TestSelector
from   hwut.strategies.core  import NullStrategy
from   hwut.strategies.test  import TestExecutionStrategy
#
import os
import sys


def run(setup, Strategy):
    """Runs a 'Strategy' starting from he current directory. After all is done
    this function lets the process return to the directory where it started.

    EXITS 0 -- i.e. with success.
    """
    common.call_directory = os.getcwd()

    selector = TestSelector(setup.test_reference_table, 
                            setup.test_directory_pattern, 
                            setup.test_application_name, 
                            setup.choice, 
                            setup.failed_only_f,
                            setup.make_failed_only_f,
                            setup.good_only_f)

    handle_directory_tree(Strategy, selector)

    common.change_directory(common.call_directory)
    sys.exit(0)

def handle_directory_tree(Strategy, Selector):
    """Determine all TEST related directories and apply the 'Strategy'.
       -- Find all TEST directories. 
       -- call 'handle_directory()' for each directory found. 
    """

    # (*) Get list of TEST sub directories.
    directory_list = fs.get_TEST_directories()
    if not directory_list:
        io.no_hwut_related_directories_found()
        return

    # (*) Sort the directories under concern nicely
    directory_list.sort(key=__directory_sort_key)

    origin_dir = os.getcwd()
    common.set_home_directory(origin_dir)

    # (*) Iterate over TEST directories.
    Strategy.start_directory_tree(directory_list)
    for directory in Selector.admissible_directories(directory_list):
        handle_directory(directory, Strategy, Selector)

    common.set_home_directory(origin_dir)
    Strategy.end_directory_tree()

def handle_directory(Directory, Strategy, Selector):
    """Execute a Strategy in the current directory on the given TestSequence.

       -- initialize testing in this directory
       -- execute all 'tests' in this directory with the given Strategy.
       -- finalize testing in this directory.
    
    RETURNS: -- Whatsoever 'Strategy' returns from '.end_directory()'
             -- None, if there is no test that has been done.
    """
    def iterable(TestSequence):
        """YIELDS: [0] Boolean  -- True, if a new group started, False else.
                   [1] TestInfo 
        """
        prev_group = None
        for test in TestSequence:
            if Strategy.break_up_requested(): break
            group = test.description.group()
            yield prev_group != group, test 
            prev_group = group

    backup_dir = common.change_directory(Directory)

    # (*) Initialize testing in the current directory
    result        = None
    test_sequence = Strategy.start_directory(Directory, Selector) 
    if test_sequence is not None: 
        # (*) Execute the test sequence
        for new_group_f, test in iterable(test_sequence):
            if new_group_f: io.on_test_group_start(test)
            io.on_test_start(test)
            Strategy.do(test) 

        # (*) Terminate testing in the current directory
        result = Strategy.end_directory()
    
    common.change_directory(backup_dir)
    return result

def __directory_sort_key(Dir):
    """Comparator for sorting directories in a way so that it is visually
    appealing. That is, directories with the same starting directories appear
    one after the other. Smaller paths come before longer paths. With this 
    setup, printed directories look very much like 'trees'.
    """
    path_list = aux.split_path(Dir)
    return len(path_list), path_list

