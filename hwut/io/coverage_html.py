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
import hwut.common                  as common
import hwut.io.html                 as html
import hwut.auxiliary.file_system   as fs
import hwut.auxiliary.executer.core as executer

from   operator import itemgetter

def do(CoverageDB):
    if CoverageDB is None: return
    print "HTML output in: ./html"
    executer.do(common.get_genhtml_application() + ["hwut-lcov-all.info", "--branch-coverage", "-o", "html"])

def write_coverage_result(CoverageDB):
    if CoverageDB is None: return

    html.write(fs.open_or_die("result-coverage.html", "wb"), 
               CoverageDB.iterable_rows())

