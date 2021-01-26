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
import hwut.auxiliary.path as aux
import hwut.auxiliary.executer  as executer
import hwut.io.messages        as io
import hwut.common    as common
#
import os
import sys

def make(MakeTarget):
    """Makes the MakeTarget. Note, that if the target is up-to-date, then actually
       nothing is to be made.
    """
    option_list = [ MakeTarget ]

    if common.MAX_CPU_NUMBER != 1: 
        option_list.append("--jobs=%s" % common.MAX_CPU_NUMBER)

    io.on_make_only_this(MakeTarget)
    executer.do([common.MAKE_APPLICATION] + option_list)

    # ONLY check if the target has been built!
    # Executable rights are checked and repaired elsewhere.
    success_f = os.access(MakeTarget, os.F_OK)

    io.on_make_only_this_end(MakeTarget, success_f)
    return success_f

def simply_this(MakeTarget):
    if MakeTarget == "": return

    JobN             = common.MAX_CPU_NUMBER
    gnu_make_job_str = "--jobs=%s" % JobN
    executer.do([common.MAKE_APPLICATION, gnu_make_job_str, MakeTarget])

def is_remake_required(FileName):
    return executer.do_stdout([common.MAKE_APPLICATION, "-q", FileName]) != 0

def is_makefile_present():
    return os.access("makefile", os.F_OK) or os.access("Makefile", os.F_OK)

def __get_target_response(Target, ErrorFunction, OptionL=[]):
    if is_makefile_present() == False: return ""

    response = executer.do_stdout([common.MAKE_APPLICATION, Target] + OptionL)
    response = response.strip() 

    if response == "" and ErrorFunction is not None: 
        ErrorFunction(os.getcwd())
    return response

def get_makeable_application_list():
    """Interacts with Makefile. Makefile shall respond with lists of test files
    which are subject to 'make-ing'. 

    RETURNS: List of test file names (without the './' at the beginning) which 
             are subject to make. That is, they should be remade, if they are
             out-of-date before the next test can be done.
    """
    response     = __get_target_response("hwut-info",
                                         io.on_makefile_does_not_contain_target_hwut_info)
    program_list = response.split()
    if program_list and program_list[0] == "make:": 
        print "Error: execution of 'make hwut-info' resulted in error."
        return []

    result = [ aux.strip_dot_slash(x) for x in program_list ]
    return [ x for x in result if len(x) != 0 ]

def OLD_get_makeable_application_list():
    program_list = __get_target_response("hwut-info",
                                         io.on_makefile_does_not_contain_target_hwut_info).split()
    result = {}
    for x in program_list:
        file_name = aux.strip_dot_slash(x)
        result[file_name] = aux.ApplicationBriefInfo(file_name, MakeF=True)
    return result

def get_gcov_relevant_source_file_list():
    program_list = __get_target_response("hwut-gcov-info",
                                         io.on_makefile_does_not_report_coverage_related_source_files).split()

    return map(aux.strip_dot_slash, program_list)

def get_gcov_object_file_directory_list():
    directory_list = __get_target_response("hwut-gcov-obj",
                                           io.on_makefile_does_not_report_coverage_related_object_directory)

    return directory_list.split()

def get_gcov_relevant_function_name_list():
    function_list = __get_target_response("hwut-gcov-funcs", None).split()

    return map(aux.strip_dot_slash, function_list)

def get_remote_information():
    """This function tries to see, if the makefile specifies a remote test environment.
       If so, it returns information about the remote spy and the remote agent.
    """
    Key   = "REMOTE"   # The remote section needs to start with 'REMOTE' in order
    #                  # to prevent a default rule from responding by accident.
    spy   = None
    agent = None
    information = __get_target_response("hwut-remote", None)
    if information == "": return None, None
    if len(information) < len(Key) or information[len(Key)] != Key: 
        io.remote_start_require_response_starting_with_key(Key)
        return None, None

    def __make_dictionary(Name, List):
        result = {}
        fields = List[0].split("=")
        if len(fields) == 1:
            result["Type"] = fields[0].strip()
        elif fields[0].strip() != "Type":
            io.remote_start_requires_the_type_as_first_argument(Name, List)
        else:
            result["Type"] = fields[1].strip()
        
        for element in List[1:]:
            fields = element.split("=")
            if len(fields) < 2: 
                io.remote_start_requires_names_for_parameter(Name, List)
            result[fields[0].strip()] = fields[1].strip()

        result["Name"] = Name
        return result
           
    for line in information.split(";"):
        idx = line.find("SPY:") 
        if idx != -1: 
            remainder = line[idx + len("SPY:"):]
            spy       = __make_dictionary("SPY:", remainder.split(","))
        idx = line.find("AGENT:") 
        if idx != -1: 
            remainder = line[idx + len("AGENT:"):]
            agent     = __make_dictionary("AGENT:", remainder.split(","))

    if spy   is None: io.remote_start_requires_definition_of_a_spy()
    if agent is None: io.remote_start_requires_definition_of_an_agent()

    return spy, agent

    
