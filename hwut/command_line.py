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
import os
import sys

import hwut.io.messages        as     io
from   hwut.auxiliary.GetPot   import GetPot
import hwut.auxiliary.path     as     path
from   hwut.common             import Setup, \
                                      get_next_nominus
#                                    
import hwut.help                                  as help
import hwut.common                                as common
import hwut.core                                  as core
import hwut.sos.c.core                            as sos
import hwut.sos.c.lazy.core                       as sols
import hwut.temporal_logic.engine                 as logic
import hwut.code_generation.function_stubs.c.core as stub_c
import hwut.code_generation.generator.core        as generator
#
from   hwut.strategies.accept                import AcceptStrategy
from   hwut.strategies.accept_incremental    import AcceptIcrementalStrategy
from   hwut.strategies.clean                 import CleanStrategy
from   hwut.strategies.logic_display         import LogicDisplayStrategy
from   hwut.strategies.difference            import DifferenceDisplayStrategy
from   hwut.strategies.info                  import InfoStrategy
from   hwut.strategies.time_info             import TimeInfoStrategy
from   hwut.strategies.test                  import TestExecutionStrategy
from   hwut.strategies.run                   import RunStrategy
from   hwut.strategies.individual_run        import IndividualRunStrategy
from   hwut.strategies.gcov                  import GcovStrategy
# TODO: from hwut.strategies.zip        import ZipStrategy

def first_three_no_minus_arguments(Argv):
    """Extract the first three no-minus arguments and derive the command, the
    application pattern and the choice pattern.

    RETURNS: [0] Command
             [1] Application Pattern
             [2] Choice Pattern
             [3] Remaining Command Line Options 
    """
    L = len(Argv)

    command             = "test"
    pattern_application = None  # any application
    pattern_choice      = None  # any choice

    # Take the first (at max 3) no-minus arguments
    first  = None
    second = None
    third  = None
    i = 1
    while 1 + 1 == 2:
        if L <= i or (Argv[i] and Argv[i][0] == "-"): break 
        first  = Argv[i]; i += 1;
        if L <= i or (Argv[i] and Argv[i][0] == "-"): break 
        second = Argv[i]; i += 1;
        if L <= i or (Argv[i] and Argv[i][0] == "-"): break 
        third  = Argv[i]; i += 1;
        break
    remainder = Argv[i:]

    command = command_db_get_by_name(first)

    if command is None:
        command = command_db["test"]
        # In case that the left-out command defaults to 'test' the third
        # no-minus is put back to the remainder.
        if third is not None: remainder.insert(0, third) 
        third   = second
        second  = first

    return command, second, third, remainder

def execute_test(Setup):
    core.run(Setup, TestExecutionStrategy(Setup))

def generate_test_makefile(Setup):
    sos.do(Setup)

def generate_test_initialization_helper(Setup):
    sos.do_initialization_help(Setup)

def generate_test_environment(Setup):
    sols.do(Setup)

def accept(Setup):
    core.run(Setup, AcceptStrategy(Setup))

def accept_incremental(Setup):
    core.run(Setup, AcceptIcrementalStrategy(Setup))

def difference(Setup):
    core.run(Setup, DifferenceDisplayStrategy(Setup))

def logic_display(Setup):
    core.run(Setup, LogicDisplayStrategy(Setup))

def gcov(Setup):
    core.run(Setup, GcovStrategy(Setup))

def make(Setup):
    #   ARGV[0] ARGV[1] AGRV[2]      ARGV[3]
    # > hwut    make    some-target  ...
    #
    # where 'some-target' enters the argument list as any other.
    argument_list = [ x for x in sys.argv[2:] if x != "--no-color" ]

    core.run(Setup, 
             RunStrategy(Setup, common.MAKE_APPLICATION, 
                         ArgumentList=argument_list))

def run(Setup):
    application = Setup.test_application_name
    #   ARGV[0] ARGV[1] AGRV[2]       ARGV[3]
    # > hwut    run     something.sh  ...
    argument_list = [ x for x in sys.argv[3:] if x != "--no-color" ]

    core.run(Setup, 
             RunStrategy(Setup, application, 
                         ArgumentList=argument_list))

def show_futile(Setup):
    core.run(Setup, CleanStrategy(Setup))

def info(Setup):
    core.run(Setup, InfoStrategy(Setup))

def time_info(Setup):
    core.run(Setup, TimeInfoStrategy(Setup))

def stub(Setup):
    stub_description_file = path.good_path(Setup.test_directory, 
                                           Setup.test_application_name)
    if stub_description_file is None:
        print "Error: missing input file"
        sys.exit(-1)

    if not Setup.output_file_stem:
        print "Error: for stubbing, an output filestem must be provided (use -o ...)"
        sys.exit(-1)

    stub_c.do(stub_description_file, Setup.output_file_stem)

def generator_implementation(Setup):
    generator_description_file_name = Setup.test_application_name
    generator_name                  = Setup.choice
    if generator_description_file_name is None:
        print "Error: missing input file"
        sys.exit(-1)
    generator.do(generator_description_file_name, 
                 generator_name)

def logic_rule_syntax_test(Setup):
    file_name = Setup.test_application_name
    logic.test_rule_syntax(file_name)

def logic_regular_expression_match_test(Setup):
    re_string = Setup.test_application_name
    file_name = Setup.choice
    if generator_description_file_name is None:
        print "Error: regular expression"
        sys.exit(-1)
    logic.test_regular_expression_match(re_string, file_name)

def logic_test(Setup):
    rule_file_name  = Setup.test_application_name
    event_file_name = Setup.choice
    logic.do(rule_file_name, event_file_name, 
             LogSH=sys.stdout, 
             OnlyREMatchesF=cl.search("--mo", "--match-only"))

def remote_execution_try(Setup):
    common.remote_executer = core.try_setup_remote_execution() 
    if common.remote_executer == None:
        io.formatted_output("Error:", 
           "Command line mode 'remote': The remote executer could not be setup. It lacks\n" + \
           "information in the makefile. Please, setup a 'hwut-remote' rule. Review HWUT\n" + \
           "documentation for details.")
        return

    common.remote_executer.do([file_name, choice])


def prepare():
    # -- store the directory from where HWUT was called.
    io.__home_directory = os.getcwd()

    # -- initialize the database
    common.set_interface("CONSOLE")

    for candidate in Setup.option_set_version:
        if candidate in sys.argv: get_version(None, None)

    for candidate in Setup.option_set_help:
        if candidate in sys.argv: get_help(None, None)

def get_version(Dummy0, Dummy1):
    help.print_version()
    sys.exit()
    
def get_help(Dummy0, Dummy1):
    help.do()
    sys.exit()
    

command_alias_db = {
    "i":   "info",
    "m":   "make",
    "fu":  "futile",
    "gen": "generator",
    "gc":  "gcov",
    "a":   "accept",
    #"mv":  "move",
    #"rm":  "remove",
    "t":   "test",
    "v":   "version",
    "":    "test",
}
    
command_db = {
    "accept":      accept,
    "ai":          accept_incremental,
    "dd":          difference,
    "futile":      show_futile,
    "gcov":        gcov,
    "generator":   generator_implementation,
    "help":        get_help,
    "info":        info,
    "ld":          logic_display,
    "make":        make,
    "run":         run,
    "sos":         generate_test_makefile,
    "sols":        generate_test_environment, # 'save our lazy souls'
    "sosi":        generate_test_initialization_helper, 
    "stub":        stub,
    "test":        execute_test,
    "time":        time_info,
    "try:logic":   logic_test,
    "try:regex":   logic_regular_expression_match_test,
    "try:remote":  remote_execution_try,
    "try:syntax":  logic_rule_syntax_test,
    "version":     get_version,
    #"move":        move,
    #"remove":      remove,
}

def command_db_get_by_name(Name):
    """RETURNS: Command that belongs to 'Name'.
                None, if no such command exists.
    """
    if Name in command_alias_db: Name = command_alias_db[Name]
    return command_db.get(Name)

def get_setup(Argv):
    command,              \
    first_argument,       \
    second_argument,      \
    remaining_option_list = first_three_no_minus_arguments(Argv)

    try:    
        remaining_option_list.insert(0, Argv[0])
        cl = GetPot(remaining_option_list)
    except:
        print "Error while parsing command line."
        sys.exit()

    setup = Setup(cl, first_argument, second_argument)

    if command not in (make, run):
        setup.check_unrecognized_options()

    return command, setup

