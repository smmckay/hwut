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
import hwut.auxiliary.file_system               as fs
import hwut.auxiliary.table as     table
from   operator             import itemgetter
 
def write_coverage_result(CoverageDB):
    """Picture see 'messsages.coverage_summary()'
    """
    if CoverageDB is None: return

    write(fs.open_or_die("result-coverage.dat", "wb"), 
          CoverageDB.iterable_rows(), SpaceF=True)
        
def write_result_db(ResultDb, FileName, SpaceF=True):
    """Write test results into a CSV file given by 'FileName'. The file will 
    contain the following columns: 

        (0) directory  (1) applicationi (2) choice (3) verdict (4) time [sec] 
        (5) crc of GOOD file

    The first line will start with '#' to indicate a comment. It contains the 
    file header.

    The 'SpaceF' may be set to 'False' to avoid nicely formatting of columns
    by additional whitespace.
    """
    if not FileName:
        return

    field_name_list = [
        "directory", "application", "choice", "verdict", "time [sec]", "crc of GOOD file"
    ]
    field_list = [
        "(%i) %s" % (i, name) for i, name in enumerate(field_name_list)
    ]
    field_list[0] = "# %s" % field_list[0]

    table  = [
        ("%s" % directory,                  "%s" % description.file_name(),                     
         "%s" % result.choice,              "%s" % result.verdict,             
         "%s" % result.time_to_execute_sec, "%s" % result.crc_32)
        for directory, description, result in ResultDb
    ]
    table.insert(0, field_list)

    try:    
        fh = fs.open_or_die(FileName, "wb")
    except:
        print "Error: could not open file '%s' for writing reference data." % FileName
        return

    write(fh, table, SpaceF)
    fh.close()

def adapt(Field):
    """Adapt field, so that they are safe in CSV environments.
                   '\' --> '\\'
                   ';' --> '\;'
      => Any even number N of backslashes represents 
         N / 2 backslashes.
      => Any odd number N of backslashes followed by a ';' represents 
         (N-1)/2 backslashes and a ';'.
        
    """
    tmp = Field.replace("\\", "\\\\")
    return tmp.replace(";", "\\;")

def unadapt(Line):
    """Undo the adaptation of a line, as performed by 'adapt()'.
                   [^\]'\;' --> '\;'
                   '\\'     --> '\'
    RETURNS:
       A tuple containing the fields of a record.
    """
    if "\\" not in Field: return Field

    backslashed_f = False
    txt           = ""
    for letter in Field:
        if letter == "\\": 
            if backslashed_f: txt += "\\"
            backslashed_f = not backslashed_f
            continue
        elif letter == ";": 
            if backslashed_f: txt += ";"
            else:             result.append(txt.lstrip()); txt = ""
        else:
            txt += letter 
        backslashed_f = False
        
    # The last letter of a line should have been a ';'
    if txt.strip():
        print "Error: CSV file contained a line not ending with ';'"
        
    return result 

def write(fh, Table, SpaceF):
    """Write the given table to a file in 'CSV' format. All lines in the table
    shall have the same number of fields. If 'SpaceF' is True, then all columns
    will be nicely formatted, so that they read well as a table. If the flag is
    False, then no extra space is printed. 

    NOTE: -- Backslash characters are replaced by double backslashes. 
          -- ';' are replaced by '\;'
    """

    adapted_table = [ 
        tuple(adapt(field) for field in record)
        for record in Table
    ]
        
    # Define the 'pretty space' function for formatting of columns
    if SpaceF:
        La    = table.max_cell_widths(adapted_table)
        space = table.space
    else:
        La = None
        def space(Idx, Field, La):
            return " "

    # Dump!
    fh.writelines(
        "%s\n" % "".join(
            "%s; %s" % (field, space(i, field, La)) 
            for i, field in enumerate(record)
        )
        for record in adapted_table
    )

def read(FileName):
    fh = fs.open_or_die(FileName, "rb")
    
    result = []
    for line in fh.readlines():
        line = line.strip()
        if line and line[0] == "#": continue
        result.append(
            unadapt(line)
        )
    return result
