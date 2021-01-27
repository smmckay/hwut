# -*- coding: utf8 -*-
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
import hwut.auxiliary.file_system        as     fs
import hwut.auxiliary.path               as     aux
import hwut.auxiliary.executer.core           as     executer
import hwut.io.messages                  as     io
from   hwut.test_db.description          import TestDescription, E_Attr

from   StringIO import StringIO
import os
import re

def do(AppName, InterpreterSequence, LastInterviewTime):
    if      LastInterviewTime is not None \
        and os.stat(AppName).st_mtime < LastInterviewTime:
        # No interview required
        return None
   
    # Ask the application a serious question ...
    io.on_update_program_entry_info(AppName)
    file_name    = aux.ensure_dot_slash(AppName)

    command_line = InterpreterSequence + [file_name, "--hwut-info"]
    response_str = executer.do_stdout(command_line)

    # Parse the response
    new_descr = parse_response(AppName, response_str)
    assert new_descr is not None

    return new_descr

def parse_response(AppName, HwutInfoStr):
    """Parses the '--hwut-info' response of a test application. 
    
    RETURNS: TestDescription, containing the parsed data, if success.
             None,            in case of failure.
    """
    HwutInfoStr = HwutInfoStr.strip()

    if not HwutInfoStr:
        io.no_response_to_hwut_info(AppName)
        return TestDescription.from_NO_INFO(AppName)
    else:
        return TestDescription.from_interview(AppName, HwutInfoStr)

def clean_html_text(Text):
    db = {
            "\"": "&quot",  "&": "&amp",    "<": "&lt",     ">": "&gt",     "¡": "&iexcl",
            "¢": "&cent",   "£": "&pound",  "¤": "&curren", "¥": "&yen",    "¦": "&brvbar",
            "§": "&sect",   "¨": "&uml",    "©": "&copy",   "ª": "&ordf",   "«": "&laquo",
            "¬": "&not",    "­": "&shy",    "®": "&reg",    "¯": "&macr",   "°": "&deg",
            "±": "&plusmn", "¹": "&sup1",   "²": "&sup2",   "³": "&sup3",   "´": "&acute",
            "µ": "&micro",  "¶": "&para",   "·": "&middot", "¸": "&cedil",  "º": "&ordm",
            "»": "&raquo",  "¼": "&frac14", "½": "&frac12", "¾": "&frac34", "¿": "&iquest",
            "×": "&times",  "÷": "&divide", "Ð": "&ETH",    "ð": "&eth",    "Þ": "&THORN",
            "þ": "&thorn",  "Æ": "&AElig",  "æ": "&aelig",  "Œ": "&OElig",  "œ": "&oelig",
            "Å": "&Aring",  "Ø": "&Oslash", "Ç": "&Ccedil", "ç": "&ccedil", "ß": "&szlig",
            "Ñ": "&Ntilde", "ñ": "&ntilde", 
    }
    txt = Text
    for key, value in db.items():
        txt = txt.replace(key, value + ";")
    return txt

def __delete_related_output_files(test):
    for choice in test.result_list():
        out_file_name = aux.get_protocol_file_name(test, choice.name, OutputF=True)
        if os.access(out_file_name, os.F_OK):
            fs.try_remove(out_file_name)

