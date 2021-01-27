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
import os
import hwut.auxiliary.path        as aux
import hwut.auxiliary.file_system as fs
import hwut.auxiliary.executer.core    as executer
import hwut.auxiliary.make        as make
import hwut.io.messages           as io
import hwut.common                as common

from hwut.strategies.core import CoreStrategy

class SourceFileCoverageInfo:
    def __init__(self, Name):
        self.name          = Name
        self.line_coverage = 0.0
        self.line_n        = 0
        self.branch_coverage = 0.0
        self.branch_n        = 0
        self.function_call_coverage = 0.0
        self.function_call_n        = 0
        self.occurence_n     = 1
        
    def __repr__(self):
        return "".join(["SourceFileCoverageInfo:  \n",
                        "   .name                   = %s\n" % self.name,
                        "   .line_coverage          = %f\n" % self.line_coverage,
                        "   .line_n                 = %f\n" % self.line_n       ,
                        "   .branch_coverage        = %f\n" % self.branch_coverage,
                        "   .branch_n               = %f\n" % self.branch_n       ,
                        "   .function_call_coverage = %f\n" % self.function_call_coverage,
                        "   .function_call_n        = %f\n" % self.function_call_n 
                        ])
        
class GcovStrategy(CoreStrategy):
    def __init__(self, Setup):
        CoreStrategy.__init__(self, Setup)
        self.report = []

    def _start_directory_tree(self, DirectoryList):
        self.__main = {}
        self.avrg_coverage = 0.0
        self.sum_line_n    = 0

    def _start_directory(self, TestSequence):
        self.set_break_up_request() # prevent a call to '.do()' for each test element

        # (0) If anything breaks, then coverage is 0.0 (we cannot tell what it actually is)
        self.avrg_coverage          = 0.0
        self.sum_line_n             = 0.0
        self.missing_gcda_file_list = [] 
        self.missing_gcno_file_list = []
        self.no_result_file_list    = []

        # (1) get relevant source files from the makefile
        source_file_list = make.get_gcov_relevant_source_file_list()
        if source_file_list == []: return

        # (2) get relevant functions
        #     (if no functions are specified, all functions are considered)
        relevant_function_name_list = make.get_gcov_relevant_function_name_list()

        all_files_exist_f = True
        for file_name in source_file_list:
            # If a file is given without a specific path, then we are more tolerant.
            # Gcov may be able to locate it.
            if aux.strip_dot_slash(file_name) == os.path.basename(file_name): continue
            # If the file has a specific directory to be located, then require that it is
            # really at that particular place.
            elif not fs.ensure_existence(file_name, 
                                         "File $$NAME$$ reported as result of 'make hwut-gcov-info', but does not exist."):
                all_files_exist_f = False

        if not all_files_exist_f:
            return

        # (2) call 'gcov' for each related source file
        #     -bp    get detailed information about coverages
        #     -f     get the information per function
        object_dir_list = make.get_gcov_object_file_directory_list()
        object_dir_list = map(lambda x: os.path.normpath(x.strip()), object_dir_list)
        for object_dir in object_dir_list:
            if not fs.ensure_existence(object_dir, 
                                       "Directory $$NAME$$ reported as result of 'make hwut-gcov-info', but does not exist.",
                                       DirectoryF=True): 
                return 

        all_entry_db = {}
        file_list    = []
        for source_file in source_file_list:
            source_file = os.path.normpath(source_file)

            object_dir = self.get_gcov_directory_for_source_file(source_file, object_dir_list)
            if object_dir is None: continue
            
            if object_dir.strip() != "": object_dir_spec = ["-o", object_dir]
            else:                        object_dir_spec = []
            
            result = execute.do(common.GCOV_APPLICATION, 
                                ["-bp", "-f", source_file] + object_dir_spec, 
                                ReturnResultF=True) 

            entry_list, file_info = analyze_gcov_output(result, source_file)

            if file_info is None: 
                self.no_result_file_list.append(source_file)
                continue

            # -- Only add functions that we are concerned with
            # -- It is conceivable that one C file is compiled into different object
            #    files for different compile options. In this case, count the 
            #    maximum coverage of each function.
            for function, entry in entry_list:
                ref = all_entry_db.get(function)
                if ref is None:                               
                    all_entry_db[function] = entry
                else:
                    if ref.line_coverage < entry.line_coverage: 
                        all_entry_db[function] = entry
                    all_entry_db[function].occurence_n += 1
            
            file_list.append(file_info)

        # (3a) show files 
        file_list.sort(lambda a, b: cmp(a.line_coverage, b.line_coverage))
        io.display_file_coverage_results(file_list)

        # (3b) show functions 
        all_entry_list = all_entry_db.items()
        all_entry_list.sort(lambda a, b: cmp(a[1].line_coverage, b[1].line_coverage))
        io.display_function_coverage_results(all_entry_list, relevant_function_name_list)

        # (4) compute the average coverage
        sum        = 0.0
        sum_line_n = 0.0  # better float for later division
        for function_name, entry in all_entry_db.iteritems():
            if relevant_function_name_list == [] or \
               function_name in relevant_function_name_list:
                sum += (entry.line_coverage * entry.line_n)
                sum_line_n   += entry.line_n

        if sum_line_n != 0: self.avrg_coverage = sum / sum_line_n * 100.0
        else:               self.avrg_coverage = 0
        self.sum_line_n = sum_line_n

    def do(self, Element):
        # self.set_break_up_requested() should have prevented a call to this function!
        assert False, \
               "GcovStrategy::do() is not to be called for each test element!"

    def _end_directory(self):
        io.print_coverage(self.avrg_coverage)

        if    self.missing_gcno_file_list != [] \
           or self.missing_gcda_file_list != [] \
           or self.no_result_file_list    != []:
            io.on_gcov_missing_files(  self.missing_gcno_file_list \
                                     + self.missing_gcda_file_list \
                                     + self.no_result_file_list)

        self.report.append([os.getcwd(), self.avrg_coverage, self.sum_line_n])

    def _end_directory_tree(self):
        io.report_coverage_summary(self.report)

    def is_only_database_query(self):
        return True

    def get_gcov_directory_for_source_file(self, SourceFileName, ObjDirList):
        result = None

        base_name = os.path.basename(SourceFileName)

        file_stem = os.path.splitext(base_name)[0]
        gcno_file = file_stem + ".gcno"
        gcda_file = file_stem + ".gcda"

        gcno_ok_f = False
        gcda_ok_f = False
        for object_dir in ObjDirList:
            ok_n = 0

            file_name = os.path.normpath(object_dir + "/" + gcno_file)
            if aux.ensure_existence(file_name, ""): gcno_ok_f = True; ok_n += 1

            file_name = os.path.normpath(object_dir + "/" + gcda_file)
            if aux.ensure_existence(file_name, ""): gcda_ok_f = True; ok_n += 1 

            if ok_n == 2:
                result = object_dir
                break
            
        if not gcno_ok_f: self.missing_gcno_file_list.append(gcno_file)
        if not gcda_ok_f: self.missing_gcda_file_list.append(gcda_file)

        return result ## self.missing_gcda_file_list == [] and self.missing_gcno_file_list == []

def analyze_gcov_output(GCovOutput, FileName):
    def __extract(Info):
        """Extracts two numbers from a string of the form '82% of 23'"""
        first, second = Info.split("of")
        first  = first.strip()
        first  = float(first[:-1]) / 100.0
        second = int(second.strip())
        return first, second

    if GCovOutput.strip() == "":
        return None, None

    tmp = None
    entry_list = []
    file_info  = None
    for line in GCovOutput.splitlines():
        if line.find("Function") == 0:
            function_name = line.split()[1][1:-1]
            tmp = SourceFileCoverageInfo(function_name)
            entry_list.append([function_name, tmp])

        elif line.find("File") == 0:
            file_name = line.split()[1][1:-1]
            file_name = os.path.normpath(file_name)
            file_info = SourceFileCoverageInfo(file_name)
            tmp = file_info

        elif line.find("Lines executed") == 0:
            info = __extract(line.split(":")[1])
            tmp.line_coverage = info[0]
            tmp.line_n        = info[1]

        elif line.find("Branches executed") == 0:
            info = __extract(line.split(":")[1])
            tmp.branches_coverage = info[0]
            tmp.branches_n        = info[1]

        elif line.find("Calls executed") == 0:
            info = __extract(line.split(":")[1])
            tmp.function_call_coverage = info[0]
            tmp.function_call_n        = info[1]

    return entry_list, file_info

