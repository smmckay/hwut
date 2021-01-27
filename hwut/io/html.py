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

def colorize_fg_default(I, K, Record):
    if K >= 3 and len(Record) > 3:
        if Record[4] != "0":
            if   K == 4:  return "#FF1010"  # RED
            elif K == 3: 
                if I % 2: return "#C0FFC0"  # DARK GREEN
                else:     return "#E0FFE0"  # LIGHT GREEN
        else:
            if K == 3:    return "#10FF10"  # BRIGHT GREEN

    if I % 2: return "#E8E8E8"              # GREY
    else:     return "#FFFFFF"              # WHITE

def colorize_bg_default(I, K, Record):
    return "#000000"
            
def write(fh, Table, colorize_bg=colorize_bg_default, colorize_fg=colorize_fg_default):
    """Write the given table to a file in 'HTML' format. 
    """

    adapted_table = [ 
        tuple(field for field in record)
        for record in Table
    ]

    if len(adapted_table) < 1: return
    first_record = adapted_table[0]
    
        
    fh.write("<style>\n")
    fh.write("th,td {\n")
    fh.write("    padding: 3px;\n")
    fh.write("}\n")
    fh.write("</style>\n")
    fh.write("<table border=\"1\"\">\n")
    fh.write("  <tr>\n    %s\n  </tr>" % "".join(
             "<th align=\"left\" bgcolor=\"#B0B0B0\">%s</th>" % field for field in first_record)
    )
    fh.write(" </tr>\n")

    # Dump!
    fh.writelines(
        "  <tr>\n    %s\n  </tr>\n" % "".join(
            "<td bgcolor=\"%s\"><font color=\"%s\" face=\"Arial\">%s</font></td>" % (colorize_bg(i, k, record), colorize_fg(i, k, record), field) 
            for k, field in enumerate(record)
        )
        for i, record in enumerate(adapted_table[1:])
    )
    fh.write("</table>\n")
    fh.close()

