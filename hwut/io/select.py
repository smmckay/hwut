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
import hwut.common         as common
from   hwut.io.messages    import *
import hwut.auxiliary.path as path
import sys
import os

def request_copy_OUT_to_GOOD(OUT_FileName):
    Dir = path.relative_to_home_pretty(os.getcwd())
    print ": Copy:  %s/%s"     % (Dir, OUT_FileName)
    print ": To:    %s/GOOD/ " % Dir
    print ":"
    print ": [yes,all,no,none,bye]" 

    result = sys.stdin.readline().strip().upper()
    if result == "BYE": print_bye_bye(); common.exit()
    return result

def request_file_list_deletion(Dir, FilenameList, DirnameList):
    """Returns a list of indeces or index-ranges indexing the files
       in the file name list that are to be deleted.
    """
    print "Following files are to be deleted:"
    print
    print "[index]  filename:"
    for i, file_name in enumerate(FilenameList):
        print "[%05i]: %s" % (i, file_name)

    return []
    print "Specify files to be deleted by their indices. Type 'all' to delete all."
    print "Example: 5                  deletes file number '5'"
    print "         5-10               deletes file number 5, 6, 7, 8, 9, and 10."
    print "         3, 5-8, 24, 27-30  deletes file number 3, 5, 6, 7, 8, 24, 27, 28, 29, 30"
    print 

    user_response = sys.stdin.readline().strip().upper()
    if user_response == "ALL": return range(len(FilenameList))

    response_list = user_response.split(",")
    result = []
    for response in response_list:
        fields = map(lambda x: x.strip(), response.split("-"))
        if fields.isdigit() == False:
            io.on_invalid_response(response)
            return []
        if len(fields)   == 1:
            result.append(int(fields[0]))
        elif len(fields) == 2:
            result.append(range(int(fields[0]), int(fields[1]) + 1))
        else:
            on_invalid_response(response)
            return []
 
    return result

def on_file_request_overwrite(FileName):
    Dir = path.relative_to_home_pretty(os.getcwd())
    print ": Overwrite:  %s/%s ?" % (Dir, FileName)
    result = sys.stdin.readline().strip().upper()
    if result == "BYE": print_bye_bye(); common.exit()
    return result

def directory(FileName, DirectoryList):
    """Requests from the user to determine an directory from where the
    files need to taken. 

    NameSP = Name in singular and plural. Example: ["library", "libraries"]

    RETURNS: Index of the chosen directory.
    """
    print ":  File '%s'" % FileName
    print ":  has been found in multiple directories:" 
    print ":  "
    L, txt = write_selection_list(DirectoryList)
    print ":  " + "-" * L
    print "".join(txt),
    print ":  " + "-" * L
    print ":  Select directory by number."
    print ":  "
    index, prefer_directory_f =  input_integer(0, len(DirectoryList))
    return index

def implementation(Reference, FileNameList, PreferenceOptionF=True, CrashOnCallF=True):
    """Requests from the user to determine the file name from a list of 
    possible files in order to select an implementation of a reference.

    RETURNS: [0] Index of the chosen file.
             [1] Flag indicating whether its directory shall be 'preferred'.
    """

    selection = {
            True:  ["Crash-on-call function stub!"], 
            False: [],
    }[CrashOnCallF] + FileNameList

    print ":  Reference '%s'" % Reference
    print ":  has been found in multiple files:" 
    print ":  "
    L, txt = write_selection_list(selection)
    print ":  " + "-" * L
    print "".join(txt),
    print ":  " + "-" * L
    if PreferenceOptionF:
        print ":  Select file by number. Add '-' to not prefer files of chosen directory."
    print ":  "
    if PreferenceOptionF:
        return input_integer(0, len(selection), "-", Offset = -1)
    else:
        return input_integer(0, len(selection), None, Offset = -1)

def print_word_list(Words):
    """Writes 'Words' in lines that never exceed the terminal width (as long 
    as no word is larger than the terminal width). 

    RETURNS: The extend of the longest line (without the ':  ' prefix)
    """
    line          = ":  "
    line_size     = 0
    line_size_max = 0
    for word in sorted(list(Words)):
       if line_size + len(word) > common.terminal_width(): 
           line += "\n:  "
           line_size = 0
       else:
           line_size += len(word)

       line += "%s " % word

       if line_size > line_size_max: line_size_max = line_size

    return line_size_max

def write_selection_list(SelectionList):
    L      = len(SelectionList)
    MaxPad = len("%i" % L)

    line_size_max = 0
    txt = []
    for i, choice in enumerate(SelectionList):
        line = "(%i) %s%s" % (i, " " * (MaxPad - len("%i" % i)), choice)
        if len(line) > line_size_max: line_size_max = len(line)
        txt.append(":  %s\n" % line)

    return line_size_max, txt

def input_integer(Min, Max, Option=None, Offset=0):
    """Reads an integer fromt the standard input and checks it against the
    given boundaries. Comments on errors are immediately printed.

    RETURNS: [0] Integer, if everything is ok.
                 None,    if the input was incorrect.
             [1] True, if the option 'Option' appeared.
                 False, else.
    """
    while 1 + 1 == 2:
        result = sys.stdin.readline().strip().upper()

        option_f = False
        if Option and result.find(Option):
            option_f = True
            result   = result.replace(Option, "")
            result   = result.strip()

        try:    
            x = int(result)
        except: 
            print ":  Expected a number. Please, try again."
            continue
        if x < Min: 
            print ":  Expected number greater or equal %i" % Min
            continue
        elif x > Max: 
            print ":  Expected number lesser or equal %i" % Max
            continue

        return x + Offset, option_f

def input(Pattern, HelpString):
    result = sys.stdin.readline().strip().upper()
    if fnmatch.fnmatch(result, Pattern):
        return result

    print ":  Input is not valid."
    for line in HelpString.splitlines():
        print ":  %s" % line

    return None
