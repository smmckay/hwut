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
import hwut.auxiliary.path             as aux
import hwut.verdict.comparison    as comparison
import hwut.temporal_logic.engine as temporal_logic


def do(TestInfo, FhOutput=None):
    if TestInfo.description.temporal_logic_f(): 
        return temporal_logic(TestInfo)
    else:
        return traditional(TestInfo, FhOutput)

def traditional(TestInfo, FhOutput):
    """Performs a 'traditional' comparison. That is, the test program produced
    some output which is to be compared with a nominal output from the GOOD 
    directory.
    """
    if FhOutput is not None: fh_out = FhOutput
    else:                    fh_out = TestInfo.OUT_FileHandle()

    fh_good = TestInfo.GOOD_FileHandle()
    if fh_good is None: return "NO GOOD FILE"
   
    if comparison.do(fh_out, fh_good, TestInfo):
        return "OK"
    else:
        return "FAIL"

def temporal_logic(TestInfo):
    """Consider the provided output as elements of temporal logic. As soon as one
    rule base fails on the output, the function returns the verdict.
    """
    for rule_file in TestInfo.description.temporal_logic_rule_file_list():
        result = temporal_logic.do(rule_file, TestInfo.OUT_FileName()) 
        if result != "OK": return result
    return "OK"

    

