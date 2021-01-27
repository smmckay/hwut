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

def max_cell_widths(Table):
    """Determine for each column the maximum width of its cells.
    RETURNS: array

    where array[i] is the maximum length of a cell found in column 'i'.
    """
    result = [ 0 ] * len(Table[0])
    for record in Table:
        for i, cell in enumerate(record):
            L = len(cell)
            if result[i] < L: result[i] = L
    return result

def space(Idx, Cell, MaxCellWidths):
    """Write padding space for a given field.

        Idx:           Index of the column of the cell in the table.
        Cell:          The cell's content.
        MaxCellWidths: Array as it is returned from 'max_cell_widths'.

    RETURNS: Formatted string.
    """
    return " " * (MaxCellWidths[Idx] - len(Cell)) 

def get_row(Row, MaxCellWidths, Pad):
    return "".join(
        "%s%s%s" % (cell, space(i, cell, MaxCellWidths), Pad)
        for i, cell in enumerate(Row)
    )
    
